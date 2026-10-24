"""Planar drone tracking: chains frame-to-frame homographies (LK flow + RANSAC)
and maps shapes drawn on a reference frame onto every frame of the shot.
Shapes are given in source pixels (480x854); output is in composition pixels (x2.25)."""
import cv2, json, sys
import numpy as np

SRC, FPS, K = sys.argv[1], 30, 1080 / 480

def frames(path):
    cap = cv2.VideoCapture(path)
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            return out
        out.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))

def chain(fr, a, b):
    """G[i] maps frame i -> frame a, for i in [a, b)."""
    G = {a: np.eye(3)}
    for i in range(a + 1, b):
        p0 = cv2.goodFeaturesToTrack(fr[i - 1], 600, 0.01, 7)
        p1, st, _ = cv2.calcOpticalFlowPyrLK(fr[i - 1], fr[i], p0, None, winSize=(21, 21), maxLevel=4)
        m = st.ravel() == 1
        H, inl = cv2.findHomography(p1[m], p0[m], cv2.RANSAC, 2.0)  # frame i -> frame i-1
        G[i] = G[i - 1] @ H
    return G

def apply(H, pts):
    p = np.hstack([np.array(pts, float), np.ones((len(pts), 1))]) @ H.T
    return (p[:, :2] / p[:, 2:3]).tolist()

fr = frames(SRC)
spec = json.load(open(sys.argv[2]))
out = {}
for seg in spec:
    a, b = round(seg["from"] * FPS), round(seg["to"] * FPS)
    G = chain(fr, a, b)
    for sh in seg["shapes"]:
        r = round(sh["ref"] * FPS)
        f0, f1 = round(sh["show"][0] * FPS), round(sh["show"][1] * FPS)
        seq = []
        for i in range(max(a, f0), min(b, f1)):
            H = np.linalg.inv(G[i]) @ G[r]
            seq.append([[round(x * K, 1), round(y * K, 1)] for x, y in apply(H, sh["pts"])])
        out[sh["id"]] = {"t0": max(a, f0) / FPS, "frames": seq}
json.dump(out, open(sys.argv[3], "w"))
print({k: len(v["frames"]) for k, v in out.items()})
