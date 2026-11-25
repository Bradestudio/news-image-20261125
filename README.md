# Bradestudio-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Bradestudio/Bradestudio-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Bradestudio/Bradestudio-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One picture that sums up Wednesday 25 November 2026: Ukrainian drones hit a Russian cargo ship in the Gulf of Finland, a Houthi drone strikes Riyadh's tallest tower injuring 11, and Trump gives the Medal of Freedom to Rudy Giuliani — 40 verified stories on a single 1024×1024 front page.

## What is inside

- **3 illustrated hero panels** — the burning cargo ship in the Gulf of Finland at night, the Riyadh tower with its great arch under a drone strike, the Medal of Freedom ceremony at the White House — each drawn from scratch with Pillow shapes.
- **A "THE DAY IN UTC" timeline** — six moments of the day, times marked approximate.
- **A "BY THE NUMBERS" strip** — 11 injured in Riyadh, 60 km from Aden, a 5.6 quake in Nepal, ~$200bn lost by Anthropic, 8 wickets, 185 runs chased, 3 tankers mined, 1 Apr '27.
- **9 briefs with drawn thumbnails** — Putin's "inevitable" retaliation, the Houthi advance on Aden, the pardoned Thanksgiving turkeys, the Sarkozy trial, the Huawei verdict, the CIA/ODNI breach, Anthropic below its IPO price, NATO's AWACS in Poland, the Hormuz tanker mines — each tagged REPORTED or CLAIM.
- **A dot-matrix world map** with 12 numbered pins for stories 1–12, each label hand-placed with a leader line so the crowded US and Middle East clusters stay readable.
- **28 more stories** in a numbered list, from the Nepal quake to the Thanksgiving turkeys' names.
- **A DATE CHECK footer** — the Merkury sinking off Libya happened on Sunday and is reported again today, not as new; the Sarkozy hearing date (1 Apr 2027) is a future date; Nepal PM Shah's India visit was 22–23 Nov and is included as context. With a certainty legend and the source line.

See [BUILD-REPORT.md](BUILD-REPORT.md) for the full list of 40 stories, their sources, and what changed vs the 24 November entry.

## How to run it

```sh
python3 gen_image.py   # redraw entry.png from scratch (Pillow only)
python3 main.py        # draw entry.png into the output directory
```

`main.py` writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`, or to the directory passed as its first argument, or to `./output`. Run either script twice and the bytes come out identical — no network, no clock, no randomness anywhere.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qjs4e9sj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
