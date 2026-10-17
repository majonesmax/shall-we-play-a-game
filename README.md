# Shall we play a game?

Demo packs for [Adventure Forever](https://github.com/majonesmax/adventure-forever) - Atari 2600 *Adventure*
running unmodified in an emulator and redrawn live from its RAM. Each demo is a **pack**: a cast (who's in
the game) and a world (where it happens) that any of Adventure Forever's looks can show.

| Demo | What it is | Best with |
|---|---|---|
| [`packs/orientation`](packs/orientation) | an office floor that goes on too long: off-white corridors, dim green carpet, flickering fluorescent light, departments behind elevator doors, a goat, and its own FM soundtrack | the VGA look |

## Playing a demo

**With the app** ([download Adventure Forever](https://github.com/majonesmax/adventure-forever#%EF%B8%8F-download), version 1.1 or later):

1. Download this repository: **Code → Download ZIP** at the top of this page.
2. Start Adventure Forever, and **drag the downloaded zip onto the game window** (or the unzipped folder).
   Every demo in it is added, and the first one starts. They stay added for next time.
3. Press **L** for the VGA look (*ORIENTATION* is made for it), **C** / **W** to change cast and world, **H**
   for every key.

The demos include a little code (`world/world.py` paints ORIENTATION's rooms) - it only draws pictures.

**From source** - with [Adventure Forever](https://github.com/majonesmax/adventure-forever#running-it-from-source-macos-windows-linux)
set up, point it at this repository's `packs` folder:

```sh
ADVENTURE_PACKS=../shall-we-play-a-game/packs python play.py --pack orientation --look vga
```

(Windows PowerShell: `$env:ADVENTURE_PACKS="..\shall-we-play-a-game\packs"; python play.py --pack orientation --look vga`.)

## Making one

A pack is a folder with a `pack.json`, a `cast/` and/or a `world/`: see
[making a pack](https://github.com/majonesmax/adventure-forever/blob/main/docs/making-a-pack.md).

Code: MIT (`LICENSE`). Art: CC BY 4.0 (`LICENSE-ASSETS.md`). Adventure is © 1980 Atari, created by Warren
Robinett; not included - bring your own ROM. Fan-made demos, not affiliated with or endorsed by anyone.
