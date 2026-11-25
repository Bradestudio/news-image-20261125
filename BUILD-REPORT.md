# Build Report — news-image-20261125

Entry rewritten from scratch (round-1 fix): `main.py`, `gen_image.py`,
`README.md`, `LICENSE`, and this report were all written fresh in this
session. No file from any earlier round was read or copied.

## The entry

- **Bounty:** news-image-20261125 (make.fun, account bradestudio)
- **Format:** one-page newspaper front page, 1024x1024, cream paper,
  black ink, red accent — "THE WORLD IN ONE DAY, Wednesday 25 November 2026".

## Story count: 40

- **Heroes 1–3:** Ukraine drones hit a Russian cargo ship in the Gulf of
  Finland; Houthi drone hits Riyadh's tallest tower, 11 hurt; Trump gives
  the Medal of Freedom to Rudy Giuliani.
- **Briefs 4–12 (with thumbnails):** Putin retaliation "inevitable";
  Houthis 60 km from Aden; turkey pardons "Freedom" and "Feathers";
  Sarkozy trial (hearing 1 Apr 2027); Huawei trade-secret verdict;
  CIA/ODNI breach; Anthropic below IPO $83 (~$200bn wiped out);
  NATO AWACS in Poland; three tankers mined in the Strait of Hormuz
  (marked CLAIM — IRGC account).
- **Map pins 1–12:** dot-matrix world map, 12 numbered pins.
- **List 13–40:** Nepal quake 5.6; BJP–Akali Dal reunion; England's
  8-wicket T20I win chasing 185; Int'l Day to End Violence Against Women;
  Dell; Gaza; EU sanctions; Iraq/Kurdish oil fields; Trump tariffs;
  Nepal PM's India visit; Fort Hood delay; Libya + the Sunday sinking;
  O'Hare radar outage; GTA 6; Sooryavanshi; NZ–India Test; Sweden;
  Black Sea shipping; oil prices; Asian stocks (Sensex -1,484);
  India A vs Sri Lanka A; Sheikh Khaled; Ras Al Khaimah crash;
  Houthi casualties; Venezuela debt $237.5bn; Man Utd/Yoro;
  Fort Hood hearing; closing line.
- **Timeline:** 6 moments in UTC (02:00–20:00).
- **By the numbers:** 11 / 60 km / 5.6 / ~$200bn / 8 wkt / 185 / 3 / 1 Apr '27.
- **Date check (footer):** the Libya sinking happened on Sunday;
  the Sarkozy hearing date (1 Apr 2027) is a future date; the Nepal PM's
  India visit was 22–23 Nov, included as context.

## Verification (run before push)

- `gen_image.py` run twice: byte-identical output.
- `entry.png` sha256:
  `22ee2f5de09918a2c84c88f53b7a3d5f069604d2e9aef7abaf5dd3f9ca28546d`
- `entry.png` size: 145,825 bytes (< 1 MiB), 1024x1024, RGB.
- Sandbox (`python3 -P -s main.py /tmp/out-test` in a clean dir with only
  `main.py` + `entry.png`): exit 0, output byte-identical.
- `MAKEFUN_OUTPUT_DIR` run: exit 0, output byte-identical.
- Visual check: masthead clean, all 3 hero captions legible, timeline
  labels clear, all 8 numbers readable, 9 briefs + badges legible,
  12 map pins labelled without overlap, list 13–40 complete, footer
  date check present. Two defects found and fixed during the visual
  check: smoke puffs drawn over the masthead (coordinate bug) and
  colliding map labels (pins re-spread).
- `main.py`: stdlib only, no Pillow, no local imports, no fonts,
  no network. `gen_image.py`: Pillow + local DejaVu only, no network,
  no clock, no randomness.
