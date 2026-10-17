# Shall we play a game?

Demo packs for [Adventure Forever](https://github.com/majonesmax/adventure-forever) - Atari 2600 *Adventure*
running unmodified in an emulator and redrawn live from its RAM. Each demo is a **pack**: a cast (who's in
the game) and a world (where it happens) that any of Adventure Forever's looks can show.

| Demo | What it is | Best with |
|---|---|---|
| [`packs/orientation`](packs/orientation) | an office floor that goes on too long: off-white corridors, dim green carpet, pools of fluorescent light, departments behind elevator doors, and a goat. *Work in progress.* | the VGA look |

## Playing a demo

With [Adventure Forever](https://github.com/majonesmax/adventure-forever#running-it-from-source-macos-windows-linux)
running from source, point it at this repository's `packs` folder:

```sh
ADVENTURE_PACKS=../shall-we-play-a-game/packs python play.py --pack orientation --look vga
```

(Windows PowerShell: `$env:ADVENTURE_PACKS="..\shall-we-play-a-game\packs"; python play.py --pack orientation --look vga`.)
In the game, **W** and **C** cycle worlds and casts, **L** the looks, and **H** shows every key.

## Making one

A pack is a folder with a `pack.json`, a `cast/` and/or a `world/`: see
[making a pack](https://github.com/majonesmax/adventure-forever/blob/main/docs/making-a-pack.md).

Code: MIT (`LICENSE`). Art: CC BY 4.0 (`LICENSE-ASSETS.md`). Adventure is © 1980 Atari, created by Warren
Robinett; not included - bring your own ROM. Fan-made demos, not affiliated with or endorsed by anyone.
