def ClauseRestriction : Prop := ∀ (a : Nat → Bool) (x : Nat) (b : Bool) (c : Clause),
  evalRestrictedClause a (restrictClause x b c) = evalClause (assignVar a x b) c
