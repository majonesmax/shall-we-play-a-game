"""ORIENTATION's world: an office floor that goes on too long - off-white corridors with panel seams and
baseboards, a dim green carpet, pools of fluorescent light from ceiling panels you never see. Painted in code
(full colour; the look reduces it - the VGA look dithers the light pools).

Every place shares the corridor style; pack.json gives each place its name and a tint (areas[place]["tint"]).
The castle gates are elevator doors: the gate's opening (its height in the game) slides two doors apart.
Now and then a room's fluorescent lights stutter (lighting()).
The three castles are structures inside the floor, painted onto the castle's own walls (the game's outline -
where you can walk - is untouched): a wall of filing cabinets (Records), a padded partition suite (Wellness),
a wire-mesh storage cage (Archives). Their battlements become what's stacked on top.
"""

import numpy as np

from content.world import World, area
from shared import layout as L

CARPET = np.array([54, 76, 64], float)       # dim green
WALL_TOP = np.array([178, 184, 176], float)  # off-white, in the gloom
SEAM = 0.88                                  # panel seams on the wall tops
FACE = 0.58                                  # the wall's front face, toward the viewer
EDGE = np.array([96, 102, 98], float)        # the line along a wall's top edge
BASEBOARD = np.array([78, 84, 80], float)
LIGHT = np.array([255, 250, 228], float)     # the fluorescent pools: a touch warm
PANEL_GRID = (48, 40)                        # ceiling panels: every 48 px across, 40 down
GATE_SHUT, GATE_OPEN = 32, 8                 # the game's gate height (px) shut, and just before it's gone
DOOR_FINISH = {"gold": (176, 150, 92), "white": (214, 216, 210), "black": (74, 78, 84)}  # brass, enamel, steel


def light_pools(h, w):
    """0..1: soft pools of light on a grid, as from ceiling panels."""
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    gx, gy = PANEL_GRID
    dx = ((xx - gx / 2) % gx) - gx / 2
    dy = ((yy - gy / 2) % gy) - gy / 2
    return np.exp(-(dx ** 2 / (2 * 12.0 ** 2) + dy ** 2 / (2 * 9.0 ** 2)))


def elevator(w, h, finish):
    """Elevator doors for a gate h px tall in the game (GATE_SHUT = shut): always drawn full height, anchored
    at the top of the doorway (padding above keeps them still while the game's gate box shrinks), the gap
    between the two doors widening as the gate opens. RGBA."""
    door_h, frame_w = GATE_SHUT, w + 6
    opening = min(1.0, max(0.0, (GATE_SHUT - h) / (GATE_SHUT - GATE_OPEN)))
    out = np.zeros((2 * GATE_SHUT - h, frame_w, 4), np.uint8)
    top = GATE_SHUT - h
    finish = np.array(finish, float)
    door = out[top:top + door_h]
    door[:, :] = (28, 30, 32, 255)                                 # the frame, and the dark shaft behind
    inner = frame_w - 4
    leaf = int(round(inner / 2 * (1 - opening)))                   # each door's visible width
    for x0, x1 in ((2, 2 + leaf), (2 + inner - leaf, 2 + inner)):
        if x1 <= x0:
            continue
        shade = np.linspace(1.08, 0.82, x1 - x0)                   # brushed metal: lit from the left
        door[2:door_h - 1, x0:x1, :3] = np.clip(finish[None, None] * shade[None, :, None], 0, 255)
        door[2:door_h - 1, x0:x1, 3] = 255
    door[1, 1:frame_w - 1] = (120, 124, 128, 255)                  # the lintel
    return out


CASTLE_ROOMS = {0x11: "records", 0x0F: "wellness", 0x10: "archives"}  # gold, white, black
CASTLE_BOX = (60, 180, 0, 144)  # the castle's part of the room: x0, x1, y0, y1 (grid columns 10-29, rows 0-4)
TOP = 16                        # the battlements' row


def records(img, cm, xx, yy):
    """A wall of beige filing cabinets, binders and boxes stacked on top."""
    cab, drawer = 12, 12
    body = cm & (yy >= TOP)
    img[body] = (196, 184, 150)
    front = body & ((yy - TOP) % drawer >= 1) & ((xx % cab) >= 1) & ((xx % cab) <= cab - 2)
    img[front] = (214, 204, 172)                                         # each drawer's face
    img[body & ((yy - TOP) % drawer == 0)] = (120, 110, 88)              # the seams between drawers
    img[body & (xx % cab == 0)] = (96, 88, 70)                           # between cabinets
    handle = front & ((yy - TOP) % drawer == 7) & (np.abs(xx % cab - 6) <= 2)
    img[handle] = (70, 66, 60)
    label = front & ((yy - TOP) % drawer >= 3) & ((yy - TOP) % drawer <= 4) & (np.abs(xx % cab - 6) <= 1)
    img[label] = (240, 236, 222)
    top = cm & (yy < TOP)                                                # boxes and binders on top
    colours = [(150, 116, 72), (60, 84, 120), (150, 116, 72), (120, 50, 46), (166, 132, 86), (64, 96, 78)]
    img[top] = np.array(colours)[(xx[top] // 6) % len(colours)]
    img[top & (yy % 8 == 7)] = (90, 70, 46)


def wellness(img, cm, xx, yy):
    """A padded partition suite: pale cushioned panels with wood trim, small plants along the top."""
    panel = 16
    body = cm & (yy >= TOP)
    u = (xx % panel) / (panel - 1)
    cushion = 1.0 - 0.18 * (2 * u - 1) ** 2                              # each panel rounded, lit from the front
    img[body] = (np.array((214, 216, 206), float)[None] * cushion[body][:, None]).astype(int)
    img[body & (xx % panel == 0)] = (150, 152, 144)
    img[body & ((yy == TOP) | (yy == TOP + 1))] = (150, 110, 74)         # wood trim, top and bottom
    img[body & (yy >= CASTLE_BOX[3] - 4)] = (150, 110, 74)
    top = cm & (yy < TOP)                                                # a potted plant on each bump
    img[top] = (54, 76, 64)                                              # (the carpet shows round them)
    pot = top & (yy >= TOP - 5)
    img[pot] = (176, 96, 64)
    leaves = top & (yy < TOP - 5) & (yy >= 2) & ((xx + yy) % 3 != 0)
    img[leaves] = (76, 140, 82)


def archives(img, cm, xx, yy):
    """A wire-mesh storage cage: steel frame, a grid of mesh, shelves of archive boxes in the dark behind.
    Ducts and vents along the top."""
    body = cm & (yy >= TOP)
    img[body] = (24, 26, 30)                                             # the dark inside
    shelf = body & ((yy - TOP) % 24 == 23)
    img[shelf] = (70, 74, 80)
    box = body & ((yy - TOP) % 24 >= 12) & ((yy - TOP) % 24 <= 21) & ((xx % 14) >= 2) & ((xx % 14) <= 11)
    img[box] = (96, 80, 58)                                              # archive boxes on the shelves
    img[box & ((yy - TOP) % 24 == 16) & (np.abs(xx % 14 - 6) <= 1)] = (200, 196, 180)  # their labels
    mesh = body & ((xx % 4 == 0) | ((yy - TOP) % 4 == 0))
    img[mesh] = (104, 110, 116)                                          # the mesh in front of it all
    img[body & ((xx % 40 == 0) | (xx % 40 == 1))] = (52, 56, 60)        # the frame's uprights
    top = cm & (yy < TOP)                                                # vent stacks with dark slits
    img[top] = (112, 116, 122)
    img[top & (yy % 4 == 2)] = (40, 42, 46)


STRUCTURES = {"records": records, "wellness": wellness, "archives": archives}


FLICKER = {0: 0.72, 1: 0.72, 2: 0.72, 5: 0.82, 6: 0.82, 11: 0.76}  # frames into a stutter -> how lit


class CustomWorld(World):
    def lighting(self, room_num, frame_no):
        """Every 7-13 s (it differs room to room) the lights stutter: a dip, back, two shorter dips."""
        period = 420 + (room_num * 97) % 360
        return FLICKER.get((frame_no + room_num * 53) % period, 1.0)

    def gate(self, castle, w, h):
        return elevator(w, h, DOOR_FINISH[castle]) if h > 0 else None

    def tint(self, room_num):
        t = self.setting(area(room_num), "tint")
        return np.array(t if t else (1.0, 1.0, 1.0), float)

    def room(self, room):
        n = room["room"]
        if n in self.rooms:
            return self.rooms[n]
        m = L.wall_mask(room)
        h, w = m.shape
        rng = np.random.default_rng(n)
        tint = self.tint(n)
        # the carpet: a low, even weave, lit in pools
        weave = rng.normal(0, 3.0, (h, w))
        weave += 2.0 * ((np.arange(w)[None, :] + np.arange(h)[:, None]) % 4 == 0)
        pools = light_pools(h, w)
        floor = CARPET[None, None] * tint + weave[..., None]
        floor = floor * (0.55 + 0.45 * pools[..., None]) + (LIGHT - CARPET)[None, None] * 0.12 * pools[..., None]
        img = floor.copy()
        # the walls: off-white tops with panel seams, a darker front face where the floor is below, a baseboard
        yy, xx = np.mgrid[0:h, 0:w]
        top = np.broadcast_to(WALL_TOP * tint, (h, w, 3)).copy()
        top[(xx % 24 == 0)] *= SEAM
        top += rng.normal(0, 1.5, (h, w))[..., None]
        img[m] = top[m]
        above_floor = [~np.roll(m, -k, axis=0) for k in range(1, 7)]
        face = m & np.logical_or.reduce(above_floor)
        img[face] = (WALL_TOP * tint * FACE)
        edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)) & ~face
        img[edge] = EDGE * tint
        base = m & ~np.roll(m, -1, axis=0) | m & ~np.roll(m, -2, axis=0)
        img[base] = BASEBOARD
        # a soft shadow on the carpet below each wall
        for k, dim in ((1, 0.62), (2, 0.72), (3, 0.82), (4, 0.9)):
            below = ~m & np.roll(m, k, axis=0)
            img[below] *= dim
        if n in CASTLE_ROOMS:  # the castle's walls as a structure on the floor
            x0, x1, y0, y1 = CASTLE_BOX
            cm = m & (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
            STRUCTURES[CASTLE_ROOMS[n]](img, cm, xx, yy)
            if CASTLE_ROOMS[n] != "wellness":  # standing on the floor: a baseboard, like the corridor walls
                img[cm & base] = BASEBOARD
        self.rooms[n] = np.clip(img, 0, 255).astype(np.uint8)
        return self.rooms[n]
