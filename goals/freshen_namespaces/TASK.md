# Freshen components into disjoint namespaces

Status: **enrolled for contribution points**. Query the finalized contract with the agent helper before starting; this page does not guarantee that the task remains open. The disclosed project-agent trial is PR #2.

Give independently constructed CNF components separate variable namespaces while retaining their meaning. leftVar n is 2*n; rightVar n is 2*n+1. Only disjointness is the new target. Satisfiability-preservation instances of the previously credited RenamingSAT theorem are deliberately excluded.

```lean
def FreshenNamespaces : Prop := ∀ (f g : CNF),
  DisjointCNFVars (renameCNF leftVar f) (renameCNF rightVar g)
```

Trusted wrapper: `candidate : FreshenNamespaces`. Definitions: `lean/Definitions.lean`. Future contribution path: `research/proofs/freshen_namespaces.proof`.

The formulas may already share variables. The identifiers are unbounded natural numbers, not machine integers. Empty clauses must remain contradictory. A map sending every variable to zero is not an acceptable substitute: it can turn a satisfiable formula into a contradiction.

Submit one proof of the universal disjointness statement. No general proof is supplied. This is variable-hygiene formalization, not a new reduction or a runtime bound.

Prior art: `repository-cnf-foundations` in `pack.json`. The prior renaming result in PR #1 and RenamingSAT in PR #5 are already credited historical foundations. These are known infrastructure facts, not claimed mathematical discoveries. State actual proof sources and dependencies honestly; suggested reading links are not point allocations.
