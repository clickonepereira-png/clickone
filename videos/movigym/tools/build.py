"""Builds index.html from tools/template.html.txt: inlines the tracked shapes and the pin icon."""
import json
PIN = ('<svg viewBox="0 0 74 96"><path d="M37 93 C37 93 5 56 5 36 A32 32 0 1 1 69 36 C69 56 37 93 37 93 Z" '
       'fill="#ffd60a" stroke="#0d0d0d" stroke-width="4"/><circle cx="37" cy="36" r="12" fill="#0d0d0d"/></svg>')
src = open("tools/template.html.txt").read()
tracks = json.dumps(json.load(open("data/tracks.json")), separators=(",", ":"))
out = src.replace("__TRACKS__", tracks).replace("__PIN2__", PIN).replace("__PIN__", PIN)
open("index.html", "w").write(out)
print(len(out))
