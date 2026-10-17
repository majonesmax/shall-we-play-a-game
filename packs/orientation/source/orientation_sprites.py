"""ORIENTATION's cast, drawn as text (one character per pixel, "." transparent): the new hire, three office
menaces, a goat, and the things on the floor. Muted, office colours - the VGA look snaps them to its palette.

Usage: python packs/orientation/source/orientation_sprites.py   (from the Adventure Forever repository, with
       ADVENTURE_PACKS pointing here)  -> ../cast/*.png and shots/orientation_cast.png
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
from shared.pixelart import edited, from_ascii as _from_ascii, mirrored  # noqa: E402


def from_ascii(art, colours):
    return _from_ascii(pad(art), colours, strict=True)


def taller(art, rows):
    """Text art with the listed rows repeated - a longer torso, longer legs - so a figure grows without being
    redrawn (rows numbered from 0, after padding)."""
    lines = pad(art).strip("\n").split("\n")
    out = []
    for i, line in enumerate(lines):
        out += [line, line] if i in rows else [line]
    return "\n" + "\n".join(out)


def pad(art):
    """Text art with every row right-padded with "." to the widest - so hand-drawn rows needn't be counted."""
    rows = art.strip("\n").split("\n")
    width = max(len(r) for r in rows)
    return "\n" + "\n".join(r.ljust(width, ".") for r in rows)


# ---- the new hire (the hero): 16 wide, a white shirt and a navy tie, a lanyard -------------------------------
HIRE = {"K": (28, 26, 30), "H": (58, 44, 38), "S": (218, 186, 160), "s": (186, 150, 126), "W": (232, 232, 224),
        "w": (190, 194, 190), "T": (44, 56, 92), "P": (72, 74, 82), "p": (52, 54, 60), "L": (84, 132, 116),
        "C": (236, 236, 228), "B": (24, 24, 26)}
_HIRE_HEAD = """
................
.....KKKKKK.....
....KHHHHHHK....
...KHHHHHHHHK...
...KHHHSHHHHK...
...KHSSSSSSHK...
...KSSSSSSSSK...
...KSKSSSSKSK...
...KSSSSSSSSK...
....KSSssSSK....
.....KSSSSK....."""
_HIRE_BODY = """
....KWWTTWWK....
...KWWWTTWWwK...
..KWWLWTTWLWwK..
..KWKWLTTLWKwK..
..KSKWWLLWWKSK..
..KKKWWCCWWKKK..
....KWWCCWwK....
....KPPPPPPK...."""
_HIRE_LEGS = ["""
....KPPKKPpK....
....KPPKKPpK....
....KPPKKPpK....
....KBBKKBBK....
................""", """
....KPPKKPpK....
...KPPK..KPpK...
...KBBK..KPpK...
.........KBBK...
................"""]
_HIRE_BACK_HEAD = """
................
.....KKKKKK.....
....KHHHHHHK....
...KHHHHHHHHK...
...KHHHHHHHHK...
...KHHHHHHHHK...
...KHHHHHHHHK...
...KHHHHHHHHK...
...KSHHHHHHSK...
....KSSSSSSK....
.....KSSSSK....."""
_HIRE_BACK_BODY = """
....KWWLLWWK....
...KWWWLLWWwK...
..KWWWWWWWWWwK..
..KWKWWWWWWKwK..
..KSKWWWWWWKSK..
..KKKWWWWWWKKK..
....KWWWWWwK....
....KPPPPPPK...."""
_HIRE_SIDE = """
................
.....KKKKK......
....KHHHHHK.....
...KHHHHHHHK....
...KHHHHHSSK....
...KHHHSSSSK....
...KHHSSSKSK....
...KHHSSSSSSK...
....KHSSSSSK....
.....KSSssK.....
.....KSSSSK.....
....KWWTTWK.....
...KWWWWTTK.....
...KWWLWWTK.....
...KWWLWWWK.....
...KWSLSWWK.....
...KWKCCKWK.....
....KWCCWK......
....KPPPPK......"""
_HIRE_SIDE_LEGS = ["""
....KPPpK.......
....KPPpK.......
....KPPpK.......
....KBBBBK......
................""", """
...KPPK.KpK.....
..KPPK...KpK....
..KBBK...KpK....
.........KBBK...
................"""]


HIRE_TALLER = (12, 17, 19, 20)  # the shirt and the legs: 24 -> 28 rows


def hire_frames():
    grow = lambda art: from_ascii(taller(art, HIRE_TALLER), HIRE)
    front = [grow(_HIRE_HEAD + _HIRE_BODY + legs) for legs in _HIRE_LEGS]
    back = [grow(_HIRE_BACK_HEAD + _HIRE_BACK_BODY + legs) for legs in _HIRE_LEGS]
    side = [grow(_HIRE_SIDE + legs) for legs in _HIRE_SIDE_LEGS]
    return {"down": front, "up": back, "right": side}


# ---- the goat (the bat, the thief): white and grey, curled horns, two frames (head up / head down) ------------
GOAT = {"K": (30, 28, 26), "G": (226, 222, 210), "g": (182, 178, 166), "N": (124, 110, 90), "E": (196, 160, 60),
        "e": (40, 34, 30), "P": (210, 170, 160), "b": (200, 196, 186)}
GOAT_UP = """
...KKK.KKK........
..KNNK.KNNK.......
..KNK..KNK........
..KKGGGGK.......K.
..KGEeGGK......KgK
..KGGGGGK......KgK
..KPPGGKKKKKKKKKK.
...KbbKKGGGGGGGGGK
...KbK.KGGGGGGGGgK
....K..KGGGGGGGGgK
.......KgggggggggK
.......KgK.KgK.KgK
.......KeK.KeK.KeK"""
GOAT_DOWN = """
..................
..................
.......KKKKKKKKK.K
..KKK.KGGGGGGGGGKgK
.KNNKKKGGGGGGGGGgK.
.KNKGGGKGGGGGGGGgK.
.KKGEeGKgggggggggK.
.KGGGGGKKgK.KgK.KgK
.KPPGGK..KgK..KgK.K
..KbbK...KeK..KeK..
..KbK..............
...K..............."""


def goat_frames():
    return {"up": from_ascii(GOAT_UP, GOAT), "down": from_ascii(GOAT_DOWN, GOAT)}


# ---- the three office menaces (the dragons): 20 wide, drawn as left halves and mirrored ------------------------
# red: the manager - a short-sleeved white dress shirt, red tie, close-cropped hair, a smile that doesn't move
MANAGER = {"K": (22, 18, 18), "H": (28, 22, 20), "S": (122, 80, 56), "s": (98, 62, 44), "W": (238, 238, 230),
           "w": (196, 198, 194), "G": (84, 88, 98), "g": (62, 66, 76), "R": (168, 40, 44), "B": (18, 18, 20),
           "e": (20, 16, 16)}
MANAGER_ART = mirrored("""
......KKKK
.....KHHHH
....KHHHHH
....KHHHHH
....KHHHSS
....KSSSSS
....KSKeSS
....KSSSSS
....KSSSSS
....KSKWWW
.....KSKKK
......KSSS
....KKKWWR
...KWWWWWR
..KWWWWWWR
.KwwKWWWWR
.KSSKWWWWR
.KSSKWWWWR
.KSSKWWWWW
.KSSKwWWWW
.KKKKKKKKK
....KGGGGK
....KgGGGK
....KgGGGK
....KgGGGK
....KgGGGK
....KgGGGK
...KBBBBBK
..........""")
MANAGER_ROAR = edited(MANAGER_ART, {9: [(4, "KSWWWWWWWWSK")], 10: [(5, "KSKeeeeKSK")],    # the smile opens
                                    10 - 1: [(0, "KSK"), (17, "KSK")],                       # hands up
                                    11: [(0, "KSK"), (17, "KSK")], 12: [(0, "KSK"), (17, "KSK")],
                                    13: [(0, "KwK"), (17, "KwK")],                            # short sleeves
                                    15: [(1, "KWW"), (16, "WWK")], 16: [(1, "KWW"), (16, "WWK")],
                                    17: [(1, "KWW"), (16, "WWK")], 18: [(1, "KWW"), (16, "WWK")],
                                    19: [(1, "KWW"), (16, "WWK")]})
# yellow: the guard (the coward) - mustard uniform, navy cap, a flashlight
GUARD = {"K": (26, 24, 26), "N": (38, 46, 72), "n": (60, 70, 100), "S": (204, 166, 138), "Y": (176, 146, 62),
         "y": (138, 112, 46), "Z": (230, 220, 160), "D": (60, 60, 64), "L": (250, 246, 200), "B": (20, 20, 22),
         "e": (30, 30, 34)}
GUARD_ART = mirrored("""
....KKKKKK
...KNNNNNN
..KNNNNNNN
..KnnnnnnK
...KSSSSSS
...KSKeSSS
...KSSSSSS
...KSSSSSS
....KSKKKS
.....KSSSS
...KKKYYYY
..KYYYYYYY
.KYYYZYYYY
.KYYYYYYYY
.KYYKYYYYY
.KYYKYYYYY
.KSSKYYYYY
.KDDKYYYYY
.KDDKyyyyy
.KLLKYYYYK
....KyYYYK
....KyYYYK
....KyYYYK
....KyYYYK
....KyYYYK
...KBBBBBK
..........""")
GUARD_ROAR = edited(GUARD_ART, {  # the coward surrenders: hands up, flashlights dropped, eyes wide
    1: [(0, 'KSK'), (17, 'KSK')],
    2: [(0, 'KSK'), (17, 'KSK')],
    3: [(0, 'KSK'), (17, 'KSK')],
    4: [(0, 'KYK'), (17, 'KYK')],
    5: [(0, 'KYK'), (17, 'KYK'), (3, 'KSeeSSSSeeSK')],
    6: [(0, 'KYK'), (17, 'KYK')],
    7: [(0, 'KYK'), (17, 'KYK')],
    8: [(4, 'KSSSSKKSSSSK')],
    9: [(5, 'KSSSKKSSSK')],
    10: [(0, 'KYK'), (17, 'KYK')],
    11: [(0, 'KYK'), (17, 'KYK')],
    14: [(0, '....'), (16, '....')],
    15: [(0, '....'), (16, '....')],
    16: [(0, '....'), (16, '....')],
    17: [(0, '....'), (16, '....')],
    18: [(0, '....'), (16, '....')],
    19: [(0, '....'), (16, '....')],
})
# green: the counsellor - auburn bob, green cardigan, a clipboard held close
COUNSELLOR = {"K": (26, 24, 28), "H": (120, 64, 44), "h": (92, 48, 34), "S": (226, 194, 172), "C": (86, 126, 92),
              "c": (64, 98, 70), "W": (238, 236, 228), "P": (196, 186, 160), "p": (150, 122, 84),
              "B": (40, 34, 30), "e": (30, 30, 34)}
COUNSELLOR_ART = mirrored("""
.....KKKKK
....KHHHHH
...KHHHHHH
...KHHSSSS
..KHHSSSSS
..KHHSKeSS
..KHHSSSSS
..KhHSSSSS
..KhHKSSKK
...KK.KSSS
....KKKCWW
...KCCCCKW
..KCCCCCCK
.KCCCCKppp
.KCCCCKpPP
.KCCCCKpPW
.KCCCCKpPW
.KSSCCKpPW
.KKKCCKppp
...KCCCCCC
...KcCCCCC
....KcCCCK
....KcCCCK
....KcCCCK
....KcCCCK
...KBBBBBK
..........""")
COUNSELLOR_ROAR = edited(COUNSELLOR_ART, {5: [(5, "KWeWSSWeWK")], 8: [(5, "SKWWWWKS")],
                                          13: [(0, "KSKCCCKpppppppKCCCKSK")[:20]],
                                          12: [(0, "KSKCCCCCCKKCCCCCCKSK")]})


MENACE_TALLER = {  # torso and leg rows repeated: they tower over the new hire, as Adventure's dragons do
    "red": (16, 17, 22, 23, 24, 25), "yellow": (11, 13, 15, 20, 21, 22, 23), "green": (12, 19, 20, 21, 22, 23, 24)}


def menace_frames():
    out = {}
    for colour, (art, roar, palette) in {"red": (MANAGER_ART, MANAGER_ROAR, MANAGER),
                                         "yellow": (GUARD_ART, GUARD_ROAR, GUARD),
                                         "green": (COUNSELLOR_ART, COUNSELLOR_ROAR, COUNSELLOR)}.items():
        rows = MENACE_TALLER[colour]
        out[f"dragon_normal_{colour}"] = from_ascii(taller(art, rows), palette)
        out[f"dragon_roar_{colour}"] = from_ascii(taller(roar, rows), palette)
    return out


# ---- things on the floor ----------------------------------------------------------------------------------------
LETTER_OPENER = """
.KK.............
KWWKKKKKKKKKKK..
KWWwwwwwwwwwwwK.
.KKKKKKKKKKKKK.."""
OPENER = {"K": (34, 32, 36), "W": (120, 84, 56), "w": (206, 210, 214)}
KEYCARD = """
KKKKKKKKKKKK
KCCCCCCCCCCK
KCssCCCCCCCK
KCssCCDDDDCK
KCCCCCCCCCCK
KKKKKKKKKKKK"""
KEYCARDS = {"key_gold": (196, 160, 72), "key_white": (230, 230, 222), "key_black": (54, 56, 60)}
PORTRAIT = """
FFFFFFFFFFFFFF
FKKKKKKKKKKKKF
FKbbbbbbbbbbKF
FKbbbHHHHbbbKF
FKbbHHHHHHbbKF
FKbbHSSSSHbbKF
FKbbHSeSeHbbKF
FKbbHSSSSHbbKF
FKbbHHSmSHHbKF
FKbHHHSSHHHbKF
FKbHHWWWWHHbKF
FKbbWWWWWWbbKF
FKKKKKKKKKKKKF
FFFFFFFFFFFFFF"""  # F: the frame, which flashes like the chalice
PORTRAIT_COLOURS = {"F": FLASH, "K": (30, 26, 24), "b": (120, 134, 140), "H": (26, 20, 20),
                    "S": (222, 182, 142), "e": (34, 26, 22), "m": (172, 98, 86), "W": (220, 214, 200)}
VACUUM = """
.KK.........
KHHK........
.KHHK.......
..KHHK......
...KHHK.....
....KHK.....
....KRRRK...
...KRrRRRK..
...KRrRRRK..
...KRrRRRK..
...KRrRRRK..
...KRRRRRK..
..KKKKKKKKK.
.KDDDDDDDDDK
.KKKKKKKKKKK"""  # an upright vacuum: handle, bag, floor head
VACUUM_COLOURS = {"K": (28, 26, 30), "H": (150, 152, 158), "R": (150, 46, 40), "r": (204, 90, 72),
                  "D": (64, 66, 72)}
TABLE_TOP = """
...KKKKKKKKKKKKKKKKKK...
..KWWWWWWWWWWWWWWWWWWK..
.KWWwwwwwwwwwwwwwwwwWWK.
KcKWwwwwwwwwwwwwwwwwWKcK"""
TABLE_MID = """
KcKWwwwwwwwwwwwwwwwwWKcK"""
TABLE_BOTTOM = """
.KWWwwwwwwwwwwwwwwwwWWK.
..KWWWWWWWWWWWWWWWWWWK..
...KKKKKKKKKKKKKKKKKK..."""
TABLE = {"K": (30, 26, 24), "W": (104, 74, 52), "w": (132, 96, 66), "c": (52, 54, 60)}
SPEAKER = """
.......KK.......
......KDDK......
.....KDDDDK.....
....KDDGGDDK....
...KDDGGGGDDK...
..KDDDDDDDDDDK..
.KDDDDDDDDDDDDK.
KKKKKKKKKKKKKKKK
KbbbbbbbbbbbbbbK
KKKKKKKKKKKKKKKK"""
SPEAKER_COLOURS = [{"K": (26, 26, 30), "D": (60, 62, 70), "G": (90, 200, 120), "b": (110, 84, 60)},
                   {"K": (26, 26, 30), "D": (60, 62, 70), "G": (40, 80, 54), "b": (110, 84, 60)}]  # lit, dim


def item_pictures():
    out = {"item_sword": from_ascii(LETTER_OPENER, OPENER), "item_chalice": from_ascii(PORTRAIT, PORTRAIT_COLOURS),
           "item_magnet": from_ascii(VACUUM, VACUUM_COLOURS),
           "bridge_top": from_ascii(TABLE_TOP, TABLE), "bridge_middle": from_ascii(TABLE_MID, TABLE),
           "bridge_bottom": from_ascii(TABLE_BOTTOM, TABLE)}
    for name, colour in KEYCARDS.items():
        shade = tuple(int(v * 0.75) for v in colour)
        out[f"item_{name}"] = from_ascii(KEYCARD, {"K": (28, 26, 30), "C": colour, "s": (200, 176, 96),
                                                    "D": shade})
    for i, colours in enumerate(SPEAKER_COLOURS):
        out[f"messenger_{i}"] = from_ascii(SPEAKER, colours)
    return out


def pictures():
    out = {}
    for view, frames in hire_frames().items():
        for i, frame in enumerate(frames):
            out[f"hero_{view}_{i}"] = frame
    goat = goat_frames()
    out["bat_up"], out["bat_down"] = goat["up"], goat["down"]
    out.update(menace_frames())
    out.update(item_pictures())
    return out


def cast_sheet(path, scale=5, per_row=13):
    """Every picture on carpet, scaled up, in rows (the flashing marker shown in one of its colours)."""
    pics = list(pictures().items())
    pics.append(("hero_left_0", pictures()["hero_right_0"][:, ::-1]))
    hmax = max(p.shape[0] for _, p in pics) + 4
    cells = []
    for _, p in pics:
        p = p.copy()
        p[np.all(p[..., :3] == FLASH, axis=2), :3] = (200, 168, 80)
        cell = np.zeros((hmax, p.shape[1] + 6, 3), np.uint8)
        cell[:] = (54, 76, 64)
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
    print(cast_sheet(os.path.join(HERE, "..", "..", "..", "shots", "orientation_cast.png")))
