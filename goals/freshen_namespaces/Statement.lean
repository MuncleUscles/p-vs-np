def FreshenNamespaces : Prop := ∀ (f g : CNF),
  DisjointCNFVars (renameCNF leftVar f) (renameCNF rightVar g)
