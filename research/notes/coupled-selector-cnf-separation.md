# Exact Exponential Separation Between Auxiliary-Variable Projections and Retained-Variable CNFs for Coupled Selector Families

## Question and scope

Accepted contribution PR #46 (`selector-cnf-clause-bound`) proves that eliminating one selector `z` from `m` clauses `(z | x_i)` and `n` clauses `(~z | y_j)` on disjoint retained variable blocks requires at least `mn` clauses in any list-CNF over the retained variables alone, and notes in its limitations that introducing auxiliary variables or altering equisatisfiability requirements changes the problem.

This nonformal note establishes the multi-selector counterpart when `k >= 1` selectors are coupled by one disjunction. Let `m_1, ..., m_k >= 0` with `M = sum_{r=1}^k m_r` retained variables `x_{r,i}` (`1 <= r <= k`, `1 <= i <= m_r`) and `k` disjoint auxiliary selector variables `z_1, ..., z_k`. Define the coupled selector CNF `Phi(m_1, ..., m_k)` with `1 + M` clauses:

1. One coupling clause `C_0 = (z_1 | z_2 | ... | z_k)`.
2. For each `r in {1, ..., k}` and `i in {1, ..., m_r}`, one binary clause `C_{r,i} = (~z_r | x_{r,i})`.

We prove three exact statements and verify finite cases in Python:

1. **Exact projection**: Existentially eliminating `z_1, ..., z_k` from `Phi` yields `F(x) = OR_{r=1}^k AND_{i=1}^{m_r} x_{r,i}` (empty `AND` for `m_r = 0` is `true`).
2. **Tight retained-variable CNF bound**: Every list-CNF over `{x_{r,i}}` alone that is pointwise equivalent to `F`—even allowing arbitrary literal signs, widths, repeated literals, duplicates, and tautologies—has at least `prod_{r=1}^k m_r` clauses, matching the canonical `Psi` expansion with equality.
3. **Linear 3-CNF auxiliary compression**: Splitting `C_0` with `k - 2` Tseitin variables `w_1, ..., w_{k-2}` (`k >= 3`) gives an exact 3-CNF projection of `(k - 1) + M` clauses (`k >= 2`, width `<= 3`) and `2k - 2` auxiliary variables (`k` for `k = 2`), yielding an exponential separation (`3k - 2` 3-clauses vs. `2^k` width-`k` clauses when `m_r = 2`).

We also compare these counts to the PR #19 / PR #22 truth-table baseline (`prod_{r=1}^k (2^{m_r} - 1)` falsifying assignments, i.e., `3^k` for `m_r = 2`) and contrast them with PR #14 list-resolution refutations under unit-falsifying assumptions.

## Proofs

### 1. Exact existential projection of `Phi(m_1, ..., m_k)`

Let `alpha` be any Boolean assignment to `{x_{r,i}}`.

- **Soundness (`=>`)**: If `(alpha, z)` satisfies `Phi`, `C_0` forces some `z_r = true`. For every `1 <= i <= m_r`, `C_{r,i} = (~z_r | x_{r,i})` forces `alpha(x_{r,i}) = true`, so `AND_{i=1}^{m_r} alpha(x_{r,i}) = true` and `F(alpha) = true`.
- **Completeness (`<=`)**: If `F(alpha) = true`, pick `r*` with `alpha(x_{r*,i}) = true` for all `1 <= i <= m_{r*}` (vacuous when `m_{r*} = 0`). Setting `z_{r*} = true` and `z_r = false` (`r != r*`) satisfies `C_0`, every `C_{r*,i}` via `x_{r*,i}`, and every `C_{r,i}` (`r != r*`) via `~z_r`.

### 2. Tight `prod_{r=1}^k m_r` bound without auxiliary variables

- **Upper bound**: If some `m_{r*} = 0`, `F` is constant `true`, represented by `0 = prod m_r` clauses. If all `m_r >= 1`, distributing `OR_{r=1}^k AND_{i=1}^{m_r} x_{r,i}` gives the positive `k`-CNF `Psi` with one clause `(x_{1,i_1} | ... | x_{k,i_k})` per tuple `(i_1, ..., i_k) in prod_{r=1}^k {1, ..., m_r}`, hence `|Psi| = prod_{r=1}^k m_r`.
- **Lower bound**: Assume all `m_r >= 1` (else `0` is trivial). Let `F_cnf` be any list-CNF over `{x_{r,i}}` (arbitrary signs, widths, duplicates, tautologies) with `evalCNF(alpha, F_cnf) = F(alpha)` for all `alpha`. For each `s = (s_1, ..., s_k) in prod_{r=1}^k {1, ..., m_r}`, define `alpha^(s)` by `alpha^(s)(x_{r,i}) = false` if `i = s_r` and `true` if `i != s_r`. Every block has one `false` variable, so `F(alpha^(s)) = false`, forcing some clause index `kappa(s)` in `F_cnf` with `c_{kappa(s)}` false under `alpha^(s)`.

  We show `kappa` is injective. Suppose `s != t` yet `kappa(s) = kappa(t)`, and set `c = c_{kappa(s)}`. Since `s != t`, some block `r*` has `s_{r*} != t_{r*}` (so `m_{r*} >= 2`). Consider `v = x_{r*, s_{r*}}`:
  - Under `alpha^(s)`, `alpha^(s)(v) = false`, so `c` cannot contain `(~v)` / `(v, false)`.
  - Under `alpha^(t)`, `t_{r*} != s_{r*}` implies `alpha^(t)(v) = true`, so `c` cannot contain `(v, true)`.

  Thus `v` does not appear in `c` with either polarity. Flipping only `v` from `false` to `true` in `alpha^(s)` produces `beta`. In `beta`, every variable in block `r*` is `true`, so `F(beta) = true`; yet `beta` agrees with `alpha^(s)` on all variables in `c`, so `c` remains `false` under `beta`, giving `evalCNF(beta, F_cnf) = false != F(beta)`, a contradiction. Hence `|F_cnf| >= prod_{r=1}^k m_r`.

### 3. Linear 3-CNF compression and comparison with PR #22 and PR #14

For `k >= 3`, replace `C_0` by `k - 1` clauses using `w_1, ..., w_{k-2}`: `(z_1 | z_2 | w_1)`, `(~w_t | z_{t+2} | w_{t+1})` (`1 <= t <= k - 3`), and `(~w_{k-2} | z_{k-1} | z_k)`. All `z_r = false` forces `w_1 = ... = w_{k-2} = true`, falsifying the last clause; if `z_j = true`, setting `w_t = true` for `t < j - 1` and `false` for `t >= j - 1` satisfies all `k - 1` clauses. Adding the `M` binary clauses `C_{r,i}` gives `(k - 1) + M` clauses (`k >= 2`), width `<= 3`.

For `m_r = 2` (`M = 2k`):
- **Auxiliary 3-CNF**: `3k - 2` clauses (`k >= 2`), `4k - 2` variables (`k >= 3`), `7k - 6` literal occurrences (`k >= 3`).
- **Minimum retained-variable CNF**: `2^k` clauses of width `k`, `k * 2^k` literal occurrences.
- **PR #19 / PR #22 falsifying-row baseline**: Each block contributes `2^{m_r} - 1` non-all-true assignments, so `F` has `prod_{r=1}^k (2^{m_r} - 1)` falsifying assignments (`3^k` when `m_r = 2`), exceeding `2^k`.
- **PR #14 resolution contrast**: Adding `k` blocking units `(~x_{r,1})` makes `Phi` unsatisfiable with a `2k`-step resolution refutation (resolve `(~z_r | x_{r,1})` with `(~x_{r,1})` to get `(~z_r)`, then resolve each `(~z_r)` against `C_0` to derive `[]`), whereas the retained-variable `Psi` has `2^k` clauses even before refutation.

## Reproducible finite checks

Executed locally with Python 3.13.15 (standard library only):

```python
from functools import reduce
from itertools import combinations, product

def eval_clause(a, c):
    return any(a[v] == sign for v, sign in c)

def eval_cnf(a, cnf):
    return all(eval_clause(a, c) for c in cnf)

def target_fn(m_list, a):
    off = 0
    for m in m_list:
        if all(a[off + i] for i in range(m)):
            return True
        off += m
    return False

def aux_cnf(m_list):
    M, k = sum(m_list), len(m_list)
    clauses = [[(M + r, True) for r in range(k)]]
    off = 0
    for r, m in enumerate(m_list):
        for i in range(m):
            clauses.append([(M + r, False), (off + i, True)])
        off += m
    return clauses, k

def aux_3cnf(m_list):
    M, k = sum(m_list), len(m_list)
    if k == 1:
        clauses, extra = [[(M, True)]], 1
    elif k == 2:
        clauses, extra = [[(M, True), (M + 1, True)]], 2
    else:
        w = M + k
        clauses = [[(M, True), (M + 1, True), (w, True)]]
        for t in range(k - 3):
            clauses.append([(w + t, False), (M + t + 2, True), (w + t + 1, True)])
        clauses.append([(w + k - 3, False), (M + k - 2, True), (M + k - 1, True)])
        extra = 2 * k - 2
    off = 0
    for r, m in enumerate(m_list):
        for i in range(m):
            clauses.append([(M + r, False), (off + i, True)])
        off += m
    return clauses, extra

for k in range(1, 5):
    m_list = [2] * k
    M = sum(m_list)
    c1, e1 = aux_cnf(m_list)
    c3, e3 = aux_3cnf(m_list)
    falses = 0
    for x in product((False, True), repeat=M):
        want = target_fn(m_list, x)
        falses += not want
        assert any(eval_cnf(x + z, c1) for z in product((False, True), repeat=e1)) == want
        assert any(eval_cnf(x + z, c3) for z in product((False, True), repeat=e3)) == want
    assert falses == 3 ** k
    print(f"k={k} M={M} aux_cnf={len(c1)} aux_3cnf={len(c3)} min_retained={2**k} falses={falses}")

for m_list in [[2], [1, 2], [2, 2]]:
    M = sum(m_list)
    assigns = list(product((False, True), repeat=M))
    sat = [a for a in assigns if target_fn(m_list, a)]
    unsat = [a for a in assigns if not target_fn(m_list, a)]
    masks = {
        sum((1 << i) for i, a in enumerate(unsat) if not eval_clause(a, [(v, s == 1) for v, s in enumerate(lits) if s]))
        for lits in product((0, 1, 2), repeat=M)
        if all(eval_clause(a, [(v, s == 1) for v, s in enumerate(lits) if s]) for a in sat)
    } - {0}
    full = (1 << len(unsat)) - 1
    best = next(sz for sz in range(1, len(unsat) + 1)
                if any(reduce(int.__or__, comb, 0) == full for comb in combinations(masks, sz)))
    print(f"exhaustive_min m={m_list}: {best}")
```

Actual output:

```text
k=1 M=2 aux_cnf=3 aux_3cnf=3 min_retained=2 falses=3
k=2 M=4 aux_cnf=5 aux_3cnf=5 min_retained=4 falses=9
k=3 M=6 aux_cnf=7 aux_3cnf=8 min_retained=8 falses=27
k=4 M=8 aux_cnf=9 aux_3cnf=11 min_retained=16 falses=81
exhaustive_min m=[2]: 2
exhaustive_min m=[1, 2]: 2
exhaustive_min m=[2, 2]: 4
```

## Prior art and limitations

- **PR #46 (`selector-cnf-clause-bound`)** and **Davis–Putnam (1960)** ([doi:10.1145/321033.321034](https://doi.org/10.1145/321033.321034)): PR #46 proves the tight `mn` bound for single-selector elimination over retained variables and flags auxiliary variables as out of scope. This note proves the tight `prod m_r` multi-selector generalization and linear 3-CNF contrast.
- **Tseitin (1968 / 1983)** ([doi:10.1007/978-3-642-81955-1_28](https://doi.org/10.1007/978-3-642-81955-1_28)) and **Cook–Reckhow (1979)** ([doi:10.2307/2273702](https://doi.org/10.2307/2273702)): Classical proof complexity establishes exponential compression from auxiliary extension variables; no novelty is claimed for Tseitin encoding or DNF-to-CNF blowup itself, only the tight integration with the repository's list-CNF semantics.
- **PR #19, PR #22, PR #14**: Supply the finite truth-table and list-resolution baselines.

**Limitations**: Nonformal note (`not-formal`), not Lean-checked. The `prod m_r` lower bound requires pointwise equivalence over retained variables without auxiliary variables; allowing auxiliary variables yields linear size. Exhaustive Python checks cover `k = 1..4` (`m_r = 2`) and general-CNF minimality up to `M = 4`. No general resolution lower bound, Extended Resolution lower bound, or P-versus-NP claim is made.
