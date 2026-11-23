# Compose CNFs with disjoint variables

Status: **reference-only**. This draft is not enrolled and offers no active reward.

The reference shows how independently satisfiable components can be joined when their variable sets are disjoint. The published proof is already available and copied unchanged under reference/.

```lean
def DisjointSAT : Prop := ∀ (f g : CNF), DisjointCNFVars f g →
  (Satisfiable (List.append f g) ↔ Satisfiable f ∧ Satisfiable g)
```

Trusted wrapper: `candidate : DisjointSAT`. Definitions: `lean/Definitions.lean`. Verification fixture only: `reference/disjoint_sat.proof`. No reward submission is requested.

Empty formulas are allowed. Opposite unit clauses on one variable show why the disjointness condition cannot simply be deleted. Overlap can also be satisfiable, so disjointness is sufficient rather than necessary for each pair.

No new proof is requested for reward. Use the disclosed expression only as a positive integration fixture; copying or renaming it is not an independent contribution.

Prior art: `biere-sinz-2006`, `repository-disjoint-reference` in `pack.json`. These are known infrastructure facts, not claimed mathematical discoveries. State actual proof sources and dependencies honestly; suggested reading links are not point allocations.
