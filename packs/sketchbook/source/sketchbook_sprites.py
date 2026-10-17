"""SKETCHBOOK's cast, drawn as text (one character per pixel, "." transparent): a boy in striped pyjamas with a
purple crayon, the things he drew that got out of hand, and what he drew along the way.

The boy is real, so he's coloured in. Everything else he drew - so it's a crayon outline on paper ("o" is the
paper inside a drawing), scribbled in here and there.

Usage: python packs/sketchbook/source/sketchbook_sprites.py   (from the Adventure Forever repository, with
       ADVENTURE_PACKS pointing here)  -> ../cast/*.png and shots/sketchbook_cast.png
"""

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
for root in (os.environ.get("ADVENTURE_FOREVER", ""), os.path.join(HERE, "..", "..", "..", "..", "adventure-nes")):
    if root and os.path.isdir(os.path.join(root, "content")):
        sys.path.insert(0, root)  # Adventure Forever's helpers (shared/pixelart.py, content/)
        break
from content.pictures import FLASH, save_folder  # noqa: E402
from shared.pixelart import edited, from_ascii as _from_ascii  # noqa: E402

PAPER = (246, 240, 226)
PURPLE, PURPLE_DARK = (112, 64, 168), (78, 40, 124)


def from_ascii(art, colours):
    return _from_ascii(pad(art), {"o": PAPER, **colours}, strict=True)


def pad(art):
    """Text art with every row right-padded with "." to the widest - so hand-drawn rows needn't be counted."""
    rows = art.strip("\n").split("\n")
    width = max(len(r) for r in rows)
    return "\n" + "\n".join(r.ljust(width, ".") for r in rows)


def taller(art, rows):
    """Text art with the listed rows repeated (rows numbered from 0, after padding)."""
    lines = pad(art).strip("\n").split("\n")
    out = []
    for i, line in enumerate(lines):
        out += [line, line] if i in rows else [line]
    return "\n" + "\n".join(out)


# ---- the boy (the hero): tousled brown hair, blue-and-white striped pyjamas, bare feet, his crayon -----------
BOY = {"K": (44, 34, 48), "H": (128, 80, 48), "h": (96, 58, 34), "S": (238, 196, 164), "s": (206, 158, 128),
       "m": (184, 92, 92), "P": (96, 150, 216), "W": (250, 250, 246), "V": PURPLE, "v": PURPLE_DARK}
_BOY_HEAD = """
....KK.KK.....
...KHHKHHKK...
..KHHHHHHHHK..
..KHhHHHHhHK..
..KHSSHSSHHK..
..KSSSSSSSSK..
..KSKSSSSKSK..
..KSSSSSSSSK..
...KSSmmSSK...
....KSSSSK...."""
_BOY_BODY = """
...KPPPPPPK...
..KWWWWWWWWK..
.KPKPPPPPPKPK.
.KWKWWWWWWKWK.
.KPKPPPPPPKPK.
.KSKWWWWWWKSKV
..K.PPPPPP.KVv
...KWWWWWWK..v"""
_BOY_LEGS = ["""
...KPPKKPPK...
...KWWKKWWK...
...KPPKKPPK...
...KSSKKSSK...
..KKKK..KKKK..""", """
...KPPKKPPK...
..KWWK..KWWK..
..KPPK..KPPK..
..KSSK..KSSK..
.KKKK....KKKK."""]
_BOY_BACK_HEAD = """
....KK.KK.....
...KHHKHHKK...
..KHHHHHHHHK..
..KHhHHHHhHK..
..KHHHHHhHHK..
..KHHhHHHHHK..
..KHHHHHHhHK..
..KSHHHHHHSK..
...KSSSSSSK...
....KSSSSK...."""
_BOY_BACK_BODY = """
...KPPPPPPK...
..KWWWWWWWWK..
.KPKPPPPPPKPK.
.KWKWWWWWWKWK.
.KPKPPPPPPKPK.
VKSKWWWWWWKSK.
vVK.PPPPPP.K..
v..KWWWWWWK..."""
_BOY_SIDE = """
....KK.K......
...KHHKHHK....
..KHHHHHHHK...
..KHhHHHHHK...
..KHHHHSSSK...
..KHHHSSSSSK..
..KHHSSSKSSK..
..KHHSSSSSSSK.
...KHSSSSmSK..
....KSSSSSK...
....KPPPPPK...
...KWWWWWWK...
...KPPPPPPK...
...KWWWWSSKVV.
...KPPPPPKKVvv
...KWWWWWK...."""
_BOY_SIDE_LEGS = ["""
....KPPPK.....
....KWWWK.....
....KPPPK.....
....KSSSK.....
....KKKKKK....""", """
...KPPKPPK....
..KWWK.KWWK...
..KPPK..KPPK..
..KSSK..KSSK..
.KKKK....KKKK."""]

BOY_TALLER = (12, 13)  # the pyjama top: a little longer


def boy_frames():
    grow = lambda art: from_ascii(taller(art, BOY_TALLER), BOY)
    front = [grow(_BOY_HEAD + _BOY_BODY + legs) for legs in _BOY_LEGS]
    back = [grow(_BOY_BACK_HEAD + _BOY_BACK_BODY + legs) for legs in _BOY_LEGS]
    side = [grow(_BOY_SIDE + legs) for legs in _BOY_SIDE_LEGS]
    return {"down": front, "up": back, "right": side}


# ---- the things he drew (the dragons): outlines on paper, scribbled in ------------------------------------------
# red: a crayon dragon. yellow (the coward): a lumpy monster that throws up its arms. green: a scribble with teeth.
DRAGON = """
..RRRR..............
.RooooR.............
RoEoooR.............
RooooooRR...........
.RRRooooR...........
...RRoooR...R.R.R...
....RoooR..RoRoRoR..
....RooooRRooooooR..
.....RooooooooooooR.
.....RoroooroooroooR
.....RooroooroooroR.
......RooooroooroR..
......RooooooooooR..
.......RooooooooR...
.......RoooRRoooR...
........RRR..RRR....
.......RoR...RoR....
.......RoR...RoR....
......RRRR..RRRR...."""
DRAGON_ROAR = edited(DRAGON, {  # jaws wide, a scribble of fire
    3: [(0, "RRRRoooRR")], 4: [(0, ".vv.RoooR")], 5: [(0, "RRRRRooo")]})
DRAGON_TALLER = (4, 5, 6, 15, 16, 17)

LUMP = """
......YYYYYY........
....YYooooooYY......
...YooooooooooY.....
..YooEEooooEEooY....
..YooEEooooEEooY....
..YoooooooooooooY...
.YoooooYYYYooooooY..
.YooooYooooYoooooY..
YYoooooYYYYooooooYY.
YoYoooooooooooooYoY.
Y.YoooyoooyoooyoY.Y.
..YooyoooyoooyooY...
..YoooooooooooooY...
...YoooooooooooY....
...YYoYYYYYYoYY.....
....YoY....YoY......
...YYYY....YYYY....."""
LUMP_ROAR = """
Y.....YYYYYY......Y.
YY..YYooooooYY...YY.
.YoYooooooooooY.YoY.
..YYoEEooooEEooYoY..
...YoEEooooEEooYY...
...YoooooooooooooY..
..YooooooYYoooooY...
..YoooooYooYooooY...
..YoooooYooYooooY...
..YooooooYYoooooY...
..YoooyoooyoooyoY...
..YooyoooyoooyooY...
..YoooooooooooooY...
...YoooooooooooY....
...YYoYYYYYYoYY.....
....YoY....YoY......
...YYYY....YYYY....."""
LUMP_TALLER = (5, 12, 13, 15)

SCRIBBLE = """
.....G.GGGG.G.......
...GGoGGooGGoGG.....
..GoGGoGGGoGGoGG....
.GGoGoGGoGGoGGoG....
GoGWWWoGoGGWWWoGG...
GGoWEWoGoGoWEWGoG...
GoGWWWGGoGGWWWoGG...
GGoGGoGGoGGoGGoG....
GoWWWWWWWWWWWWGGG...
GGWvWvWvWvWvWWGoG...
GoGGoGGoGGoGGoGGG...
.GGoGGoGGoGGoGG.....
..GGoGGoGoGGoG......
...GG.GGGG.GG.......
....G..G...G........
....G..G...G........
...GG..GG..GG......."""
SCRIBBLE_ROAR = edited(SCRIBBLE, {  # the mouth opens wide
    8: [(2, "WWWWWWWWWWWW")], 9: [(2, "vWvWvWvWvWvW")], 10: [(2, "KKKKKKKKKKKK")],
    11: [(3, "WvWvWvWvWvW")]})
SCRIBBLE_TALLER = (2, 3, 10, 11, 14, 15)

VILLAINS = {
    "red": (DRAGON, DRAGON_ROAR, DRAGON_TALLER,
            {"R": (204, 48, 52), "r": (240, 128, 120), "E": (34, 30, 36), "v": (240, 128, 48)}),
    "yellow": (LUMP, LUMP_ROAR, LUMP_TALLER,
               {"Y": (214, 160, 20), "y": (250, 210, 60), "E": (34, 30, 36)}),
    "green": (SCRIBBLE, SCRIBBLE_ROAR, SCRIBBLE_TALLER,
              {"G": (60, 150, 72), "W": (250, 250, 246), "E": (34, 30, 36), "v": (60, 150, 72),
               "K": (34, 30, 36)}),
}


def villain_frames():
    out = {}
    for colour, (art, roar, rows, palette) in VILLAINS.items():
        out[f"dragon_normal_{colour}"] = from_ascii(taller(art, rows), palette)
        out[f"dragon_roar_{colour}"] = from_ascii(taller(roar, rows), palette)
    return out


# ---- the bird (the bat, the thief): long neck, long legs, two frames (wings up / down) ---------------------------
BIRD_UP = """
B..........B......
BB........BB......
.BBo....oBB...BBB.
..BBooooBB...BoEB.
...BooooB...BooBvv
....BoooBBBBooB...
.....BoooooooB....
......BBBBBBB.....
........B.B.......
.......BB.BB......"""
BIRD_DOWN = """
..............BBB.
.............BoEB.
............BooBvv
...BBBBBBBBBooB...
..BoooooooooooB...
.BBooooBBBBBBB....
BB..BooB..........
B....BB.B.B.......
.......BB.BB......"""
BIRD = {"B": (240, 128, 48), "E": (34, 30, 36), "v": (250, 210, 60)}


# ---- what he drew along the way --------------------------------------------------------------------------------
CRAYON = """
.....KKKKKKKKKKKK.
..KKVVwwVVVVVwwVVK
KvVVVVwwVVVVVwwVVK
..KKVVwwVVVVVwwVVK
.....KKKKKKKKKKKK."""  # the sword: his crayon, drawn huge - the tip on the left
CRAYON_COLOURS = {"K": (44, 34, 48), "V": PURPLE, "v": PURPLE_DARK, "w": (176, 140, 220)}
KEY = """
.CCC.........
CoooCCCCCCCCC
CoooCoooooooC
CoooCCCCCoCoC
.CCC.....C.C."""
KEYS = {"key_gold": (214, 160, 20), "key_white": (150, 148, 150), "key_black": (34, 30, 36)}
WINDOW = """
FFFFFFFFFFFFFF
FNNNNNNFNNNNNF
FNNNYYNFNNNNNF
FNNYYNNFNNSNNF
FNNYYNNFNNNNNF
FNNNYYNFNNNNNF
FFFFFFFFFFFFFF
FNNNNNNFNNNSNF
FNSNNNNFNNNNNF
FNNNNNNFNNNNNF
FNNNNNSFNNNNNF
FFFFFFFFFFFFFF"""  # the chalice: his own bedroom window, the moon in it. F: the frame, which flashes
WINDOW_COLOURS = {"F": FLASH, "N": (44, 84, 180), "Y": (250, 210, 60), "S": (254, 254, 250)}
MAGNET = """
GGGG..GGGG
GooG..GooG
MMMM..MMMM
MooM..MooM
MooM..MooM
MooM..MooM
MoooMMoooM
.MooooooM.
..MMMMMM.."""  # a horseshoe magnet, grey tips
MAGNET_COLOURS = {"M": (204, 48, 52), "G": (150, 148, 150)}
LADDER_TOP = """
KK....................KK
KoK..................KoK
KoKKKKKKKKKKKKKKKKKKKKoK"""
LADDER_MID = """
KoK..................KoK"""
LADDER_BOTTOM = """
KoKKKKKKKKKKKKKKKKKKKKoK
KoK..................KoK
KK....................KK"""  # the bridge: a ladder laid flat across the wall
LADDER = {"K": (120, 78, 52)}
ASLEEP = ["""
.............KKK..
...............K..
.WWWWWW......KKK..
WWWKKKKW..........
WWKHHHHKPPPPPPPP..
WWKSSSSSPPPPPPPPP.
WWKSKSSSPWPPPWPPPP
WWWKSSSPPPPPPPPPPP
.WWWWWWPPPPPPPPPP.""", """
..............KKK.
.........KKK....K.
.WWWWWW....K..KKK.
WWWKKKKW..KKK.....
WWKHHHHKPPPPPPPP..
WWKSSSSSPPPPPPPPP.
WWKSKSSSPWPPPWPPPP
WWWKSSSPPPPPPPPPPP
.WWWWWWPPPPPPPPPP."""]  # the messenger: the boy asleep, a blanket drawn up, Zs floating
ASLEEP_COLOURS = {"K": (44, 34, 48), "W": (250, 250, 246), "H": (128, 80, 48), "S": (238, 196, 164),
                  "P": PURPLE}


def item_pictures():
    out = {"item_sword": from_ascii(CRAYON, CRAYON_COLOURS), "item_chalice": from_ascii(WINDOW, WINDOW_COLOURS),
           "item_magnet": from_ascii(MAGNET, MAGNET_COLOURS),
           "bridge_top": from_ascii(LADDER_TOP, LADDER), "bridge_middle": from_ascii(LADDER_MID, LADDER),
           "bridge_bottom": from_ascii(LADDER_BOTTOM, LADDER)}
    for name, colour in KEYS.items():
        out[f"item_{name}"] = from_ascii(KEY, {"C": colour})
    for i, art in enumerate(ASLEEP):
        out[f"messenger_{i}"] = from_ascii(art, ASLEEP_COLOURS)
    return out


def pictures():
    out = {}
    for view, frames in boy_frames().items():
        for i, frame in enumerate(frames):
            out[f"hero_{view}_{i}"] = frame
    out["bat_up"], out["bat_down"] = from_ascii(BIRD_UP, BIRD), from_ascii(BIRD_DOWN, BIRD)
    out.update(villain_frames())
    out.update(item_pictures())
    return out


def cast_sheet(path, scale=5, per_row=13):
    """Every picture on paper, scaled up, in rows (the flashing marker shown in one of its colours)."""
    pics = list(pictures().items())
    pics.append(("hero_left_0", pictures()["hero_right_0"][:, ::-1]))
    hmax = max(p.shape[0] for _, p in pics) + 4
    cells = []
    for _, p in pics:
        p = p.copy()
        p[np.all(p[..., :3] == FLASH, axis=2), :3] = (112, 64, 168)
        cell = np.zeros((hmax, p.shape[1] + 6, 3), np.uint8)
        cell[:] = (226, 218, 200)
        a = p[..., 3:4] > 0
        sub = cell[hmax - p.shape[0] - 2:hmax - 2, 3:3 + p.shape[1]]
        cell[hmax - p.shape[0] - 2:hmax - 2, 3:3 + p.shape[1]] = np.where(a, p[..., :3], sub)
        cells.append(cell)
    rows = [np.concatenate(cells[i:i + per_row], axis=1) for i in range(0, len(cells), per_row)]
    width = max(r.shape[1] for r in rows)
    sheet = np.concatenate([np.pad(r, ((0, 2), (0, width - r.shape[1]), (0, 0))) for r in rows], axis=0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(sheet).resize((sheet.shape[1] * scale, sheet.shape[0] * scale), Image.NEAREST).save(path)
    return path


if __name__ == "__main__":
    save_folder(os.path.join(HERE, "..", "cast"), pictures())
    print(cast_sheet(os.path.join(HERE, "..", "..", "..", "shots", "sketchbook_cast.png")))
