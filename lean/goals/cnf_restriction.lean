def CNFRestriction : Prop := ∀ (a : Nat → Bool) (x : Nat) (b : Bool) (f : CNF),
  evalCNF a (restrictCNF x b f) = evalCNF (assignVar a x b) f
