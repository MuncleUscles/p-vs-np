import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {SOURCE_CASES, loadSource, diagnoseSource} from './source-collector-access.mjs';

const token = 'diagnostic-test-credential-DO-NOT-LOG';
const digest = 'a'.repeat(64);
const options = {method: 'GET', redirect: 'error'};

test('only exact checked-in source cases can be selected', () => {
  assert.deepEqual(SOURCE_CASES, ['A', 'B', 'C', 'D-anthropic']);
  for (const name of SOURCE_CASES) {
    const source = loadSource(name);
    assert.ok(Number.isSafeInteger(source.pr) && source.pr > 0);
    assert.match(source.commit, /^[a-f0-9]{40}$/);
  }
  for (const bad of [undefined, '', 'none', '../B', 'A.json', 'A/../../B', 'B\n', '__proto__']) {
    assert.throws(() => loadSource(bad), /Invalid source selection/);
  }
});

test('runs the complete collector with token first and then without credentials', async () => {
  const seen = [], requests = [];
  const result = await diagnoseSource({sourceCase: 'B', token,
    collect: async (request, settings) => {
      seen.push({request, settings});
      await settings.fetchImpl('https://api.github.com/repos/' + request.repository, options);
      await settings.fetchImpl('https://api.github.com/repos/' + request.repository + '/pulls/' + request.pr, options);
      return {source_hash: digest, packet: {requests: [{}, {}], confidential_body: token}, secret: token};
    },
    fetchImpl: async (url, settings) => { requests.push({url, settings}); return {}; },
  });
  assert.equal(seen.length, 2);
  assert.deepEqual(seen[0].request, loadSource('B'));
  assert.deepEqual(seen[1].request, loadSource('B'));
  assert.notEqual(seen[0].request, seen[1].request);
  assert.equal(seen[0].settings.token, token);
  assert.equal(Object.hasOwn(seen[1].settings, 'token'), false);
  assert.equal(seen[0].settings.timeoutMs, 30000);
  assert.equal(seen[1].settings.timeoutMs, 30000);
  assert.equal(requests.length, 4);
  assert.deepEqual(result, [true, false].map(authenticated => ({source_case: 'B', authenticated, ok: true, source_hash: digest, request_count: 2})));
  assert.ok(!JSON.stringify(result).includes(token));
});

test('collector failures expose fixed classification and bounded numeric fields only', async () => {
  for (const [message, expected] of [
    ['GitHub provenance: HTTP 403 for /repos/any/' + token, {classification: 'collector-http-error', status: 403}],
    ['GitHub provenance: retrieval deadline exceeded', {classification: 'collector-deadline'}],
    ['GitHub provenance: GitHub request failed', {classification: 'collector-transport-error'}],
    ['foreign response body or credential ' + token, {classification: 'collector-validation-or-runtime-error'}],
  ]) {
    const result = await diagnoseSource({sourceCase: 'A', token, collect: async () => { throw Error(message); }});
    assert.deepEqual(result, [true, false].map(authenticated => ({source_case: 'A', authenticated, ok: false, request_count: 0, ...expected})));
    assert.ok(!JSON.stringify(result).includes(token));
  }
});

test('transport refuses foreign endpoints, repository switches, redirects and writes', async () => {
  for (const [url, settings] of [
    ['https://example.com/repos/brilliant-hq/pequalnp-proofs', options],
    ['https://api.github.com/repos/other/repo', options],
    ['https://user:password@api.github.com/repos/brilliant-hq/pequalnp-proofs', options],
    ['https://api.github.com/repos/brilliant-hq/pequalnp-proofs#fragment', options],
    ['https://api.github.com/repos/brilliant-hq/pequalnp-proofs', {method: 'POST', redirect: 'error'}],
    ['https://api.github.com/repos/brilliant-hq/pequalnp-proofs', {method: 'GET', redirect: 'follow'}],
  ]) {
    let contacted = false;
    const result = await diagnoseSource({sourceCase: 'B', token, fetchImpl: async () => { contacted = true; }, collect: async (_, settings_) => settings_.fetchImpl(url, settings)});
    assert.equal(contacted, false);
    assert.ok(result.every(row => row.ok === false && row.request_count === 0));
  }
});

test('does not print a collector packet or an unchecked success summary', async () => {
  for (const value of [{source_hash: token, packet: {requests: []}}, {source_hash: digest, packet: {requests: []}}, {source_hash: digest, packet: {requests: [{}]}}]) {
    const result = await diagnoseSource({sourceCase: 'C', token, collect: async () => value});
    assert.ok(result.every(row => row.ok === false));
    assert.ok(!JSON.stringify(result).includes(token));
  }
});

test('workflow stays read-only and main-only with fixed collector revision and checked-out requests', () => {
  const text = fs.readFileSync(new URL('../workflows/source-access.yml', import.meta.url), 'utf8');
  assert.match(text, /permissions:\n  contents: read\n/);
  assert.match(text, /if: github.ref == 'refs\/heads\/main'/);
  assert.match(text, /ref: 7669a2cdd54dee1f828f02f86723b4d5ff526075/);
  assert.match(text, /ref: \$\{\{ github.sha \}\}/);
  assert.match(text, /options: \[none, A, B, C, D-anthropic\]/);
  assert.equal((text.match(/persist-credentials: false/g) || []).length, 2);
  assert.doesNotMatch(text, /secrets\.|contents: write|checks: write|pull-requests: write|environment: protocol|npm ci|manage-federation|run-federation/);
});
