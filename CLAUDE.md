# Working on these demos with an AI assistant

Notes for Claude Code (or any coding assistant) making or changing a demo pack here. People: the same notes
are how a demo gets made.

Each folder in `packs/` is a pack for [Adventure Forever](https://github.com/majonesmax/adventure-forever): a
cast (who) and a world (where) that any of its looks can show. Clone Adventure Forever next to this repository
(`../adventure-forever` or `../adventure-nes`); its [CLAUDE.md](https://github.com/majonesmax/adventure-forever/blob/main/CLAUDE.md)
has the commands and rules this repository relies on.

## A pack

```
packs/<name>/
  pack.json                 names: the cast's, the world's, each place's, the win lines, the title word
  source/<name>_sprites.py  the whole cast as text art (one character a pixel) -> writes cast/*.png
  cast/*.png                generated - don't hand-edit
  world/world.py            paints each room (a CustomWorld), the gates, any lighting
  world/music.json          the soundtrack, in the FM synth's notation (engine/fm.py)
```

Start from the nearest existing demo. The picture names a cast can have, and what each pack.json field does,
are in Adventure Forever's [making a pack](https://github.com/majonesmax/adventure-forever/blob/main/docs/making-a-pack.md).

## Commands (run from the Adventure Forever folder)

```sh
export ADVENTURE_PACKS=../shall-we-play-a-game/packs
python ../shall-we-play-a-game/packs/<name>/source/<name>_sprites.py   # regenerate the cast + a cast sheet
python tools/preview.py --pack <name>                                  # the pack in every look - read the PNG
python engine/fm.py ../shall-we-play-a-game/packs/<name>/world/music.json  # the songs as .wav files
python play.py --pack <name> --look <look>                             # play it
```

## Rules

- **If you know, you know.** Every demo is inspired by something, and names none of it: no names of shows,
  books, characters, companies or places, no logos, no likenesses, no quotes, no exact designs. Describe the
  feeling and invent the details.
- **The game decides where walls are.** A world chooses only what they look like; castle shapes can be
  disguised, not moved.
- **Look before you say it's done:** run `tools/preview.py`, read the picture, and check every look.
- Each demo is made for one look (its row in the README says which) but must be playable in all of them.
- Code is MIT and art is CC BY 4.0. Only add art you made, or made here as text art.

## Readable code

The same rules as Adventure Forever's ([its CLAUDE.md](https://github.com/majonesmax/adventure-forever/blob/main/CLAUDE.md),
"Readable code"): names that say what things are, one idea per line, named numbers, short functions, types
on every signature (`Picture`, `Mask`, `Floats`, `Rgb`... from its `shared/types.py`), lines up to 110
characters.

```sh
ruff check --config ruff.toml .     # the readability rules
pyright                             # the type hints (pyrightconfig.json finds Adventure Forever beside this)
python tools/readability.py         # ...both, and no short names; every file is at zero - keep it there
```

The tools come from `requirements-dev.txt`, or from Adventure Forever's `.venv`, which readability.py finds
by itself. `.claude/settings.json` runs readability.py after every edit, and GitHub runs all three on every
push (`.github/workflows/checks.yml`). A tidy-up must not change the art: the cast scripts must regenerate
the same PNGs (`git status` shows none changed), and the worlds must paint the same rooms.

## Adding a demo to the README

A row in the table: the name linked to its folder, the look it's best in, one sentence, and a screenshot in
`docs/media/<name>.png` (three screens side by side, at 2x).
