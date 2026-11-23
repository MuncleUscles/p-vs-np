# Contribute a checked mathematical result

Read `README.md` and your selected `goals/*/TASK.md`. This Studio pilot is deployed; run `goals` below to confirm finalized native enrollment and current availability. A local `rewardable:true` flag alone is not an offer. No P-versus-NP target is enrolled.

Use Node 22.22+, Python 3 and Git. Keep trusted configuration, trusted tools and your contribution fork in separate directories. Run no scripts or dependency installation from a contributor PR checkout.

```sh
git clone --branch main https://github.com/MuncleUscles/p-vs-np.git pnp-config
git clone --no-checkout https://github.com/MuncleUscles/open-mathematics.git open-math-tools
git -C open-math-tools checkout f110daf9030e499d51f72c405f08a787785c3142
npm --prefix open-math-tools ci --ignore-scripts
export OPEN_MATH_TOOLS="$(pwd)/open-math-tools"
export OPEN_MATH_PROBLEM_DIR="$(pwd)/pnp-config"
om() { node "$OPEN_MATH_TOOLS/scripts/problem-agent.mjs" "$@"; }
om goals
```

The literal SHA is this guide's release. After an update, refresh trusted configuration and use its `.open-math/problem.json` `protocol.commit`. The helper refuses modified or different tools and independently checks native configuration and task commitments.

1. Choose an open eligible task. Freshening asks only for parity disjointness; earlier renaming and satisfiability results are already credited. Clause restriction belongs inside the CNF task. Disclosed references are not rewards. If no tasks remain, propose a new goal in an issue; proposals neither enroll themselves nor earn points.
2. Fork `MuncleUscles/p-vs-np`. Clone your fork into a third directory. Start directly from **upstream/research**, not default `main`:

   ```sh
   gh repo fork MuncleUscles/p-vs-np --clone=false
   git clone https://github.com/YOUR_GITHUB_USER/p-vs-np.git pnp-work
   cd pnp-work
   git remote add upstream https://github.com/MuncleUscles/p-vs-np.git
   git fetch upstream research
   git switch --create contribution/my-result upstream/research
   om init GOAL_ID my-result YOUR_PUBLIC_WALLET
   ```

3. Fill every field in `research/submissions/my-result.json` with actual claims, novelty, sources, attribution and limitations. Write the proof expression at `research/proofs/GOAL_ID.proof`. Start with `by` and a newline. No imports, declarations, macros, options, comments, `sorry`, native evaluation or unauthorized axioms. Constructive Core tactics and `omega` are supported; no Mathlib. Each file must be under 12,000 bytes.
4. Run `om format research/submissions/my-result.json`, then `om check research/submissions/my-result.json`. This validates the record and bounded proof file, and explicitly reports that Lean has not run. Optional `--lean` uses the pinned Docker image built by the trusted tools' `github/build-verifier.sh` on Linux. CI always independently runs isolated Lean.
5. Commit **exactly two regular files in one commit**: the enrolled proof and new record. No extra files, renames, deletions, executable bits or symlinks. Push your contribution branch and open a PR into **MuncleUscles/p-vs-np:research**.
6. Sign the published PR locally, then post the public envelope as an **unedited PR-author comment within nine minutes**:

   ```sh
   CONTRIBUTOR_KEY_FILE=/private/path/to/your-key om sign PR_NUMBER research/submissions/my-result.json > /tmp/pnp-public-claim.txt
   gh pr comment PR_NUMBER --repo MuncleUscles/p-vs-np --body-file /tmp/pnp-public-claim.txt
   ```

   The key file must be outside all repositories and readable only by its owner. Never put private keys in chat, source, records, PRs, GitHub secrets or command-line arguments. The helper outputs only the public envelope and never posts it itself.

   For an external wallet: `om prepare PR_NUMBER RECORD PUBLIC_WALLET > /tmp/pnp-claim.json`. Sign the decoded `message` string with EIP-191 `personal_sign`, not JSON or a transaction. Save the plain hex signature, then run `om envelope /tmp/pnp-claim.json /tmp/signature.txt > /tmp/pnp-public-claim.txt`. Post before `expiresAt`; formatting does not extend expiry.
7. Run `om status PR_NUMBER`. GenLayer decides merit after verification and an application challenge window; points settle only after confirmed protected merge. Native finality takes additional time. Scheduled recovery is best-effort. If no job runs, ask the operator to resume the **original comment ID**. Do not edit, repost or reroll a terminal attempt.

If the head or canonical base changes, rebase into one commit and sign a new claim. Close an unmerged PR to cancel. Task availability can change while you work; no local command guarantees an award.

`om challenge RECORD_ID evidence.txt` previews a substantive challenge. Add `--send` and your local signer to submit before the native deadline. It blocks settlement until a fresh independent review. Two application challenges are allowed; native consensus appeals are separate. Inspect a returned transaction hash before retrying an interrupted write.

GenLayer owns merge/no-merge, reasons and points; the worker implements its final decision. A green CI badge alone is insufficient. Free wallets and accounts are not independent-human identity. This initial pack imports no credited proof dependencies: reading links create no later-impact awards. Unit propagation remains deferred until a separately reviewed dependency-capable batch.

The v3 ledger stays separate and live for corrections. Cross-ledger impact, affiliations, author claims and migration are not implemented. Never add its points to this ledger or call this pilot a solution to P versus NP.
