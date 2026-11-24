import fs from 'node:fs';
import {fileURLToPath, pathToFileURL} from 'node:url';

export const SOURCE_CASES = Object.freeze(['A', 'B', 'C', 'D-anthropic']);
const SOURCE_ROOT = new URL('../../.open-math/federation-sources/', import.meta.url);
const COLLECTOR = new URL('../../../protocol/github/github-provenance.mjs', import.meta.url);

export function loadSource(sourceCase) {
  if (!SOURCE_CASES.includes(sourceCase)) throw Error('Invalid source selection');
  const path = fileURLToPath(new URL(sourceCase + '.json', SOURCE_ROOT));
  const stat = fs.lstatSync(path);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.size > 16384) throw Error('Invalid source file');
  const bytes = fs.readFileSync(path, 'utf8'), value = JSON.parse(bytes);
  if (JSON.stringify(value, null, 2) + '\n' !== bytes) throw Error('Noncanonical source file');
  return value;
}

function failure(error) {
  const message = typeof error?.message === 'string' ? error.message : '';
  const status = /^GitHub provenance: HTTP ([1-5][0-9]{2}) for \/repos\//.exec(message);
  if (status) return {classification: 'collector-http-error', status: Number(status[1])};
  if (message === 'GitHub provenance: retrieval deadline exceeded') return {classification: 'collector-deadline'};
  if (message === 'GitHub provenance: GitHub request failed') return {classification: 'collector-transport-error'};
  return {classification: 'collector-validation-or-runtime-error'};
}

// Trusted transport injection is for local tests only. Remote documents never
// select code, endpoints, credentials, output fields, or the source request.
export async function diagnoseSource({sourceCase, token, collect, fetchImpl = globalThis.fetch}) {
  const source = loadSource(sourceCase);
  if (typeof collect !== 'function' || typeof fetchImpl !== 'function' ||
      typeof token !== 'string' || token.length === 0 || token.length > 4096 || !/^[\x21-\x7e]+$/.test(token)) {
    throw Error('Invalid diagnostic configuration');
  }
  const results = [];
  for (const authenticated of [true, false]) {
    let requestCount = 0;
    const transport = async (url, options) => {
      const target = new URL(url);
      const root = '/repos/' + source.repository;
      if (target.origin !== 'https://api.github.com' || target.username || target.password ||
          target.hash || !(target.pathname === root || target.pathname.startsWith(root + '/')) || options?.method !== 'GET' ||
          options.redirect !== 'error' || requestCount >= 64) throw Error('Unsafe diagnostic request');
      requestCount++;
      return fetchImpl(url, options);
    };
    try {
      const result = await collect(structuredClone(source), {
        ...(authenticated ? {token} : {}), fetchImpl: transport, timeoutMs: 30000,
      });
      if (!/^[a-f0-9]{64}$/.test(result?.source_hash) || !Array.isArray(result?.packet?.requests) ||
          result.packet.requests.length !== requestCount || requestCount === 0) throw Error('Invalid collector summary');
      results.push({source_case: sourceCase, authenticated, ok: true, source_hash: result.source_hash, request_count: requestCount});
    } catch (error) {
      results.push({source_case: sourceCase, authenticated, ok: false, request_count: requestCount, ...failure(error)});
    }
  }
  return results;
}

async function main() {
  // The workflow checks out this exact reviewed module at the frozen revision.
  // It imports only node:crypto; no dependency installation or native client.
  const {collectGithubProvenance} = await import(COLLECTOR.href);
  const results = await diagnoseSource({sourceCase: process.env.SOURCE_CASE, token: process.env.GITHUB_TOKEN, collect: collectGithubProvenance});
  for (const result of results) console.log(JSON.stringify(result));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(() => {
    console.log(JSON.stringify({ok: false, classification: 'diagnostic-configuration-error'}));
    process.exitCode = 1;
  });
}
