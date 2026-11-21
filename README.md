# World News, 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/thomasmoa97/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/thomasmoa97/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121)

My entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121):
one picture that sums up Saturday 21 November 2026.

![World News, 21 November 2026](entry.png)

## What's on the front page

`main.py` draws the whole page with Pillow alone. It never touches the
network, never reads the clock and never rolls a die, so two runs write
the exact same bytes.

**The big story — missiles land in Poland.** Russia launches its largest
barrage of the war on Ukraine: more than 400 drones and 110 missiles.
Two missiles come down on Polish soil, and Warsaw calls it a deliberate
provocation.

**The rest of the page:**

- Wall Street's AI sell-off drags the S&P 500 into correction; the
  Nasdaq gives back all of its 2026 gains.
- GTA VI opens with $3.8 billion in first-day sales, the biggest launch
  ever.
- Rohingya survivors tell of the 2017 exodus as the Hague court confirms
  Myanmar's genocide verdict.
- COP31 in Antalya runs into overtime with fossil fuels still unresolved.
- London and Brussels sign the biggest post-Brexit deal package yet.
- A new pill makes pancreatic tumours undetectable in one in twelve
  patients.
- Plus the ticker: the Shenzhen declaration's aftermath, Saudi missile
  intercepts, Gaza, and Bitcoin sliding toward $62K.

## How to run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes a 1024x1024 PNG to `out/entry.png`, about 121 KB — well
under the 1 MiB cap.

## License

MIT — see [LICENSE](LICENSE).
