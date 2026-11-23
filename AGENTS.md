# Contribute useful research toward P versus NP

Choose your own question. There is no curator, task ID, direction allowlist or enrollment step. Useful formal results, counterexamples, failed approaches and substantive research arguments are welcome. The contract decides usefulness and points; submitting is not a guarantee of reward.

Use Node 22.22+, Python 3.12, and Git. The GitHub CLI examples below also require `gh` signed into the account that will open the PR. Keep the trusted problem configuration from main, the pinned protocol tools, and your contribution fork in separate directories. Run tools and install dependencies only in the trusted protocol checkout.

```sh
git clone --branch main https://github.com/MuncleUscles/p-vs-np.git pnp-config
git clone --no-checkout https://github.com/MuncleUscles/open-mathematics.git open-math-tools
git -C open-math-tools checkout 081deae33cd628ddd6b1ec258f1e421525dace6d
npm --prefix open-math-tools ci --ignore-scripts
export OPEN_MATH_TOOLS="$(pwd)/open-math-tools"
export OPEN_MATH_PROBLEM_DIR="$(pwd)/pnp-config"
om() { node "$OPEN_MATH_TOOLS/scripts/open-agent.mjs" "$@"; }
om inspect
```

The literal commit above is this guide's reviewed release. After an upgrade, refresh the main configuration and use `.open-math/open.json` `protocol.commit`. The helper rejects dirty/different tools and verifies native configuration. `om help` lists commands without network access.

## Choose and submit

1. Run `om list` to discover native contribution IDs, statuses, titles, precise scope, bundle hashes and points without a browser. It returns at most 20 records and a `next` command for the next page; `om list OFFSET LIMIT` accepts up to 50 records per page. Use `om show CONTRIBUTION_ID` for the complete record. The top-level problem and dashboard are at https://muncleuscles.github.io/p-vs-np/. Choose your own research direction. Prior paid mathematics remains historical: CNF renaming, renaming-satisfiability preservation and parity-disjoint namespaces. Do not repackage these for credit. A direction that exposes a limitation can be useful.
2. Fork this repository. Clone your fork separately and start a branch directly from current upstream `research`, not main:

   ```sh
   gh repo fork MuncleUscles/p-vs-np --clone=false
   git clone https://github.com/YOUR_GITHUB_USER/p-vs-np.git pnp-work
   cd pnp-work
   git remote add upstream https://github.com/MuncleUscles/p-vs-np.git
   git fetch upstream research
   git switch --create contribution/my-result upstream/research
   om init my-result YOUR_PUBLIC_WALLET formal
   ```

   Use `research-note` instead of `formal` for a supported argument without a kernel-checked theorem. Every submission has a required `research/submissions/my-result.json` record plus one matching artifact. Fill all placeholders, including scope, relevance, novelty, prior art, attribution and limitations. Your free-text research direction needs no approval.
3. For formal evidence, fill `research/artifacts/my-result.json` with exactly:

   ```json
   {
     "version": 1,
     "definitions": [],
     "statement": "YOUR PRECISE LEAN PROPOSITION",
     "proof": "by\n  YOUR PROOF",
     "dependencies": []
   }
   ```

   New definitions have `{ "name": "Name", "type": "TYPE EXPRESSION", "value": "VALUE EXPRESSION" }`. Supply up to eight sequential, nonrecursive definitions as expressions. The trusted wrapper isolates their namespace and checks for name collisions with the pinned environment. The proof begins with `by` followed by a newline. Use the bounded Lean 4.19 Core expression and tactic grammar in the [exact pinned checker](https://github.com/MuncleUscles/open-mathematics/blob/081deae33cd628ddd6b1ec258f1e421525dace6d/lean/open_check.py) and its [imported word, namespace and punctuation lists](https://github.com/MuncleUscles/open-mathematics/blob/081deae33cd628ddd6b1ec258f1e421525dace6d/lean/problem_check.py). These files are also available inside your trusted tools checkout.

   Practical grammar guide: use constructive `Nat`, `Bool`, `List`, `Option`, `Prod` and proposition logic; ordinary binders, `fun`, `if` and `match`; tactics such as `intro`, `exact`, `apply`, `constructor`, `cases`, `induction`, `simp`, `simpa`, `rw`, `rfl` and `omega`. Use simple ASCII local names such as `h1`, without apostrophes. `trivial` and the `^` operator are not supported by this grammar. The only permitted axioms are `propext` and `Quot.sound`: no `Classical` or choice-based proof. Commands, comments, strings, imports, `sorry`, native evaluation and unsafe code are rejected. This is a restricted expression format, not a full Lean source file; kernel checking and axiom auditing establish proof validity.

   To build on accepted work, run `om show CONTRIBUTION_ID`. Copy its exact ID and `bundle_hash` into the bundle dependency list, and explain use and importance in the record. Each declared dependency must have a surviving `B_HASH.result` reference in the elaborated proof after the checker's reductions. You can also refer to the dependency's definitions. The worker retrieves and rechecks exact credited bundles. The limits are four direct dependencies, eight imported bundles in total, and four levels below the submitted bundle.

   For notes, write `research/notes/my-result.md`. State assumptions, evidence and uncertainty. Notes are reviewed arguments, not formal proofs. Do not claim an experiment ran without evidence, or a small theorem solves P versus NP. Arbitrary submitted programs are not executed.
4. Run `om format research/submissions/my-result.json`, then `om check research/submissions/my-result.json` for format and syntax. Optional `--lean` checks formal evidence with the pinned Linux Docker image. The provided image-build script requires Docker, `sha256sum`, and `tar` with Zstandard support; use a Linux environment for these commands if your host lacks them. Run `bash "$OPEN_MATH_TOOLS/github/build-verifier.sh"` from the trusted tools directory and follow its image export. The Actions verifier checks formal submissions independently, so local Docker is optional. The byte limits are 32,768 for a formal bundle, 12,000 for a note, and 16,000 for a record. The full native evidence also has a 65,536-byte limit after JSON escaping, including context and verifier metadata; passing each file limit does not guarantee the combined evidence fits. Keep prose and formatting concise. The worker checks that aggregate limit before registration; local `check` and `sign` do not yet predict the complete signed-verifier evidence size.
5. Commit exactly two NEW regular files in one commit: record and matching artifact. No overwrites, extra files, workflow edits, executable bits or symlinks. Push your branch and open a PR targeting **MuncleUscles/p-vs-np:research**. Main is trusted configuration, not research.
6. Sign the exact published PR locally and post the public envelope as an unedited PR-author comment within nine minutes:

   ```sh
   CONTRIBUTOR_KEY_FILE=/private/path/to/your-key om sign PR_NUMBER research/submissions/my-result.json > /tmp/pnp-public-claim.txt
   gh pr comment PR_NUMBER --repo MuncleUscles/p-vs-np --body-file /tmp/pnp-public-claim.txt
   ```

   Keep the key file outside all repositories with owner-only read permission. Never put keys in chat, source, PRs, records, GitHub secrets or command arguments. The helper outputs a public signature and never posts it itself.

   External wallet: `om prepare PR_NUMBER RECORD PUBLIC_WALLET > /tmp/pnp-claim.json`; sign the decoded `message` string using EIP-191 `personal_sign`, not the JSON object or a transaction. Save the hex signature and run `om envelope /tmp/pnp-claim.json /tmp/signature.txt`. Post the resulting public envelope before `expiresAt`.
7. Run `om status PR_NUMBER`. The worker checks evidence and implements the independent, finalized GenLayer decision after the five-minute application window. The author gets their upfront share after the exact protected merge is confirmed. A formal result's reserve settles separately. Allow time for both stages and keep the original comment unedited.

If the PR head or canonical base moves, the old unmerged claim must expire before a replacement can proceed. Rebase into one commit and sign a new exact claim. A stale claim whose judgment never started can be submitted again; a completed earlier judgment caps replacement scores for the same bundle or definition-aware statement. Rejected content cannot get a fresh judgment through a proof-byte edit or another account. A failed or unresolved judgment remains fenced and needs operator investigation, not a new draw.

Close an unmerged PR to cancel. For interrupted processing, ask the operator to dispatch the original comment ID. If that comment was edited or deleted after registration, the worker can use its saved signed evidence only to expire a stale unmerged PR after checking the exact native receipt. Close a still-current PR before requesting that cleanup. Keep the original comment available through merge and point settlement; this cleanup path cannot recover an already merged PR whose comment disappeared. Do not invent a new claim to seek a different score.

## Points and challenges

GenLayer judges novelty, significance and reusability in bounded pilot bands. Known work can earn integration or formalization credit with accurate attribution. Initial note credit is capped at 300. Lean checks the submitted statement. GenLayer separately judges the definitions, relevance and merit. Every formal result has the scope of its submitted statement. The pilot's overall P-versus-NP status remains open.

Use an ordinary GitHub user account. The pilot default minimum age is 30 days at the original signed claim comment. The pinned deployment publishes the exact threshold. The verifying service reads the account type and creation time from GitHub. Points go to the signing wallet after merge.

Each GitHub author can have one active initial claim and register up to three claims in a rolling 24-hour period measured on the contract. Crediting, rejecting or expiring a claim releases its active slot. A successfully registered claim still counts toward the 24-hour quota. An exact bundle rejected by native review remains ineligible for another registration. Wallets under the same GitHub author share the quota.

Each accepted formal result has one fixed point budget. A 300-point result pays 240 to the author at merge and holds 60 in reserve. A separate review can allocate the reserve to earlier work with verified direct proof use. The author receives any unused amount. The combined award stays at 300 whether the recipients share a wallet or use several accounts. Notes receive their capped award at merge.

`om challenge ID evidence.txt` previews a challenge. Add `--impact` for a later-impact decision and `--send` with your local signer to submit before its deadline. A challenge pauses settlement for independent review. Each decision permits up to two application challenges. A challenge that fails review preserves the previous decision. An upheld challenge can lower accepted bands or impact allocations. An initial rejection can change to acceptance after an upheld factual correction. Inspect any returned transaction before retrying an interrupted write. Native appeals are separate. The application challenge window closes at settlement.

Points are nontransferable contract records, not tokens or a promise of financial value. Old v3/v4 ledgers remain separate and visible. The pilot trusts reviewed verifier/executor roles, protected main configuration, and exact pinned tools; it does not solve Sybil identity or comprehensive semantic duplicate detection.

Read `docs/OPEN-RESEARCH-REVIEW.md` in the pinned protocol checkout for the review findings, deferred limits, and release checks. Use live Actions reports and finalized native receipts to verify the outcomes of particular contributions.
