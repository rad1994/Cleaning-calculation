import struct, zlib, os

BG = (0x4f, 0x60, 0x72)        # --pr (background)
HANDLE = (0x8a, 0x5a, 0x3a)    # broom handle (brown)
BAND = (0x3a, 0x4d, 0x5e)      # binding band (dark)
BRISTLE = (0xe8, 0xc4, 0x68)   # bristles (gold)
BRISTLE_DK = (0xc9, 0xa2, 0x3e)
SPARK = (0xe8, 0xec, 0xf0)     # sparkle dots

OUT_DIR = os.path.join(os.path.dirname(__file__), 'icons')
os.makedirs(OUT_DIR, exist_ok=True)


def seg_dist(px, py, ax, ay, bx, by):
    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    ab2 = abx * abx + aby * aby
    t = max(0.0, min(1.0, (apx * abx + apy * aby) / ab2))
    cx, cy = ax + abx * t, ay + aby * t
    dx, dy = px - cx, py - cy
    return (dx * dx + dy * dy) ** 0.5


def point_in_triangle(px, py, a, b, c):
    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
    d1 = sign((px, py), a, b)
    d2 = sign((px, py), b, c)
    d3 = sign((px, py), c, a)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def make_png(size, maskable=False):
    s = float(size)
    px = bytearray(size * size * 3)

    # broom geometry (fractions of canvas size)
    handle_a = (0.34 * s, 0.20 * s)
    handle_b = (0.62 * s, 0.60 * s)
    handle_w = 0.045 * s

    band_a = (0.585 * s, 0.555 * s)
    band_b = (0.655 * s, 0.655 * s)
    band_w = 0.075 * s

    tri = ((0.655 * s, 0.625 * s), (0.84 * s, 0.79 * s), (0.50 * s, 0.905 * s))

    bristle_lines = [
        ((0.65 * s, 0.635 * s), (0.575 * s, 0.86 * s)),
        ((0.685 * s, 0.665 * s), (0.685 * s, 0.875 * s)),
        ((0.72 * s, 0.70 * s), (0.795 * s, 0.85 * s)),
    ]

    sparkles = [
        (0.27 * s, 0.78 * s, 0.02 * s),
        (0.21 * s, 0.66 * s, 0.012 * s),
        (0.33 * s, 0.85 * s, 0.01 * s),
    ]

    for y in range(size):
        for x in range(size):
            cx, cy = x + 0.5, y + 0.5
            color = BG

            if point_in_triangle(cx, cy, *tri):
                color = BRISTLE
                for (lx1, ly1), (lx2, ly2) in bristle_lines:
                    if seg_dist(cx, cy, lx1, ly1, lx2, ly2) <= 0.012 * s:
                        color = BRISTLE_DK
                        break

            if seg_dist(cx, cy, band_a[0], band_a[1], band_b[0], band_b[1]) <= band_w / 2:
                color = BAND

            if seg_dist(cx, cy, handle_a[0], handle_a[1], handle_b[0], handle_b[1]) <= handle_w / 2:
                color = HANDLE

            for sx, sy, sr in sparkles:
                dx, dy = cx - sx, cy - sy
                if dx * dx + dy * dy <= sr * sr:
                    color = SPARK

            i = (y * size + x) * 3
            px[i:i + 3] = bytes(color)

    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filter type 0 (none)
        start = y * size * 3
        raw += px[start:start + size * 3]

    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')


for size, name, maskable in [
    (192, 'icon-192.png', False),
    (512, 'icon-512.png', False),
    (512, 'icon-512-maskable.png', True),
    (180, 'apple-touch-icon.png', False),
]:
    data = make_png(size, maskable)
    path = os.path.join(OUT_DIR, name)
    with open(path, 'wb') as f:
        f.write(data)
    print(path, len(data), 'bytes')
