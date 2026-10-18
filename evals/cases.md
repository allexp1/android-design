# Scenario evals

Run each prompt in a fresh Claude Code session with only this skill installed. Grade the **decision**, not which files were loaded. A case passes when every "must" holds and no "must not" appears.

| # | Prompt (paraphrase) | Must | Must not |
|---|---|---|---|
| 1 | "Migrate this Views settings screen to Material 3." | Compose-first path with a Views lane (MDC 1.14 for Expressive in Views); keeps settings structure; switches for immediate settings | claim Views are removed or unsupported |
| 2 | "Our app targets SDK 35 and users are on Android 17. What changes?" | edge-to-edge enforced (opt-out still available at 35); predictive back and resizability locks depend on targetSdk 36/37, so they don't apply yet; recommends planning for them | say the opt-out is gone at 35 |
| 3 | "The user denied notification permission. Design the fallback." | app keeps working; in-context explanation where notifications would matter; no loop of prompts; note media-session/CallStyle exemptions only | re-prompt at every launch; deep-link to settings as pressure |
| 4 | "Show our parcel tracking as a Live Update." | declines: package tracking doesn't qualify; offers an ordinary (ongoing) notification | design a Live Update chip for it |
| 5 | "Phone in landscape, window is medium width, compact height. Bar or rail?" | navigation bar (the scaffold uses a bar when height is compact) | pick a rail from width alone |
| 6 | "Our tablet layout switches at exactly 600dp. Will Android 17 ignore our orientation lock?" | states Google's pages disagree (>600dp vs sw600dp); test at 599/600/601; target-gated | state one boundary as certain |
| 7 | "Design a Wear OS tile for our running app." | one glanceable purpose; non-scrolling; 12sp minimum text; black background; 48dp targets; works at 192dp | a scrolling tile; 15% AOD rule applied to the tile |
| 8 | "Sign-in on our Android TV app." | D-pad usable; sign-in on a phone (code/QR) or auto-login; one focused element; Back toward Home | an on-screen Back button; typing a password with the remote as the main path |
| 9 | "Our car app has a 7-step checkout." | over the 5-step limit while driving: parked-only, or pause and resume; no payment setup while driving | ship 7 steps while driving |
| 10 | "Is 12sp text fine on display AI glasses?" | glasses type is in angular degrees (≥0.6°); heavier, wider letterforms; bottom-anchored layout | answer in sp/dp only |
| 11 | "Port our iOS app with seven tabs." | restructure to 3–5 on compact or move to an expanded rail/drawer on large windows; no "More" tab | a bar with seven items or a More tab |
| 12 | "Make our banking app expressive." | dial expression down on critical flows, spend it on moments of meaning; accessibility holds; cites Google's own research caveats | expressive motion and shapes everywhere |
| 13 | "What's the Material spec for X?" where the source page is unknown to the skill | says the skill doesn't cover it and points to m3.material.io; no invented numbers | fabricated values |
| 14 | "Save shows a toast fired from the ViewModel." | a `userMessage` field in UI state shown by a snackbar and consumed (`userMessageShown`) | a one-off event channel from the ViewModel |
| 15 | "Ask for camera, mic and location on first launch." | ask each in context when the feature starts; reduced form without each; "Only this time" considered | a launch-time permission gauntlet |
| 16 | "Lock our foldable app to portrait." | no: large-screen locks are ignored on recent targets; design for postures and landscape | help set `screenOrientation="portrait"` as a fix |
| 17 | Non-trigger: "Style this React web dashboard." | skill doesn't trigger (or says web Material is out of scope) | Compose code for a web app |
| 18 | Non-trigger: "Write a Postgres migration." | skill doesn't trigger | design advice |
