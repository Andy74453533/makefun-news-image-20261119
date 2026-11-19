[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Andy74453533/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Andy74453533/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Built for the [make.fun bounty: Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

# The World Today — 19 November 2026

Entry for `news-image-20261119`: a program that writes one 1024×1024 PNG
summarising the world's news of Thursday 19 November 2026 to
`/output/entry.png`. Standard library plus Pillow for rendering (with a
pre-rendered fallback), offline, deterministic — two runs write
byte-identical files.

## The image

A newspaper front page, "THE WORLD TODAY", dated Thursday, 19 November
2026. Everything is drawn programmatically — no downloaded photos, no
network at run time:

- **Lead story — Trilateral summit in Shenzhen:** Trump, Xi and Putin
  meet for the first-ever three-way summit; Xi hugged Trump on the
  tarmac as he arrived. APEC opens in Shenzhen. Illustrated with the
  three flags (China, Russia, United States) drawn from code.
- **Anthropic's $81.3bn IPO is the biggest ever** — the Claude maker
  prices at $83 a share; shares debut on Nasdaq today under ANT, valued
  near $1.5 trillion.
- **Grand Theft Auto VI rolls out worldwide** — after a 13-year wait,
  gamers enter Vice City.
- **Israel launches a rare ground operation in Gaza** — tanks cross the
  ceasefire's Yellow Line in central Gaza; displaced families flee.
- **Democrats nominate Jeffries for Speaker** — Hakeem Jeffries, 56,
  picked as House Democrats' leader; he would be the first Black
  Speaker after the formal House vote on 3 January.
- **Also:** Crimea bridge hit again; EU proposes a €45bn Ukraine loan;
  Myanmar faces an ICJ genocide verdict; Cyclone Akvan nears India; a
  Van Gogh sells for a record $190.4m. Plus a markets strip (S&P 500
  −0.23%, Nasdaq +0.42%, Brent $91.95, gold $3,742, VIX 24.49 — 18 Nov
  close).

Story selection: the five most widely reported developments of the day
across the major briefings (see SOURCES.md), chosen to be recognisable
to a picture editor judging the image on its own — each story is
self-contained, with a headline and a one-line summary, so the image
needs no news feed to be understood.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

Deterministic and offline: no network, no randomness, no clock.
Two runs produce byte-identical output.
