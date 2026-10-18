# android-design

**An [Agent Skill](https://www.anthropic.com/news/skills) that teaches Claude Google's Android design guidance and Material 3 Expressive, the reasoning beneath them, and a method for applying them to native Android apps.**

**Version 1.0.0** · current to **Android 17** (API 37) and Compose Material 3 1.4 / 1.5 beta, October 2026 · [Changelog](CHANGELOG.md)

```bash
npx android-design
```

The companion of [apple-hig](https://github.com/allexp1/apple-hig) for Android.

---

## What it does

- **Designs and reviews native Android UI** in Jetpack Compose (first) or Views, for phones, tablets, foldables, desktop windows, Wear OS, TV, cars, XR and AI glasses, and widgets.
- **Starts from a method, not a rulebook:** intake (surface, targetSdk, window, input, abilities), constraints, alternatives, a decision, failure states, validation.
- **Knows which rules the platform enforces** and from which targetSdk: edge-to-edge, predictive back, large-screen resizability.
- **Treats expression as a dial:** Material 3 Expressive where it helps, restraint where the task is critical or dense, accessibility at every setting.
- **Ports iOS designs as decisions**, with conditions and a test for each, not one-to-one swaps.
- **States conflicts between Google's own pages** instead of picking one silently.

## What's inside

```
android-design/
├── SKILL.md              # router: scope, routing, principles, quick rules, checklist, verify
├── references/
│   ├── applying.md       # the method and worked examples
│   ├── philosophy.md     # Google's stated values vs this skill's synthesis
│   ├── psychology.md     # heuristics that change a decision, with their limits
│   ├── foundations.md    # color, dynamic color, type, shape, motion, elevation, icons
│   ├── expressive.md     # Material 3 Expressive and the expression dial
│   ├── adaptive.md       # window size classes, navigation, panes, enforcement, back, foldables, desktop
│   ├── components.md     # Material 3 components with iOS equivalents
│   ├── patterns.md       # navigation, settings, sign-in, permissions, notifications, Live Updates, states, copy
│   ├── accessibility.md  # acceptance criteria and testing
│   ├── quality.md        # core and adaptive quality, Android vitals, startup
│   ├── architecture.md   # the state and event contract that makes a design implementable
│   ├── from-ios.md       # iOS-to-Android decision table
│   ├── wear.md · tv.md · cars.md · xr-glasses.md · widgets.md
│   ├── versions.md       # platform and library matrix
│   └── glossary.md
└── .living/              # facts that change between releases (living-skills/1.1)
```

## Install

```bash
npx android-design            # installs to ~/.claude/skills/android-design
./install.sh                  # from a clone
```

## Design kits and samples (Google)

- Android UI kit (Figma): https://www.figma.com/community/file/1237551184114564748
- Material 3 design kit (Figma): https://www.figma.com/community/file/1035203688168086460
- Widget canonical layouts (Figma): https://www.figma.com/community/file/1478519017421157788
- Material Theme Builder: https://material-foundation.github.io/material-theme-builder/
- Now in Android: https://github.com/android/nowinandroid · Compose samples: https://github.com/android/compose-samples

## Keeping it current

Facts that change faster than releases (OS and library versions, new guidance) live in `android-design/.living/KNOWLEDGE.md`, refreshed from the sources in `.living/sources.md` with every change logged. The original `SKILL.md` is never edited by a refresh.

## License

MIT for this skill's own text and code (see [LICENSE](LICENSE)). Android, Material Design, Google Play and related names are trademarks of Google LLC. This is an independent reference, not affiliated with or endorsed by Google; see [NOTICE](NOTICE).
