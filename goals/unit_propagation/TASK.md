# Preserve satisfiability for one forced unit step

Status: **deferred**. This draft is not enrolled and offers no active reward.

Verify one forced unit step. The formula must contain exactly the singleton clause [(x,b)]; restrictCNF then sets that literal and simplifies the formula. Both directions of satisfiability preservation are required.

```lean
def UnitPropagation : Prop := ∀ (x : Nat) (b : Bool) (f : CNF),
  List.Mem [(x, b)] f → (Satisfiable (restrictCNF x b f) ↔ Satisfiable f)
```

Trusted wrapper: `candidate : UnitPropagation`. Definitions: `lean/Definitions.lean`. Future contribution path: `research/proofs/unit_propagation.proof`.

The membership assumption is List.Mem explicitly, because CNF is a reviewed def alias. The condition is inhabited, but cannot be dropped: restricting the satisfiable formula [[(0,false)]] using value true produces an empty contradictory clause. One step may create another unit; repeated propagation is outside this goal.

This roadmap statement is deferred until verified dependency attribution is supported; it is not an active reward task. Its target is the exact equivalence under the stated membership condition. No general proof is supplied. This does not establish iterative propagation, DPLL completeness or complexity.

Prior art: `lamr-restriction` in `pack.json`. These are known infrastructure facts, not claimed mathematical discoveries. State actual proof sources and dependencies honestly; suggested reading links are not point allocations.
