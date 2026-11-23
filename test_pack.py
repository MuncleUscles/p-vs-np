"""Offline regressions for reviewed pack assembly, not arbitrary proof execution."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent

class PackChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pnp-pack-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'pack'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '.pack-check-*', '.validation-*'))
        self.manifest = json.loads((self.root / 'pack.json').read_text())

    def run_check(self):
        (self.root / 'pack.json').write_text(json.dumps(self.manifest))
        return subprocess.run([os.sys.executable, '-B', str(self.root / 'check-pack.py')],
                              cwd=self.temp.name, capture_output=True, text=True, timeout=60)

    def test_portable_positive_from_another_directory(self):
        run = self.run_check()
        self.assertEqual(run.returncode, 0, run.stderr)
        evidence = json.loads((self.root / 'validation.json').read_text())
        self.assertEqual(evidence['openGeneralProofsSupplied'], 0)
        self.assertEqual(evidence['boundaryCount'], 28)
        self.assertEqual(len(evidence['negativeProofChecks']), 5)

    def test_changed_definitions_fail_and_remove_stale_success(self):
        file = self.root / 'lean/Definitions.lean'
        file.write_text(file.read_text().replace('c.any (evalLiteral a)', 'false'))
        run = self.run_check()
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('hash mismatch', run.stderr)
        self.assertFalse((self.root / 'validation.json').exists())

    def test_rehashed_false_reference_is_actually_compiled(self):
        name = 'reference/disjoint_sat.proof'
        proof = b'by exact True.intro\n'
        (self.root / name).write_bytes(proof)
        self.manifest['trustedFiles'][name] = hashlib.sha256(proof).hexdigest()
        run = self.run_check()
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Lean rejected', run.stderr)
        self.assertFalse((self.root / 'validation.json').exists())

    def test_boundary_axiom_coverage_cannot_be_silently_omitted(self):
        self.manifest['boundaries']['theorems'].pop()
        run = self.run_check()
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('coverage mismatch', run.stderr)
        self.assertFalse((self.root / 'validation.json').exists())

    def test_display_cannot_diverge_from_the_executed_goal(self):
        self.manifest['goals'][1]['statementDisplay'] = 'def FreshenNamespaces : Prop := True'
        run = self.run_check()
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Statement display/hash mismatch', run.stderr)
        self.assertFalse((self.root / 'validation.json').exists())

if __name__ == '__main__':
    unittest.main()
