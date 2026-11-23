# Verify one-variable clause restriction

Status: **supporting-only**. This draft is not enrolled and offers no active reward.

Validate the exact executable single-clause transformation in lean/Definitions.lean. The result none denotes a satisfied clause; some remaining denotes a surviving clause. Evaluation must match the original clause under assignVar for every original assignment.

```lean
def ClauseRestriction : Prop := ∀ (a : Nat → Bool) (x : Nat) (b : Bool) (c : Clause),
  evalRestrictedClause a (restrictClause x b c) = evalClause (assignVar a x b) c
```

Trusted wrapper: `candidate : ClauseRestriction`. Definitions: `lean/Definitions.lean`. Future contribution path: `research/proofs/clause_restriction.proof`.

In particular, some [] evaluates to false while none evaluates to true. Account for repeated variables, both signs in one tautological clause, absent variables and the empty clause. The output cannot depend on the original assignment at the overridden variable.

This is a supporting milestone for cnf_restriction, not a separately rewardable submission. Its singleton-CNF converse would duplicate essentially the same result. The supporting statement is the universal Boolean equality. No general proof is supplied. This is a reusable semantic primitive, not a whole satisfiability procedure.

Prior art: `lamr-restriction` in `pack.json`. These are known infrastructure facts, not claimed mathematical discoveries. State actual proof sources and dependencies honestly; suggested reading links are not point allocations.
