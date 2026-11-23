def DisjointSAT : Prop := ∀ (f g : CNF), DisjointCNFVars f g →
  (Satisfiable (List.append f g) ↔ Satisfiable f ∧ Satisfiable g)
