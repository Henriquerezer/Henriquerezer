# Profile design and implementation plan

The profile should make Henrique's research, software and data work understandable within one screen. Professional background comes from the owner; project descriptions come from public source inspection. No private project information belongs here.

## Directions

**A — Research Editorial (selected technical recommendation):** warm neutral surfaces, ink typography, blue accents and generous spacing. An original abstract image-to-model-to-evidence motif connects the three pillars. Best balance of academic identity, legibility and restrained motion. Light and dark SVG variants selected with GitHub-compatible picture elements.

**B — AI Engineering Lab:** deep navy, subtle cyan and a system diagram composition. Strong engineering signal, but more visually dominant and less balanced against scientific writing. Kept as an alternative, not a second duplicated README.

## Editorial structure

Hero: “Medical AI research. Applied AI engineering.” Name and PhD context in native text as well as artwork. Three short linked pillar cards. Four public project links with honest maturity labels. Research section distinguishes author-reported acceptance from publication. A compact evidence-based stack, a Portuguese summary, and activity below the work.

No clinical validation claims, inflated performance, private project names, visitor counters or decorative technology badges. Research details requiring further clearance stay out. Contact links reuse the existing public profile.

## Implementation plan

- [ ] Preserve original files externally; use a local working branch; do not commit or publish.
- [ ] Write the main README, with four public exploratory projects and no unsupported metrics.
- [ ] Implement Python standard-library activity collection from GitHub's public calendar. Reject missing, malformed, duplicate and incomplete dates; do not substitute zero for unknown counts. Public calendar aggregates may include anonymized private activity if the owner enabled it; never infer private repositories.
- [ ] Keep the last valid snapshot on fetch failures, with its observation date visible. Write only changed bytes. No PAT required; GITHUB_TOKEN is scoped only to updating generated files in the workflow.
- [ ] Generate six SVG components in light/dark variants, with short one-shot CSS animation, reduced-motion handling, XML escaping and STATIC=1. No external assets or fonts.
- [ ] Preserve the previous snake workflow, correcting its schedule and leaving it manual-only because the new README replaces that graphic. Add daily generation with minimum permissions and no-change commit guard.
- [ ] Test parsing failures, stale cache preservation, real month aggregation, XML, static/reduced-motion behavior and determinism. Inspect a local GitHub-width preview at desktop and mobile sizes.

## Validation limits

Local rendering is not a GitHub production test. A final GitHub/Camo rendering check requires the owner to approve publication of the branch. Workflow execution is likewise pending publication. The proposed implementation must report these limits, not claim an unpublished README was tested live.

## Decisions

Use native Markdown for detailed text and links; image content stays short. Pillar cards use full-width rows to remain readable on phones. Use system fonts, avoiding font licensing and embedded payloads. Use CSS only for finite decorative motion; SMIL is unnecessary and makes reduced-motion harder. Keep the GitHub calendar's true date window and mark boundary months as partial.
