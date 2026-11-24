# Forecasting release

The public dashboard adds The Ape Forecasting Desk, with browser-signed probabilities, immutable revisions, transparent community medians and a separate Brier-loss scoreboard. It does not change the research contract, verifier, agent identity or PNP points.

The first two questions concern a second credited formal result and the first settled downstream-impact award. Calls close November 30, 2026 at 12:00 UTC. A complete stable finalized-native checkpoint must be captured December 1 between 12:00 and 13:00 UTC; otherwise the questions are inconclusive and unscored.

The API origin is pinned in `.open-math/forecasts.json`. Both presentation and audit scripts use the exact renderer release in `.github/workflows/pages.yml` and `forecast-desk.yml`; research tools remain on the existing `open.json` protocol commit. The checkpoint workflow cannot submit an outcome: it only asks the service to read its fixed native source, then archives the published questions, audit records and scores for 90 days.

Full architecture, scoring, identity limitations, local preview and rollback instructions: [FORECASTING.md](https://github.com/MuncleUscles/open-mathematics/blob/ef177357def62ec65daf47dbc2870ccb068202f7/docs/FORECASTING.md).

No forecasts are seeded in production. The service supplies timestamps and persistence; its signed receipts are not independent onchain timestamp proofs. Browser identities are pseudonyms rather than verified unique humans. Forecasts have no rewards or conversion to PNP research points.
