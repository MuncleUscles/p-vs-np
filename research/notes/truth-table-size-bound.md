# Exact row cost of the finite truth-table certificate format

This is a research note, not a Lean-checked theorem. It gives an exact size specification and a separating benchmark for the accepted finite checker in [PR #19](https://github.com/MuncleUscles/p-vs-np/pull/19). The counting and resolution arguments are elementary known methods; the contribution is their explicit integration with this repository's definitions, including edge cases and executable regression data.

## Object under analysis

The exact source is [finite-truth-table-certificates.json at d5d340c](https://github.com/MuncleUscles/p-vs-np/blob/d5d340c74a44616d1998cdb1ac0eac66ac2eb795/research/artifacts/finite-truth-table-certificates.json), bundle SHA-256 `b7472b94ef951596bf9effbeb5e46756b6c6c3d0d56a92c50a040c2a39b42543`. Its variables are `Fin n`, assignments are functions `Fin n -> Bool`, clauses are literal lists, and the CNF is indexed by `Fin m`. A literal `(v,b)` is true exactly when the assignment at v is b.

A certificate C is a finite set of pairs (a,j). The definition `check` requires (i) for every assignment a, some (a,j) belongs to C, and (ii) every row in C names a clause j falsified by a. The definition `certificate` includes *all* such falsified pairs. These two definitions, not a claim about all UNSAT proof systems, are the scope below.

## Tight minimum and exact generator size

**Proposition 1.** Every accepted certificate has at least 2^n rows. For an unsatisfiable CNF, its minimum accepted certificate size is exactly 2^n. An accepted certificate attains this minimum exactly when each assignment occurs in one row.

There are 2^n assignments. The first projection from C onto assignments is surjective by coverage; its nonempty fibers partition C. Thus |C| is the sum of 2^n positive fiber sizes and is at least 2^n, with equality exactly when all fibers have size one. If f is UNSAT, each assignment falsifies some clause. Choose the least falsified clause index for each assignment. The resulting pairs are distinct in their first coordinate, satisfy both checks, and number 2^n. This is an existence and exhaustive-construction argument, not a fast SAT algorithm.

**Proposition 2.** Let d_j be the number of *distinct variables* in indexed clause j. Its contribution to the all-row generator is zero if it contains both signs of a variable, and otherwise 2^(n-d_j). Therefore

    |certificate(f)| = sum over non-tautological indexed clauses j of 2^(n-d_j).

For a non-tautological clause, falsity fixes one consistent Boolean value on each of its d_j variables, leaving n-d_j free choices. A tautological clause has no falsifying assignment. Rows with different clause indices are distinct, so sum these counts even for syntactically duplicate clauses. Repeated same-sign literals do not add constraints. An empty clause has d_j=0 and contributes 2^n rows.

The formula holds for satisfiable f too, but then the generated rows fail coverage. For n=0 there is one empty assignment; the only possible clause is empty. With m=0 there is no accepted certificate; with m>0 the minimum is one and the all-row generator has m rows. Thus neither empty domains nor duplicate clauses justify replacing the indexed sum by a set of distinct clauses.

## A minimally unsatisfiable separating family

For n>=1 consider the Horn CNF

    F_n = (x_1) AND (not x_1 OR x_2) AND ...
          AND (not x_(n-1) OR x_n) AND (not x_n).

For n=1 the middle conjunction is empty. There are n+1 clauses and 2n literal occurrences, and every variable occurs. Unit propagation from x_1 forces every x_i true and contradicts the last clause. The family is minimally UNSAT: deleting x_1 admits the all-false assignment; deleting not x_n admits all-true; deleting implication i admits x_1,...,x_i true and x_(i+1),...,x_n false. This rules out unused-variable padding and redundant-clause padding as explanations for the size gap.

Every accepted row certificate has at least 2^n rows, and that minimum is attained. The all-row generator has two unit-clause contributions of 2^(n-1) and, for n>=2, n-1 binary-clause contributions of 2^(n-2). Hence its size is (n+3)2^(n-2), versus 2 for n=1. For n>=2 its overhead relative to an optimal row certificate is exactly (n+3)/4.

Resolution is short on the same family: resolve the unit x_i with (not x_i OR x_(i+1)) to derive x_(i+1), then resolve x_n with not x_n to obtain the empty clause. This uses n steps, including the final step. In the list representation of [PR #14](https://github.com/MuncleUscles/p-vs-np/pull/14), each left premise is the already derived positive unit and each right premise is an original clause. Its `resolve` filters the pivot from both sides, leaving precisely the next unit or the empty list. No contraction or weakening is needed. This is a paper-level encoding argument, not a new Lean proof of a conversion between the two representations.

With explicit binary variable indices, F_n occupies O(n log(n+1)) input bits; 2^n rows therefore grow faster than every polynomial in this input length. The bound is exponential in n, not asserted exponential in the binary input length. A flat certificate storing n Boolean bits per row needs at least n*2^n assignment bits when n>=1. A succinct program describing the rows can be much smaller, but checking that different format would require an additional soundness argument and is outside this result.

## Reproducible finite checks

The following standard-library-only Python code was executed locally with Python 3.14.7. It mirrors the two certificate definitions and the list resolution operation, checks the general counting formula on six edge cases, and checks F_n for n=1..8. It does not execute Lean, extract verified code, measure timing, or establish an asymptotic theorem by experiment. Run the code in this section with `python3`; no repository changes or packages are required.

```python
from itertools import product

def assignments(n):
    return list(product((False, True), repeat=n))

def holds(a, c):
    return any(a[v] == sign for v, sign in c)

def all_rows(n, clauses):
    return {(a, j) for a in assignments(n)
            for j, c in enumerate(clauses) if not holds(a, c)}

def predicted(n, clauses):
    total = 0
    for c in clauses:
        literals = set(c)
        tautology = any((v, not sign) in literals for v, sign in literals)
        if not tautology:
            total += 2 ** (n - len({v for v, _ in literals}))
    return total

def chain(n):
    return [[(0, True)]] + [[(i, False), (i + 1, True)]
                            for i in range(n - 1)] + [[(n - 1, False)]]

def resolution_steps(n, clauses):
    derived = list(clauses)
    for i in range(n):
        left = [(i, True)]
        right = [(i, False), (i + 1, True)] if i + 1 < n else [(i, False)]
        assert left in derived and right in derived
        derived.append([l for l in left if l != (i, True)] +
                       [l for l in right if l != (i, False)])
    assert derived[-1] == []
    return n

print('n clauses minimum_rows all_rows resolution_steps')
for n in range(1, 9):
    f = chain(n)
    rows = all_rows(n, f)
    assert len(rows) == predicted(n, f)
    assert len(rows) == (2 if n == 1 else (n + 3) * 2 ** (n - 2))
    selected = {(a, min(j for j, c in enumerate(f) if not holds(a, c)))
                for a in assignments(n)}
    assert selected <= rows and len(selected) == 2 ** n
    # Deleting any one clause leaves a satisfying assignment.
    for omitted in range(len(f)):
        assert any(all(holds(a, c) for j, c in enumerate(f) if j != omitted)
                   for a in assignments(n))
    print(n, len(f), len(selected), len(rows), resolution_steps(n, f))

# Empty domains; repeated literals/clauses; tautologies; unused variable.
for n, f in [(0, []), (0, [[]]), (0, [[], []]),
             (1, [[(0, True), (0, True)]]),
             (1, [[(0, True), (0, False)]]),
             (2, [[(0, True)], [(0, True)], []])]:
    assert len(all_rows(n, f)) == predicted(n, f)
print('six edge cases passed')
```

Actual output:

```text
n clauses minimum_rows all_rows resolution_steps
1 2 2 2 1
2 3 4 5 2
3 4 8 12 3
4 5 16 28 4
5 6 32 64 5
6 7 64 144 6
7 8 128 320 7
8 9 256 704 8
six edge cases passed
```

## Research consequence, prior art, and limits

PR #19 already discloses exponential enumeration and an upper bound of m*2^n rows. This note adds a tight minimum for *every* accepted certificate, a clause-sensitive exact generator formula, and a minimally UNSAT family connecting the finite checker to the accepted resolution checker. These can serve as expected-value tests and a warning against presenting completeness alone as an efficiency improvement. Removing redundant rows improves the generator by a linear factor on F_n, but cannot eliminate the exponential assignment-coverage cost. Support compression cannot help this family because all n variables occur.

The classical distinction between proof correctness and proof length is developed in Cook and Reckhow, [The relative efficiency of propositional proof systems](https://doi.org/10.2307/2273702), Journal of Symbolic Logic 44(1), 1979, pp. 36-50. Its public extract discusses shortest proofs and relative proof-system efficiency. The present elementary counting application is not attributed to that paper as a specific theorem, and no priority is claimed for the implication chain or its resolution refutation.

No conclusion about P versus NP or NP versus coNP follows. There is no lower bound for resolution on this family; the construction explicitly gives short resolution proofs. The note does not establish a polynomial runtime bound for the particular compiled Lean `decide` implementation, or for rejecting malformed short certificates. Row counts, encoding sizes, and verifier runtime are distinct quantities. The repository's original formal soundness/completeness result is neither invalidated nor reproved here. Prior-art review was limited to the live five-record ledger, the two exact checker artifacts, their submission records, and the linked Cook-Reckhow public extract; this is integration work, not a comprehensive novelty search.
