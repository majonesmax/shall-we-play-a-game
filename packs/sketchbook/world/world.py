"""SKETCHBOOK's world: a blank page, and only what a boy has drawn on it in purple crayon - every wall a wobbly
outline, scribbled in with hatching. The game decides where the walls are; he just draws them.

Painted in code. Every place is drawn the same way; pack.json gives each place its name, and a few places a
different crayon (areas[place]["ink"]: the woods in green, the scribbles in red, the dark in graphite).
The castles are things he drew on the castle's own walls (the game's outline - where you can walk - is
untouched): his house with its windows lit (home), a round stone tower, and an old house with something
looking out. The gates are drawn doors.
On the paper look the page is the paper itself; other looks show it as a page under their own rules.
"""

import numpy as np

from content.world import World, area
from shared import layout as L

PAGE = np.array([246, 240, 226], float)    # the paper
PURPLE = np.array([112, 64, 168], float)    # his crayon
WOBBLE = 0.9                                # how far a line wanders, in pixels


def grown(m, k=1):
    """The mask grown by k pixels (4-neighbour)."""
    for _ in range(k):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m


def wobbled(mask, seed):
    """The mask redrawn by hand: every pixel taken from a little way off, along slow waves."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    ys = np.clip(yy + np.round(WOBBLE * np.sin(xx / 7.0 + seed * 1.3 + yy / 29.0)).astype(int), 0, h - 1)
    xs = np.clip(xx + np.round(WOBBLE * np.sin(yy / 6.0 + seed * 0.7 + xx / 31.0)).astype(int), 0, w - 1)
    return mask[ys, xs]


def outline(m, seed):
    """A crayon line two pixels wide along the walls' edge (one inside, one outside), redrawn by hand."""
    inner = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    outer = grown(m) & ~m
    return wobbled(inner | outer, seed)


def hatching(m, rng, every=5):
    """Diagonal scribble strokes filling the walls, broken where the crayon skipped."""
    h, w = m.shape
    yy, xx = np.mgrid[0:h, 0:w]
    strokes = ((xx + yy) % every == 0) & (rng.random((h, w)) > 0.18)
    return m & strokes


CASTLE_ROOMS = {0x11: "home", 0x0F: "tower", 0x10: "old_house"}  # gold, white, black
CASTLE_BOX = (60, 180, 0, 144)  # the castle's part of the room: x0, x1, y0, y1
TOP = 16                        # the battlements' row
YELLOW, ORANGE, RED, SKY, GRAPHITE, BROWN = ((250, 210, 60), (240, 128, 48), (204, 48, 52), (110, 180, 228),
                                             (70, 68, 74), (120, 78, 52))


def windows(cm, xx, yy, w, h, gap_x, gap_y, x_off=0):
    """Window rectangles (w x h) on a grid inside the castle's body: (frame, pane)."""
    body = cm & (yy >= TOP + 6) & (yy < CASTLE_BOX[3] - 18)
    u, v = (xx - x_off) % gap_x, (yy - TOP - 6) % gap_y
    pane = body & (u >= 3) & (u < 3 + w) & (v >= 3) & (v < 3 + h)
    frame = grown(pane) & body & ~pane
    return frame, pane


def home(img, cm, xx, yy, rng):
    """His house: warm orange scribble, yellow lit windows with crossbars, a red roof along the top."""
    img[hatching(cm & (yy >= TOP), rng, 4)] = ORANGE
    frame, pane = windows(cm, xx, yy, 10, 12, 20, 26)
    img[pane] = YELLOW
    img[frame | (pane & ((xx % 20 == 8) | ((yy - TOP - 6) % 26 == 9)))] = PURPLE
    img[cm & (yy < TOP)] = PAGE
    img[hatching(cm & (yy < TOP), rng, 3)] = RED


def tower(img, cm, xx, yy, rng):
    """A round stone tower: rows of stones drawn as little arcs, narrow arched windows."""
    body = cm & (yy >= TOP)
    stone = body & (((yy - TOP) % 10 == 0) | (((xx + 6 * (((yy - TOP) // 10) % 2)) % 12 == 0) & ((yy - TOP) % 10 < 9)))
    img[stone] = SKY
    frame, pane = windows(cm, xx, yy, 5, 14, 24, 34, 4)
    img[pane] = GRAPHITE
    img[frame] = PURPLE
    img[hatching(cm & (yy < TOP), rng, 3)] = SKY


def old_house(img, cm, xx, yy, rng):
    """An old house, scribbled dark, boarded windows - and in one of them, two eyes."""
    img[hatching(cm & (yy >= TOP), rng, 3)] = GRAPHITE
    frame, pane = windows(cm, xx, yy, 10, 12, 20, 26)
    img[pane] = PAGE
    img[pane & ((xx + yy) % 6 < 2)] = BROWN                       # boards across
    img[frame] = PURPLE
    eyes = (np.abs(yy - (TOP + 6 + 26 + 8)) <= 1) & ((np.abs(xx - 105) <= 1) | (np.abs(xx - 110) <= 1))
    img[eyes & cm] = YELLOW
    img[hatching(cm & (yy < TOP), rng, 3)] = GRAPHITE


STRUCTURES = {"home": home, "tower": tower, "old_house": old_house}


def door(w, h):
    """A drawn door, cut to the gate's height h: brown planks, an outline, a round knob. RGBA."""
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3], out[..., 3] = PAGE, 255
    yy, xx = np.mgrid[0:h, 0:w]
    out[(xx % 5 == 2) & (xx > 0) & (xx < w - 1)] = (*BROWN, 255)
    edge = (xx <= 1) | (xx >= w - 2) | (yy >= h - 2)
    out[edge] = (*PURPLE.astype(int), 255)
    if h > 12:
        out[h // 2 - 1:h // 2 + 2, w - 6:w - 3] = (*YELLOW, 255)
    return out


class CustomWorld(World):
    def gate(self, castle, w, h):
        return door(w, h) if h > 0 else None

    def ink(self, room_num):
        c = self.setting(area(room_num), "ink")
        return np.array(c if c else PURPLE, float)

    def room(self, room):
        n = room["room"]
        if n in self.rooms:
            return self.rooms[n]
        m = L.wall_mask(room)
        h, w = m.shape
        rng = np.random.default_rng(n)
        yy, xx = np.mgrid[0:h, 0:w]
        img = np.broadcast_to(PAGE, (h, w, 3)).copy()
        img += rng.normal(0, 1.2, (h, w))[..., None]               # the paper's own faint grain
        ink = self.ink(n)
        img[hatching(m, rng)] = ink
        if n in CASTLE_ROOMS:
            x0, x1, y0, y1 = CASTLE_BOX
            cm = m & (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
            img[cm] = PAGE
            STRUCTURES[CASTLE_ROOMS[n]](img, cm, xx, yy, rng)
        img[outline(m, n)] = ink
        self.rooms[n] = np.clip(img, 0, 255).astype(np.uint8)
        return self.rooms[n]
