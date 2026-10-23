"""Synthesize cartoon SFX for the comedic edit (deterministic, 48 kHz stereo WAV)."""
import numpy as np, wave, sys, os

SR = 48000
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/sfx"
rng = np.random.default_rng(7)

def env(n, a=0.005, r=0.2):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e

def save(name, x, gain=0.85):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    s = (np.stack([x, x], 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())

def tone(freqs, dur, kind="sine"):
    t = np.arange(int(dur * SR)) / SR
    f = np.interp(t, np.linspace(0, dur, len(freqs)), freqs)
    ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == "square":
        return np.sign(np.sin(ph)) * 0.6 + 0.4 * np.sin(3 * ph) / 3
    if kind == "saw":
        return 2 * ((ph / (2 * np.pi)) % 1) - 1
    return np.sin(ph)

# boing: wobbling pitch spring
t = np.arange(int(0.7 * SR)) / SR
f = 180 + 260 * np.exp(-t * 5) * (1 + 0.5 * np.sin(2 * np.pi * 14 * t))
save("boing", np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5))

# slide whistle down / up
save("slide-down", tone([1800, 400], 0.6) * env(int(0.6 * SR), 0.01, 0.1))
save("slide-up", tone([400, 1900], 0.45) * env(int(0.45 * SR), 0.01, 0.08))

# record scratch: band-limited noise with fast pitch wobble
n = int(0.5 * SR); t = np.arange(n) / SR
noise = rng.standard_normal(n)
wob = np.sin(2 * np.pi * np.cumsum(300 + 900 * np.abs(np.sin(2 * np.pi * 5 * t))) / SR)
save("scratch", np.convolve(noise * wob, np.ones(12) / 12, "same") * env(n, 0.002, 0.15))

# dun dun duuun: brassy saw chords
parts = []
for f0, d in [(196, 0.28), (185, 0.28), (165, 1.3)]:
    x = sum(tone([f0 * k], d, "saw") / k for k in (1, 1.5, 2))
    parts.append(x * env(len(x), 0.01, 0.12 if d < 1 else 0.8)); parts.append(np.zeros(int(0.06 * SR)))
save("dundun", np.concatenate(parts))

# sad trombone: wah-wah-wah-waaah
parts = []
for f0, d in [(311, 0.35), (293, 0.35), (277, 0.35), (261, 1.1)]:
    t = np.arange(int(d * SR)) / SR
    vib = 1 + (0.02 * np.sin(2 * np.pi * 6 * t) if d > 1 else 0)
    x = sum(np.sin(2 * np.pi * np.cumsum(f0 * k * vib * np.ones_like(t)) / SR) / k for k in (1, 2, 3, 4))
    wah = 0.6 + 0.4 * np.sin(np.pi * t / d)
    parts.append(x * wah * env(len(t), 0.03, 0.12 if d < 1 else 0.6))
save("trombone", np.concatenate(parts))

# crickets
n = int(1.6 * SR); t = np.arange(n) / SR
chirp = np.sin(2 * np.pi * 4500 * t) * (np.sin(2 * np.pi * 30 * t) > 0.3)
gate = ((t % 0.5) < 0.18).astype(float)
save("crickets", chirp * gate * env(n, 0.05, 0.3), 0.5)

# ding (bell)
t = np.arange(int(1.2 * SR)) / SR
save("ding", sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1320, 1), (2640, 0.4), (3960, 0.2)]) * np.exp(-t * 4))

# car horn (two-tone)
d = 0.55; t = np.arange(int(d * SR)) / SR
save("horn", (tone([420], d, "square") + tone([520], d, "square")) * env(len(t), 0.01, 0.05), 0.7)

# pop
t = np.arange(int(0.12 * SR)) / SR
save("pop", np.sin(2 * np.pi * np.cumsum(900 - 5000 * t) / SR) * np.exp(-t * 40))

# rewind (fast reversed-tape squeal)
n = int(0.9 * SR); t = np.arange(n) / SR
f = 300 + 2500 * (t / 0.9) ** 2
x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + 0.5 * np.convolve(rng.standard_normal(n), np.ones(6) / 6, "same") * np.sin(2 * np.pi * 40 * t)
save("rewind", x * env(n, 0.02, 0.1), 0.6)

# stamp (thud)
t = np.arange(int(0.35 * SR)) / SR
save("stamp", (np.sin(2 * np.pi * np.cumsum(120 - 200 * t) / SR) + 0.4 * rng.standard_normal(len(t)) * np.exp(-t * 60)) * np.exp(-t * 12))
print("ok")
