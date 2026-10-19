"""SKETCHBOOK's world: a blank page, and only what a boy has drawn on it in purple crayon - every wall a
wobbly outline, scribbled in with hatching. The game decides where the walls are; he just draws them.

Painted in code. Every place is drawn the same way; pack.json gives each place its name, and a few places a
different crayon (areas[place]["ink"]: the woods in green, the scribbles in red, the dark in graphite).
The castles are things he drew on the castle's own walls (the game's outline - where you can walk - is
untouched): his house with its windows lit (home), a round stone tower, and an old house with something
looking out. The gates are drawn doors.
On the paper look the page is the paper itself; other looks show it as a page under their own rules.
"""

from typing import Callable

import numpy as np

from content.world import Room, World, area
from shared import layout as L
from shared.types import Floats, Mask, Picture, Point

PAGE = np.array([246, 240, 226], float)    # the paper
PURPLE = np.array([112, 64, 168], float)    # his crayon
WOBBLE = 0.9                                # how far a line wanders, in pixels
SKIPPED = 0.18                              # how often the crayon skips, in a hatching stroke
GRAIN = 1.2                                 # the paper's faint grain: how much each pixel's shade varies


def grown(mask: Mask, steps: int = 1) -> Mask:
    """The mask grown by `steps` pixels (4-neighbour)."""
    for _ in range(steps):
        mask = mask | np.roll(mask, 1, 0) | np.roll(mask, -1, 0) | np.roll(mask, 1, 1) | np.roll(mask, -1, 1)
    return mask


def wobbled(mask: Mask, seed: int) -> Mask:
    """The mask redrawn by hand: every pixel taken from a little way off, along slow waves."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    from_y = np.clip(yy + np.round(WOBBLE * np.sin(xx / 7.0 + seed * 1.3 + yy / 29.0)).astype(int), 0, h - 1)
    from_x = np.clip(xx + np.round(WOBBLE * np.sin(yy / 6.0 + seed * 0.7 + xx / 31.0)).astype(int), 0, w - 1)
    return mask[from_y, from_x]


def outline(walls: Mask, seed: int) -> Mask:
    """A crayon line two pixels wide along the walls' edge (one inside, one outside), redrawn by hand."""
    surrounded = np.roll(walls, 1, 0) & np.roll(walls, -1, 0) & np.roll(walls, 1, 1) & np.roll(walls, -1, 1)
    inner = walls & ~surrounded
    outer = grown(walls) & ~walls
    return wobbled(inner | outer, seed)


def hatching(walls: Mask, rng: np.random.Generator, every: int = 5) -> Mask:
    """Diagonal scribble strokes filling the walls, broken where the crayon skipped."""
    h, w = walls.shape
    yy, xx = np.mgrid[0:h, 0:w]
    strokes = ((xx + yy) % every == 0) & (rng.random((h, w)) > SKIPPED)
    return walls & strokes


CASTLE_ROOMS = {0x11: "home", 0x0F: "tower", 0x10: "old_house"}  # gold, white, black
CASTLE_BOX = (60, 180, 0, 144)  # the castle's part of the room: x0, x1, y0, y1
TOP = 16                        # the battlements' row
YELLOW, ORANGE, RED, SKY, GRAPHITE, BROWN = ((250, 210, 60), (240, 128, 48), (204, 48, 52), (110, 180, 228),
                                             (70, 68, 74), (120, 78, 52))
OLD_HOUSE_EYES = (TOP + 6 + 26 + 8, (105, 110))   # the eyes' row, and each eye's column


def windows(castle: Mask, xx: Floats, yy: Floats, size: Point, spacing: Point,
            x_off: int = 0) -> tuple[Mask, Mask]:
    """Window rectangles (size: w, h) on a grid (spacing: across, down) inside the castle's body:
    (frame, pane)."""
    w, h = size
    spacing_x, spacing_y = spacing
    body = castle & (yy >= TOP + 6) & (yy < CASTLE_BOX[3] - 18)
    across, down = (xx - x_off) % spacing_x, (yy - TOP - 6) % spacing_y
    pane = body & (across >= 3) & (across < 3 + w) & (down >= 3) & (down < 3 + h)
    frame = grown(pane) & body & ~pane
    return frame, pane


def home(img: Floats, castle: Mask, xx: Floats, yy: Floats, rng: np.random.Generator) -> None:
    """His house: warm orange scribble, yellow lit windows with crossbars, a red roof along the top."""
    img[hatching(castle & (yy >= TOP), rng, 4)] = ORANGE
    frame, pane = windows(castle, xx, yy, (10, 12), (20, 26))
    img[pane] = YELLOW
    crossbars = pane & ((xx % 20 == 8) | ((yy - TOP - 6) % 26 == 9))
    img[frame | crossbars] = PURPLE
    img[castle & (yy < TOP)] = PAGE
    img[hatching(castle & (yy < TOP), rng, 3)] = RED


def tower(img: Floats, castle: Mask, xx: Floats, yy: Floats, rng: np.random.Generator) -> None:
    """A round stone tower: rows of stones drawn as little arcs, narrow arched windows."""
    body = castle & (yy >= TOP)
    course = (yy - TOP) // 10                                     # which row of stones
    between_courses = (yy - TOP) % 10 == 0
    between_stones = ((xx + 6 * (course % 2)) % 12 == 0) & ((yy - TOP) % 10 < 9)
    img[body & (between_courses | between_stones)] = SKY
    frame, pane = windows(castle, xx, yy, (5, 14), (24, 34), 4)
    img[pane] = GRAPHITE
    img[frame] = PURPLE
    img[hatching(castle & (yy < TOP), rng, 3)] = SKY


def old_house(img: Floats, castle: Mask, xx: Floats, yy: Floats, rng: np.random.Generator) -> None:
    """An old house, scribbled dark, boarded windows - and in one of them, two eyes."""
    img[hatching(castle & (yy >= TOP), rng, 3)] = GRAPHITE
    frame, pane = windows(castle, xx, yy, (10, 12), (20, 26))
    img[pane] = PAGE
    img[pane & ((xx + yy) % 6 < 2)] = BROWN                       # boards across
    img[frame] = PURPLE
    eyes_y, (left_eye, right_eye) = OLD_HOUSE_EYES
    eyes = (np.abs(yy - eyes_y) <= 1) & ((np.abs(xx - left_eye) <= 1) | (np.abs(xx - right_eye) <= 1))
    img[eyes & castle] = YELLOW
    img[hatching(castle & (yy < TOP), rng, 3)] = GRAPHITE


Structure = Callable[[Floats, Mask, Floats, Floats, np.random.Generator], None]   # paints a castle's front
STRUCTURES: dict[str, Structure] = {"home": home, "tower": tower, "old_house": old_house}


def door(w: int, h: int) -> Picture:
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
    def gate(self, castle: str, w: int, h: int) -> Picture | None:
        return door(w, h) if h > 0 else None

    def ink(self, room_number: int) -> Floats:
        chosen = self.setting(area(room_number), "ink")
        return np.array(chosen if chosen else PURPLE, float)

    def room(self, room: Room) -> Picture:
        room_number = room["room"]
        if room_number in self.rooms:
            return self.rooms[room_number]
        walls = L.wall_mask(room)
        h, w = walls.shape
        rng = np.random.default_rng(room_number)
        yy, xx = np.mgrid[0:h, 0:w]
        img = np.broadcast_to(PAGE, (h, w, 3)).copy()
        img += rng.normal(0, GRAIN, (h, w))[..., None]
        ink = self.ink(room_number)
        img[hatching(walls, rng)] = ink
        if room_number in CASTLE_ROOMS:
            x0, x1, y0, y1 = CASTLE_BOX
            castle = walls & (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
            img[castle] = PAGE
            STRUCTURES[CASTLE_ROOMS[room_number]](img, castle, xx, yy, rng)
        img[outline(walls, room_number)] = ink
        self.rooms[room_number] = np.clip(img, 0, 255).astype(np.uint8)
        return self.rooms[room_number]
