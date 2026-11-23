-- Trusted foundations. Core Lean only: no Mathlib dependency in this component.
def Clause := List (Nat × Bool)
def CNF := List Clause
def evalLiteral (a : Nat → Bool) (l : Nat × Bool) : Bool := a l.1 == l.2
def evalClause (a : Nat → Bool) (c : Clause) : Bool := c.any (evalLiteral a)
def evalCNF (a : Nat → Bool) (f : CNF) : Bool := f.all (evalClause a)
-- Goal: variable renaming commutes with CNF evaluation for every assignment.
-- This supports future reductions. It proves no complexity lower bound.
def renameClause (r : Nat → Nat) (c : Clause) : Clause := c.map (fun l => (r l.1, l.2))
def renameCNF (r : Nat → Nat) (f : CNF) : CNF := f.map (renameClause r)
def RenamingSound : Prop := ∀ (r : Nat → Nat) (a : Nat → Bool) (f : CNF),
  evalCNF a (renameCNF r f) = evalCNF (fun n => a (r n)) f

def Satisfiable (f : CNF) : Prop := ∃ a : Nat → Bool, evalCNF a f = true

-- Repeated variables are deliberately retained; membership is the only use.
def cnfVars (f : CNF) : List Nat := f.flatMap (fun c => c.map Prod.fst)
def DisjointCNFVars (f g : CNF) : Prop :=
  ∀ n : Nat, n ∈ cnfVars f → n ∈ cnfVars g → False

-- Freshening uses disjoint even and odd namespaces; no finite-width arithmetic.
def leftVar (n : Nat) : Nat := 2 * n
def rightVar (n : Nat) : Nat := 2 * n + 1

-- Assign exactly one variable, leaving all other values unchanged.
def assignVar (a : Nat → Bool) (x : Nat) (b : Bool) : Nat → Bool :=
  fun n => if n == x then b else a n

-- none means the clause was satisfied and can be removed from a conjunction.
-- some [] means a contradiction; these outcomes must never be conflated.
def restrictClause (x : Nat) (b : Bool) (c : Clause) : Option Clause :=
  if c.any (fun l => l.1 == x && l.2 == b) then none
  else some (c.filter (fun l => l.1 != x))
def evalRestrictedClause (a : Nat → Bool) (c : Option Clause) : Bool :=
  match c with
  | none => true
  | some remaining => evalClause a remaining
def restrictCNF (x : Nat) (b : Bool) (f : CNF) : CNF :=
  f.filterMap (restrictClause x b)
