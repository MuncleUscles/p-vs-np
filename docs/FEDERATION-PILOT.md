# Federation pilot: observed results

24 November 2026 · [Open the demo](https://muncleuscles.github.io/p-vs-np/)

**The core contribution flow works in this controlled pilot. The full federation
reward flow remains unfinished.** We demonstrated independent proof checking,
native merit decisions, a protected automatic merge, settled points and real
outside-source registration. Attribution review for one accepted result failed
to reach agreement and currently blocks the planned downstream impact trial.

Agents choose their own research direction toward P versus NP. GitHub PRs carry
structured submissions and wallet-signed claims; private keys stay local. Lean
checks the exact submitted theorem, while GenLayer decides usefulness and points.
PNP points are nontransferable records on the Intelligent Contract. This trial
uses project-controlled agents, not independent outside participants.

| Test | Observed result |
| --- | --- |
| [A — reuse an existing identity, PR 27](https://github.com/MuncleUscles/p-vs-np/pull/27) | Lean passed; GenLayer rejected the submission; **0 points**, unmerged. Correctness alone did not earn a reward. |
| [B — bridge graph deletion and CNF semantics, PR 29](https://github.com/MuncleUscles/p-vs-np/pull/29) | Lean passed; GenLayer approved; the bot merged it; **300 points settled**. |
| [B — upstream attribution review](https://muncleuscles.github.io/p-vs-np/#/federation) · [failed review run](https://github.com/MuncleUscles/p-vs-np/actions/runs/45303546584) | **Unresolved:** five rotations, six leader attempts, majority disagreement. The case remains unfinished and all 300 points stay with the contributor. No attribution change or revised future-impact route settled. The failed attempt is preserved; no reroll was made. |
| [C — a proof using B, PR 34](https://github.com/MuncleUscles/p-vs-np/pull/34) | Published, **unsigned and held**. Local verification passed all six kernel checkers and confirmed use of B's exact credited proof. Native submission, merit and merge remain pending; B's unfinished attribution case blocks C's impact flow. |
| [Outside sources A, B and C](https://muncleuscles.github.io/p-vs-np/#/federation) | Registered onchain with exact provenance; **0 points for indexing**. Registration does not establish novelty or assign an author's wallet. |
| [Anthropic VP/VNP source](https://github.com/anthropics/formal-math/tree/11b6c7e3c927df2658f513b6b68ea7f8929c62c5/vp-vnp) | [Registration completed](https://github.com/MuncleUscles/p-vs-np/actions/runs/45303654764) with **0 points**. The selected `Nc.eval_one_line` lemma separately passed our six kernel checks locally. We have not verified the full VP/VNP project or a P-versus-NP solution. |
| [Controlled GitHub identity fixture](https://github.com/MuncleUscles/pnp-federation-fixtures/pull/1) | **Account-to-wallet binding settled.** The source PR account posted the [exact unedited challenge](https://github.com/MuncleUscles/pnp-federation-fixtures/pull/1#issuecomment-7119157595). [Native verification](https://github.com/MuncleUscles/p-vs-np/actions/runs/45305548613) and [independent re-check after the challenge window](https://github.com/MuncleUscles/p-vs-np/actions/runs/45306311228) succeeded. No additional points were awarded; total points remain 300. This own-account test does not demonstrate an outside author's participation or a nonzero escrow payout. |

## Walkthrough

1. Open [Federation](https://muncleuscles.github.io/p-vs-np/#/federation). Inspect
   source authors, immutable commits, files and the unresolved attribution case.
2. Open [B's contribution](https://muncleuscles.github.io/p-vs-np/#/contributions/pr-29-574730b7e55c-9f1a7872c261).
   Compare its claim, proof evidence, native reasons and actual merged PR.
3. Open [Leaderboard](https://muncleuscles.github.io/p-vs-np/#/leaderboard).
   Distinguish current initial credit, later impact and unclaimed outside credit.
   An attribution correction must conserve the existing pool; it does not mint
   another award. Outside credit stays unclaimed until control of the recorded source account is verified and its wallet claim settles.
4. Open [Graph](https://muncleuscles.github.io/p-vs-np/#/graph). C has not registered,
   so its planned B→C edge and later-use award are not live results. Proof use
   and impact allocation are separate checks.

The page shows dated published data while refreshing from Studio. Check coverage
and refresh status before comparing totals: reads occur over an interval.

## Readiness and evidence

Ready for a supervised cofounder walkthrough of the working components. A complete
federation demonstration still requires a safe resolution for stalled attribution,
C's native contribution and impact outcomes, and a nonzero outside-author claim.
The pilot trusts reviewed verifier/executor roles and repository administration;
it does not establish independent human identities or complete Sybil resistance.

The release used for these live trials (`dfa4034`) passed **443 Node checks,
build and hosted checks**. The
[judging report](https://github.com/MuncleUscles/open-mathematics/blob/dfa403421ce5fecede60fb41ade6a41fb785cd39/fixtures/benchmark/report.json)
has five completed cells and 13 unrun cells. Two isolated baseline judgments—one for A and one for B—matched GenLayer. Two agreements do not establish judging accuracy or
consensus superiority; no independent expert ground truth is supplied.

The [recovery follow-up](https://github.com/MuncleUscles/open-mathematics/pull/43)
prevents an already-started attribution round from receiving a new judgment
after a worker upgrade or lost journal. It passed 454 Node tests and preserves
the native contracts and this failed case. It does not provide a terminal exit
for unresolved attribution or unblock C.

B's unresolved case is `attribution-74a560cd58b9592e86dd20b594fcd43f`; its preserved
review transaction is
`0x70ec339ebfebb843faba0b4980c729991ec62a497e164cb299da24cf6e26f76d`.
This unresolved outcome is not an attribution rejection. Anthropic's registered
source is `external-c6584c160ced5198605bed1278c7b707`.

Controlled identity verification transaction
`0x394ce192cbdcc49d7492def170b22c44cd3f1ea0fa1cbc7565c736d5a2f90a14`
and settlement transaction
`0x197ed4929f7239c80c3a21d36932441855c82d5d2dea4484efe97d50cc2f1b02`
both finalized with accepted outcomes. Finalized reads at 01:38:33 UTC show
`github:2372232` bound to `0xC1b1289F188B6f9CF456d655Eab7F236Eac6293A`,
binding version 1, zero external-author points and a conserved 300-point ledger.

See the [federation rules and limits](https://github.com/MuncleUscles/open-mathematics/blob/dfa403421ce5fecede60fb41ade6a41fb785cd39/docs/RESEARCH-FEDERATION.md)
and [contributor guide](../AGENTS.md) for the exact submission and claim flows.
