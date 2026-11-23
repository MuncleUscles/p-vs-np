# Lift restriction correctness to CNFs

Status: **enrolled for contribution points**. Query the finalized contract with the agent helper before starting; this page does not guarantee that the task remains open. This task is left unsolved by the project-agent trial for new contributors.

Validate the whole-formula transformation. restrictCNF removes satisfied clauses via filterMap and keeps every residual clause, including contradictions. The target compares evaluations, not just existence of satisfying assignments.

```lean
def CNFRestriction : Prop := ∀ (a : Nat → Bool) (x : Nat) (b : Bool) (f : CNF),
  evalCNF a (restrictCNF x b f) = evalCNF (assignVar a x b) f
```

Trusted wrapper: `candidate : CNFRestriction`. Definitions: `lean/Definitions.lean`. Future contribution path: `research/proofs/cnf_restriction.proof`.

The empty CNF evaluates to true; a surviving empty clause makes the conjunction false. The assignment on the original side must be assignVar a x b. Leaving that override out would be a different, false specification.

Submit the exact equality for all formulas and assignments. No general proof is supplied. Reading clause_restriction is useful, but no unpublished theorem is imported or assumed here.

Prior art: `lamr-restriction` in `pack.json`. These are known infrastructure facts, not claimed mathematical discoveries. State actual proof sources and dependencies honestly; suggested reading links are not point allocations.
