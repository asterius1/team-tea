# Void Council — GW2 April Fools Recruitment Page

Recruiting page for the **Void Council** (tea faction) in the Guild Wars 2 April Fools 2026 competition.

Live at: https://asterius1.github.io/team-tea/

## What it does

- Randomly loads in **Prestige mode** (dark, dramatic propaganda poster) or **Chaos mode** (unhinged Comic Sans rainbow fever dream) — 50/50 on each visit
- Button in the bottom-right corner to swap between modes
- Links to a Discord message where people react with the Void Council shield emoji to sign up
- Konami code easter egg (↑↑↓↓←→←→BA)

## Stack

Pure HTML/CSS/JS. Single file. No build step, no dependencies, no framework.

## Editing

Everything is in `index.html`. Key things to update:

- **Discord link** — search for `discord.com/channels`
- **Event description / requirements** — the `.p-lore` and `.p-requirements` sections (prestige), `.c-lore` and `.c-requirements` (chaos)
- **Year in top banner** — search for `April Fools 2026`

## Hosting

Deployed via GitHub Pages from the `main` branch.
