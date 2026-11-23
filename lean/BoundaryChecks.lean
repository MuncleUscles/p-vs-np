-- Reviewed semantic sentinels, not general solutions to the open goals.
namespace Boundary

theorem empty_cnf_sat : Satisfiable ([] : CNF) := ⟨fun _ => false, rfl⟩
theorem empty_clause_unsat : ¬ Satisfiable ([[]] : CNF) := by
  intro ⟨a, ha⟩
  simp [evalCNF, evalClause] at ha

theorem positive_unit_sat : Satisfiable [[(0, true)]] := ⟨fun _ => true, rfl⟩
theorem negative_unit_sat : Satisfiable [[(0, false)]] := ⟨fun _ => false, rfl⟩
theorem opposite_units_unsat : ¬ Satisfiable ([[(0, true)]] ++ [[(0, false)]]) := by
  intro ⟨a, ha⟩
  change ((a 0 == true || false) && ((a 0 == false || false) && true)) = true at ha
  cases h : a 0 <;> simp [h] at ha

theorem overlapping_variables : ¬ DisjointCNFVars [[(0, true)]] [[(0, false)]] := by
  intro h
  exact h 0 (by simp [cnfVars]) (by simp [cnfVars])
theorem overlap_can_be_sat : Satisfiable ([[(0, true)]] ++ [[(0, true)]]) :=
  ⟨fun _ => true, rfl⟩

-- Nonempty collision example becomes disjoint; both literal signs survive.
theorem freshening_shapes :
    renameCNF leftVar [[(0, true), (3, false)]] = [[(0, true), (6, false)]] ∧
    renameCNF rightVar [[(0, false), (3, true)]] = [[(1, false), (7, true)]] := by
  constructor <;> rfl
theorem freshened_conflict_is_sat :
    Satisfiable (List.append (renameCNF leftVar [[(0, true)]])
      (renameCNF rightVar [[(0, false)]])) :=
  ⟨fun n => n == 0, rfl⟩
theorem freshened_empty_clause_unsat :
    ¬ Satisfiable (renameCNF rightVar ([[]] : CNF)) := by
  intro ⟨a, ha⟩
  simp [renameCNF, renameClause, evalCNF, evalClause] at ha

-- A collapsing map does not preserve satisfiability; freshness has substance.
theorem different_variables_sat : Satisfiable [[(0, true)], [(1, false)]] :=
  ⟨fun n => n == 0, rfl⟩
theorem collapsed_variables_unsat :
    ¬ Satisfiable (renameCNF (fun _ => 0) [[(0, true)], [(1, false)]]) := by
  intro ⟨a, ha⟩
  change ((a 0 == true || false) && ((a 0 == false || false) && true)) = true at ha
  cases h : a 0 <;> simp [h] at ha

-- Distinguish removing a satisfied clause from retaining an empty contradiction.
theorem satisfied_clause_removed : restrictClause 0 true [(0, true)] = none := rfl
theorem falsified_clause_retained : restrictClause 0 true [(0, false)] = some [] := rfl
theorem empty_clause_retained : restrictClause 0 false [] = some [] := rfl
theorem absent_variable_unchanged :
    restrictClause 7 false [(0, true), (1, false)] = some [(0, true), (1, false)] := rfl
theorem mixed_clause_restricted :
    restrictClause 0 true [(0, false), (1, true), (0, false)] = some [(1, true)] := rfl
theorem tautological_clause_removed :
    restrictClause 0 false [(0, true), (0, false)] = none := rfl
theorem option_semantics : evalRestrictedClause (fun _ => false) none = true ∧
    evalRestrictedClause (fun _ => false) (some []) = false := ⟨rfl, rfl⟩
theorem assignment_override : assignVar (fun _ => false) 0 true 0 = true ∧
    assignVar (fun _ => false) 0 true 1 = false := ⟨rfl, rfl⟩

theorem cnf_restriction_keeps_conflict :
    restrictCNF 0 true [[(0, true)], [(0, false)]] = [[]] := rfl
theorem cnf_restriction_example :
    restrictCNF 0 true [[(0, true)], [(0, false), (1, true)], [(2, false)]] =
      [[(1, true)], [(2, false)]] := rfl
theorem restriction_of_empty_cnf : restrictCNF 0 true [] = [] := rfl
theorem restriction_of_empty_clause : restrictCNF 0 true [[]] = [[]] := rfl

-- Unit side condition is inhabited, but deleting it gives a false SAT claim.
theorem unit_condition_present : [(0, true)] ∈ ([[ (0, true) ], [(1, false)]] : CNF) := by
  simp
theorem unit_condition_not_automatic : ¬ ([(0, true)] ∈ ([[(0, false)]] : CNF)) := by
  decide
theorem forced_wrong_value_unsat :
    ¬ Satisfiable (restrictCNF 0 true [[(0, false)]]) := by
  exact empty_clause_unsat

theorem one_step_is_not_fixpoint :
    restrictCNF 0 true [[(0, true)], [(0, false), (1, true)]] = [[(1, true)]] := rfl

end Boundary
