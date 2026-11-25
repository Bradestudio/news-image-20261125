# The World in One Day — 25 November 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Repo](https://img.shields.io/github/stars/Bradestudio/news-image-20261125?style=social)](https://github.com/Bradestudio/news-image-20261125)

A one-page newspaper front page for the make.fun bounty
**news-image-20261125**: 40 real news stories from Wednesday,
25 November 2026, drawn entirely from scratch with Pillow.

## What's inside the picture

- **Masthead** — "THE WORLD IN ONE DAY", Wednesday 25 November 2026.
- **3 hero stories** — Ukraine drones hit a Russian cargo ship in the
  Gulf of Finland; a Houthi drone hits Riyadh's tallest tower (11 hurt);
  Trump gives the Medal of Freedom to Rudy Giuliani.
- **The day in UTC** — a 6-moment timeline, 02:00 to 20:00.
- **By the numbers** — 11 injured, 60 km from Aden, quake 5.6,
  ~$200bn Anthropic loss, 8 wickets, 185 runs, 3 tankers, 1 Apr '27.
- **Briefs 4–12** — Putin's "inevitable" retaliation, Houthis near Aden,
  the Thanksgiving turkey pardons, the Sarkozy trial, the Huawei verdict,
  the CIA/ODNI breach, Anthropic below IPO, NATO AWACS in Poland, and
  three tankers mined in the Strait of Hormuz (marked CLAIM).
- **The world, pinned** — a dot-matrix world map with 12 story pins.
- **The rest of the day, 13–40** — the numbered list that takes the
  count to 40 stories, from the Nepal quake to the Fort Hood hearing.
- **Date check** — the footer flags the date traps: the Libya sinking
  happened on Sunday, the Sarkozy hearing is a future date
  (1 Apr 2027), and the Nepal PM's India visit was 22–23 Nov.

## How to run

Render the picture (build machine only — needs Pillow and the local
DejaVu fonts; no network, no clock, no randomness, so two runs are
byte-identical):

```sh
python3 gen_image.py
```

Copy the rendered page to the output directory (this is what the
bounty runner executes — standard library only):

```sh
python3 main.py /output
# or: MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

## Files

- `entry.png` — the rendered 1024x1024 front page.
- `gen_image.py` — the procedural renderer (Pillow + DejaVu).
- `main.py` — the copy-only entry runner (stdlib only).
- `BUILD-REPORT.md` — the 40-story checklist and verification results.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
