"""Synthesize the project's SFX (pure Python, seeded -> reproducible).

Run: python3 tools/make_sfx.py   (writes assets/sfx/*.wav, 48 kHz mono 16-bit)
"""
import math, random, struct, wave, os

SR = 48000
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sfx")


def write(name, samples, gain=0.9):
    peak = max(1e-9, max(abs(s) for s in samples))
    data = b"".join(struct.pack("<h", int(max(-1, min(1, s / peak * gain)) * 32767)) for s in samples)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data)


def env(t, a, d):  # attack / exponential decay
    return (t / a if t < a else math.exp(-(t - a) / d))


def whoosh(dur=0.32, seed=1, lo=0.02, hi=0.35):
    rnd = random.Random(seed); n = int(SR * dur); out = []; y = y2 = 0.0
    for i in range(n):
        t = i / n
        shape = math.sin(math.pi * t) ** 2          # swell in, swell out
        k = lo + (hi - lo) * math.sin(math.pi * t)   # sweeping low-pass = "air"
        x = rnd.uniform(-1, 1)
        y += k * (x - y); y2 += k * (y - y2)
        out.append(y2 * shape)
    return out


def pop(f0=900, f1=320, dur=0.09):
    n = int(SR * dur); out = []; ph = 0.0
    for i in range(n):
        t = i / SR
        f = f1 + (f0 - f1) * math.exp(-t * 60)
        ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * env(t, 0.002, 0.025))
    return out


def click(seed=3, dur=0.03, f=2600):
    rnd = random.Random(seed); n = int(SR * dur)
    return [(0.6 * math.sin(2 * math.pi * f * i / SR) + 0.4 * rnd.uniform(-1, 1)) * env(i / SR, 0.0005, 0.004) for i in range(n)]


def impact(dur=0.4, seed=5):
    rnd = random.Random(seed); n = int(SR * dur); out = []; ph = 0.0; y = 0.0
    for i in range(n):
        t = i / SR
        f = 45 + 110 * math.exp(-t * 25)
        ph += 2 * math.pi * f / SR
        y += 0.25 * (rnd.uniform(-1, 1) - y)
        out.append(math.sin(ph) * env(t, 0.002, 0.12) + 0.5 * y * env(t, 0.001, 0.02))
    return out


def tick(dur=0.025):
    n = int(SR * dur)
    return [math.sin(2 * math.pi * 4200 * i / SR) * env(i / SR, 0.0003, 0.003) for i in range(n)]


def confirm(dur=0.5):
    n = int(SR * dur); out = []
    for i in range(n):
        t = i / SR
        a = math.sin(2 * math.pi * 1046.5 * t) * env(t, 0.003, 0.08)                     # C6
        b = math.sin(2 * math.pi * 1568.0 * t) * env(t - 0.09, 0.003, 0.16) if t > 0.09 else 0  # G6
        out.append(0.6 * a + 0.7 * b + 0.15 * math.sin(2 * math.pi * 3136 * t) * env(t, 0.003, 0.05))
    return out


def riser(dur=1.4, seed=7):
    """Noise + tone sweeping upward: the 'climbing' bed under the stacking blocks."""
    rnd = random.Random(seed); n = int(SR * dur); out = []; y = 0.0; ph = 0.0
    for i in range(n):
        t = i / n
        k = 0.02 + 0.3 * t
        y += k * (rnd.uniform(-1, 1) - y)
        ph += 2 * math.pi * (180 + 520 * t * t) / SR
        amp = t ** 1.6 * (1 - max(0, (t - 0.94) / 0.06))
        out.append((0.7 * y + 0.25 * math.sin(ph)) * amp)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("whoosh.wav", whoosh(0.32, 1), 0.7)
    write("whoosh-fast.wav", whoosh(0.22, 2, 0.04, 0.5), 0.6)
    write("pop.wav", pop(), 0.7)
    write("pop-high.wav", pop(1400, 600, 0.07), 0.55)
    write("click.wav", click(), 0.6)
    write("impact.wav", impact(), 0.95)
    write("tick.wav", tick(), 0.45)
    write("confirm.wav", confirm(), 0.7)
    write("riser.wav", riser(), 0.6)
    # six pops climbing a major scale: one per completed column
    for i, semis in enumerate([0, 2, 4, 5, 7, 9]):
        f = 620 * 2 ** (semis / 12)
        write(f"pop-up-{i + 1}.wav", pop(f * 1.6, f, 0.1), 0.7)
    print("ok")
