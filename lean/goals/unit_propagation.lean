def UnitPropagation : Prop := ∀ (x : Nat) (b : Bool) (f : CNF),
  List.Mem [(x, b)] f → (Satisfiable (restrictCNF x b f) ↔ Satisfiable f)
