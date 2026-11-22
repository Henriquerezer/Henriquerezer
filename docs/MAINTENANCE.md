# Maintaining the profile

The README is the editorial source. `scripts/render_readme_cards.py` generates original artwork using Python 3.12+ and system fonts. The hero embeds a reduced copy of Henrique's chosen ASCII-style PNG as a data URI inside the SVG. Source PNGs and ASCII drafts are ignored by Git and remain local. No third-party rendering service or font download is required. `data/contributions.json` contains only dates and counts from GitHub's publicly visible calendar, plus provenance.

To replace the portrait, resize the local source PNG to 560 × 560 pixels and save it as `.preview/portrait-readme.png`, then run the generator. When the source is absent (as in GitHub Actions), the generator reuses the image already embedded in the committed `cards/hero.svg`. Keep that generated SVG in the repository; it is the public portrait artifact. The currently prepared copy is about 460 KB before base64 encoding.

## Rebuild

```sh
python -m unittest discover -s tests -v
python scripts/fetch_github_activity.py
python scripts/render_readme_cards.py
```

For static QA on PowerShell (write to a separate directory so animated assets remain intact):

```powershell
$env:STATIC = '1'
python scripts/render_readme_cards.py --output .preview/static
Remove-Item Env:STATIC
```

On Linux/macOS: `STATIC=1 python scripts/render_readme_cards.py --output .preview/static`.

## Data and failures

The collector requests calendar years separately because GitHub's HTML endpoint returns a calendar year even for some cross-year requests. It then validates a continuous 365-day window ending on the UTC observation date. Monthly values are derived from daily counts; boundary months and today can be partial. The endpoint is public HTML, not a stable API contract. A format change causes a failure, never a fabricated zero. HTTP requests have a timeout, bounded retries and rate-limit handling.

Fetch failures leave the last good file untouched. Both the stored observation date and the displayed date range remain unchanged. No timestamp changes on identical data. Run logs report failures; the daily workflow can render the dated cache. Public activity may include anonymized private counts if enabled by the profile owner; no repository names, events, private API responses or access tokens are stored.

## Automation

`update-readme.yml` runs daily at 09:23 UTC and manually on the default branch only. It uses the standard `GITHUB_TOKEN` provided through checkout credentials to commit only changed generated files. Its job has `contents: write`; other permissions are not granted. Actions are pinned to verified commit SHAs. No personal token is required.

The automation author is `github-actions[bot]`, never Codex. The current local changes have not been committed or pushed. This scheduled publication behavior takes effect only after the owner approves and publishes the workflow. Branch protection may prevent direct updates; in that case adapt the workflow to a reviewed PR process rather than weakening protection.

The former snake workflow remains available manually. Its previous schedule ran every minute during two hours per day, and its push trigger referenced `master`; both automatic triggers were removed because the new README does not use that output. No remote workflow or setting was changed during local preparation.

## Accessibility and previews

The README keeps headings, links and detailed descriptions as native text. SVGs have titles/descriptions and image alt text, system fonts, light/dark variants and short finite CSS animations. `prefers-reduced-motion` removes movement. No JavaScript, SMIL, external requests or looping effects are required. Full-width pillar rows stay readable on narrow layouts.

Generate the local GitHub-width approximation with `python scripts/preview_profile.py`; open `.preview/index.html`. This is not GitHub's sanitizer or Camo pipeline. Before approval to publish, local preview and XML checks are possible; actual GitHub rendering and Actions execution require a subsequent authorized publication. Verify those separately after publication.

## Editorial rules

Keep private audits and backups outside the versioned tree. The owner approved only the limited Formula 1 and medical imaging MCP previews in this README; review any further private project disclosure individually. Never add credentials, medical samples, restricted data or unpublished metrics. Project status is descriptive, not proof of production quality. Verify personal contribution before asserting exclusive authorship. Acceptance of the Healthcom work is owner-reported; replace the status only after verifying the proceedings record or DOI.

Visual approach studied: [Avi Vashishta's SVG README article](https://www.avivashishta.com/blog/github-profile-readme-animated-svg-cards). This implementation and composition are original; no source code, portrait or font files were copied.
