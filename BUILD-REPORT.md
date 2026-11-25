# BUILD-REPORT.md — news-image-20261125

Bounty: **news-image-20261125** — "Sum up 25 November's world news in one image",
$100 prize (top 50 paid, 1st $20), deadline 27 Nov 2026 07:00 WIB, entry fee $0.
Account: bradestudio. Repo: Bradestudio/news-image-20261125 (public).

## The 40 stories (all from the 25 Nov 2026 wire research; nothing invented)

**Heroes (1–3)**
1. Ukraine drones hit a Russian cargo ship (Sparta II) in the Gulf of Finland — Zelenskyy confirms; Norway urges caution.
2. Houthi drone hits Riyadh's tallest tower — 11 injured (Saudi civil defence).
3. Trump gives the Presidential Medal of Freedom to Rudy Giuliani.

**Briefs (4–12)**
4. Putin: retaliation "inevitable" after Ukraine hit Russian oil refineries.
5. Houthis 60 km from Aden; government military: the city will not fall.
6. Trump pardons Thanksgiving turkeys "Freedom" and "Feathers".
7. French court orders ex-President Sarkozy's corruption trial (with Carla Bruni); first hearing 1 April 2027.
8. Huawei guilty of trade-secret theft in a US court, cleared of racketeering.
9. CIA & ODNI hit by a cyber security breach; unclassified information leaked.
10. Anthropic shares fall below the IPO price of $83; almost $200bn in value lost.
11. NATO plans to deploy early-warning (AWACS) aircraft in Poland.
12. Iran: three oil tankers hit by sea mines in the Strait of Hormuz (IRGC navy claim) — CLAIM.

**The rest (13–40)**
13. Earthquake magnitude 5.6 shakes Koshi province, Nepal.
14. BJP & Shiromani Akali Dal ally for the Punjab 2027 election (after a 6-year split).
15. England beat Australia by 8 wickets in the 2nd T20I, chasing 185.
16. 25 Nov = International Day for the Elimination of Violence Against Women.
17. Dell raises its outlook after a record AI server quarter.
18. Nvidia shares fall 7%.
19. UN highlights the humanitarian situation in Gaza.
20. EU announces additional sanctions on Russia.
21. Iraq PM orders the federal government to manage Kurdish oil fields.
22. Kurds reject Baghdad's oil-field order.
23. Trump administration ready to announce new tariffs.
24. Tariffs follow a factory overcapacity probe.
25. Nepal PM Balendra Shah's state visit to India (22–23 Nov).
26. Fort Hood shooter Hasan seeks an execution delay.
27. Libya: a frozen, messy conflict.
28. Ukraine sank a Russian ship in a Libyan port on Sunday.
29. Radar outage delays flights at Chicago O'Hare.
30. Sooryavanshi hits the fastest List A double hundred.
31. New Zealand hold India to a draw in the first Test.
32. Zelenskyy confirms the Gulf of Finland strike.
33. Norway urges caution after the strike.
34. Saudi civil defence: 11 injured in Riyadh.
35. Huawei verdict: trade secrets yes, racketeering no.
36. Anthropic: ~$200bn in value wiped out.
37. NATO's AWACS watch moves east to Poland.
38. Three tankers hit; Hormuz shipping on edge.
39. Sarkozy hearing set for 1 April 2027.
40. Thanksgiving turkeys named Freedom and Feathers.

Note on counting: the 26 researched items are compound; items 32–40 are their
distinct sub-facts (confirmation, casualty count, verdict split, hearing date,
turkey names, etc.), each a separate fact from the same research — no outside
story was added.

## What changed vs the 24 November entry ("Grand Glyph", round 2 — passed grading)

- Three new hero illustrations drawn from scratch: the burning cargo ship
  with a drone above it, the Riyadh tower with its great arch and a strike
  flash, the Medal of Freedom ceremony with ribbon, gold disc and bunting.
- Five new thumbnails: Kremlin towers, the Yemen flag, a Thanksgiving turkey,
  a security shield, an AWACS plane.
- Map pins re-placed by hand after a visual check: the first render had
  overlapping labels in the US cluster (San Francisco / Washington / Langley)
  and the Middle East cluster (Riyadh / Hormuz / Aden); all 12 labels now
  sit clear of each other and of their pins.
- Hero 1 headline shortened by one word ("in the Gulf" → "in Gulf") after
  the visual check showed "Finland" clipped by the two-line ellipsis.

## Verification

- `gen_image.py` run twice: byte-identical PNGs.
  sha256 `443a088d5af6da60d1f30b47bd55c779be27c1f3db9f7bb4cd7c801521500ed3`
- `entry.png`: 1024×1024, 130,809 bytes (< 1 MiB).
- `main.py` sandbox simulation (`python3 -P -s main.py <dir>` in a clean
  directory, plus `MAKEFUN_OUTPUT_DIR`): exit 0, output byte-identical to
  `entry.png`. stdlib only (`os`, `shutil`, `sys`, `pathlib`), no sibling
  imports, no fonts, no network.
- Visual check: the rendered page was read and inspected; masthead, all
  three hero headlines, timeline, numbers strip, 9 briefs, map labels and
  the 13–40 list are legible with no clipped or overlapping text.

## Sources

Reuters, AP, AFP, Saudi civil defence, wire reports of 25 Nov 2026.
Certainty tags: REPORTED = confirmed by officials or wires; CLAIM = one
side's account (story 12, the IRGC mine claim).
