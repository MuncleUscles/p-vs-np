#!/usr/bin/env python3
"""Compile reviewed local pack definitions/boundaries/reference; not a PR sandbox."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'validation.json'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def local(relative):
    require(isinstance(relative, str) and not Path(relative).is_absolute(), 'Relative trusted path required')
    result = ROOT / relative
    require(result.resolve().is_relative_to(ROOT) and result.is_file() and not result.is_symlink(), 'Invalid trusted path')
    return result

def run_lean(lean, source, positive=True):
    with tempfile.TemporaryDirectory(prefix='.pack-check-', dir=ROOT) as directory:
        file = Path(directory) / 'Check.lean'
        file.write_bytes(source)
        run = subprocess.run([lean, '--trust=0', '-DmaxHeartbeats=100000', str(file)],
                             capture_output=True, text=True, timeout=45)
    log = run.stdout + run.stderr
    if positive:
        require(run.returncode == 0 and not any(word in log for word in ['warning:', 'error:', 'sorryAx']),
                'Lean rejected reviewed assembly:\n' + log[:4000])
    else:
        require(run.returncode != 0 and 'error:' in log, 'False proof fixture unexpectedly passed')
    return {'sha256': sha(source), 'bytes': len(source), 'exitCode': run.returncode, 'log': log if positive else 'Rejected deliberately false proof.'}

def axioms(log, names, allowed):
    reports = {}
    for name in names:
        pattern = r"^'" + re.escape(name) + r"' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)$"
        matches = list(re.finditer(pattern, log, re.M))
        require(len(matches) == 1, 'Missing or ambiguous axiom report for ' + name)
        values = [x.strip() for x in (matches[0].group(1) or '').split(',') if x.strip()]
        require(set(values) <= set(allowed), 'Unexpected axioms for ' + name)
        reports[name] = values
    return reports

def verify():
    lean = os.environ.get('LEAN_BIN') or 'lean'
    version = subprocess.run([lean, '--version'], capture_output=True, text=True, check=True, timeout=10).stdout.strip()
    require(re.match(r'^Lean \(version 4\.19\.0(?:,|\))', version), 'Exact Lean 4.19.0 required')
    manifest_bytes = (ROOT / 'pack.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest['schemaVersion'] == 1 and manifest['activation'] == 'draft-unenrolled', 'Unexpected pack state')
    require(manifest['toolchain'] == 'leanprover/lean4:v4.19.0' and manifest['mathlib'] is None, 'Unexpected toolchain')
    require(manifest['allowedAxioms'] == ['propext', 'Quot.sound'], 'Unexpected axiom policy')
    files = {name: local(name).read_bytes() for name in manifest['trustedFiles']}
    for name, data in files.items():
        require(len(data) <= 16000, 'Trusted file exceeds bound')
        data.decode('utf-8', errors='strict')
        require(sha(data) == manifest['trustedFiles'][name], 'Trusted file hash mismatch: ' + name)
    require(len(manifest['goals']) == 5 and len({g['id'] for g in manifest['goals']}) == 5, 'Expected five distinct goals')
    definitions = files[manifest['definitions']['path']]
    boundaries = files[manifest['boundaries']['path']]
    require(sha(definitions) == manifest['definitions']['sha256'] and sha(boundaries) == manifest['boundaries']['sha256'], 'Metadata binding mismatch')
    statements = []
    for goal in manifest['goals']:
        require(re.fullmatch(r'candidate : [A-Za-z][A-Za-z0-9]*', goal['declaration']), 'Unexpected declaration')
        statement = files[goal['statementPath']]
        require(sha(statement) == goal['statementSha256'] and statement.decode().strip() == goal['statementDisplay'], 'Statement display/hash mismatch')
        require(len(goal['statementDisplay']) <= 2000 and goal['dependencies'] == [], 'Unsupported statement/dependency shape')
        expected_status = {'disjoint_sat': 'reference-only', 'freshen_namespaces': 'proposed-open', 'clause_restriction': 'supporting-only', 'cnf_restriction': 'proposed-open', 'unit_propagation': 'deferred'}
        require(goal['status'] == expected_status[goal['id']], 'Unexpected goal availability')
        require(goal['rewardable'] == (goal['id'] in ['freshen_namespaces', 'cnf_restriction']), 'Launch eligibility mismatch')
        require(not (ROOT / goal['proofPath']).exists(), 'A proposed research proof must not already be supplied')
        statements.append(statement)
    names = ['Boundary.' + name for name in manifest['boundaries']['theorems']]
    require(len(names) == len(set(names)) and manifest['boundaries']['theorems'] == re.findall(r'^theorem (\w+)', boundaries.decode(), re.M), 'Boundary audit coverage mismatch')
    audit = '\n'.join('#print axioms ' + name for name in names).encode()
    boundary_run = run_lean(lean, definitions + b'\n' + b'\n'.join(statements) + b'\n' + boundaries + b'\n' + audit)
    boundary_axioms = axioms(boundary_run['log'], names, manifest['allowedAxioms'])
    reference_goal = next(g for g in manifest['goals'] if g['id'] == 'disjoint_sat')
    proof = files[reference_goal['referenceProof']]
    reference_source = definitions + b'\n' + files[reference_goal['statementPath']] + b'\ntheorem candidate : DisjointSAT := ' + proof + b'\nexample : DisjointSAT := candidate\n#print axioms candidate\n'
    reference_run = run_lean(lean, reference_source)
    reference_axioms = axioms(reference_run['log'], ['candidate'], manifest['allowedAxioms'])
    negative_runs = {}
    for goal in manifest['goals']:
        source = definitions + b'\n' + files[goal['statementPath']] + ('\ntheorem ' + goal['declaration'] + ' := by exact True.intro\n').encode()
        negative_runs[goal['id']] = run_lean(lean, source, positive=False)
    return {'status': 'pass', 'scope': 'Reviewed local definitions, exact goal types, boundary checks and disclosed reference only; not sandbox, native enrollment, reward or proof of the unimplemented general goals.', 'packSha256': sha(manifest_bytes), 'toolchain': version, 'kernelTrust': 0, 'maxHeartbeats': 100000, 'boundaryCount': len(names), 'boundaries': boundary_run, 'boundaryAxioms': boundary_axioms, 'reference': reference_run, 'referenceAxioms': reference_axioms, 'negativeProofChecks': negative_runs, 'openGeneralProofsSupplied': 0, 'trustedFiles': manifest['trustedFiles']}

def main():
    EVIDENCE.unlink(missing_ok=True)
    try:
        result = verify()
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=ROOT, prefix='.validation-', delete=False) as file:
            json.dump(result, file, indent=2)
            file.write('\n')
            temporary = Path(file.name)
        temporary.replace(EVIDENCE)
        print(json.dumps({'status': result['status'], 'boundaryCount': result['boundaryCount'], 'openGeneralProofsSupplied': 0, 'negativeProofChecks': len(result['negativeProofChecks']), 'packSha256': result['packSha256']}))
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print('Pack verification failed: ' + str(error), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
