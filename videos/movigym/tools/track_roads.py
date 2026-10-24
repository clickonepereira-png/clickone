"""Road lines anchored on hand-marked keyframes.
Between two keyframes the line is carried forward from the first and backward from
the second with homographies estimated only from features near the road (rooftops
have parallax and drag a whole-frame fit), then the two are cross-blended, so the
line is re-anchored on the real street at every keyframe."""
import cv2, json, sys
import numpy as np

SRC, FPS, K, N = sys.argv[1], 30, 1080 / 480, 24

cap = cv2.VideoCapture(SRC)
fr = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    fr.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))

def resample(pts, n=N):
    p = np.array(pts, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    s = np.linspace(0, d[-1], n)
    return np.c_[np.interp(s, d, p[:, 0]), np.interp(s, d, p[:, 1])]

def step(i, j, line):
    """Homography taking frame i to frame j, fitted on features near the line."""
    mask = np.zeros_like(fr[i])
    cv2.polylines(mask, [line.astype(np.int32)], False, 255, 110)
    p0 = cv2.goodFeaturesToTrack(fr[i], 500, 0.01, 6, mask=mask)
    if p0 is None or len(p0) < 25:
        p0 = cv2.goodFeaturesToTrack(fr[i], 600, 0.01, 7)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(fr[i], fr[j], p0, None, winSize=(25, 25), maxLevel=4)
    m = st.ravel() == 1
    H, _ = cv2.findHomography(p0[m], p1[m], cv2.RANSAC, 1.5)
    return H

def carry(line, i, j):
    out, cur = {i: line}, line
    d = 1 if j > i else -1
    for k in range(i, j, d):
        H = step(k, k + d, cur)
        cur = cv2.perspectiveTransform(cur.reshape(-1, 1, 2), H).reshape(-1, 2)
        out[k + d] = cur
    return out

spec = json.load(open(sys.argv[2]))
tracks = json.load(open(sys.argv[3]))
for sh in spec:
    keys = [(round(t * FPS), resample(p)) for t, p in sh["keys"]]
    a, b = round(sh["show"][0] * FPS), round(sh["show"][1] * FPS)
    res = {}
    res.update(carry(keys[0][1], keys[0][0], a))  # lead-in before the first key
    res.update(carry(keys[-1][1], keys[-1][0], b))  # tail after the last key
    for (ka, la), (kb, lb) in zip(keys, keys[1:]):
        fwd, bwd = carry(la, ka, kb), carry(lb, kb, ka)
        for i in range(ka, kb + 1):
            w = (i - ka) / (kb - ka)
            res[i] = (1 - w) * fwd[i] + w * bwd[i]
    seq = [[[round(x * K, 1), round(y * K, 1)] for x, y in res[i]] for i in range(a, b)]
    tracks[sh["id"]] = {"t0": a / FPS, "frames": seq}
    print(sh["id"], len(seq))
for gone in ("calle43b", "derecha", "turf"):
    tracks.pop(gone, None)
json.dump(tracks, open(sys.argv[3], "w"))
