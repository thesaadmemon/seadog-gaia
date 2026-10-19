"""Write index.html for the StarIQ deck pitch from the narration timing.

usage: python tools/build_index.py

Slide slots, narration clips and slide-change whooshes all come from one table here
plus assets/audio/vo/timing.json, so a re-timed narration only needs a rerun.
"""
import json
import subprocess

TOTAL = 210.7
SLIDES = [  # composition id, chapter label, start, end
    ("d01-title", "StarIQ", 0.0, 9.5),
    ("d02-sovereign", "Problem 1 · Sovereignty", 9.5, 27.6),
    ("d03-race", "The race", 27.6, 49.6),
    ("d04-reliability", "Problem 2 · Reliability", 49.6, 65.0),
    ("d05-pain", "Is the pain real?", 65.0, 93.5),
    ("d06-demo", "Demonstrated", 93.5, 103.6),
    ("d07-solution", "Solution", 103.6, 121.9),
    ("d08-evidence", "Evidence", 121.9, 134.0),
    ("d09-market", "Market", 134.0, 148.7),
    ("d10-team", "Team", 148.7, 169.3),
    ("d11-moat", "Defensibility", 169.3, 182.8),
    ("d12-ask", "The ask", 182.8, 202.7),
    ("d13-close", "StarIQ", 202.7, TOTAL),
]
# accents beyond the slide-change whooshes: (id, file, start, volume)
ACCENTS = [
    ("sfx-demo", "chime.mp3", 98.05, 0.4),
    ("sfx-raise", "ping.mp3", 184.5, 0.4),
    ("sfx-close", "impact-bass-1.mp3", 202.56, 0.32),
]


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return round(float(out), 3)


timing = json.load(open("assets/audio/vo/timing.json"))
slots, chapters, vo, sfx = [], [], [], []
for i, (cid, label, a, b) in enumerate(SLIDES):
    slots.append(f'      <div id="slot-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                 f'data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="{1 + i % 2}" '
                 f'data-width="1920" data-height="1080"></div>')
    if 0 < i < len(SLIDES) - 1:
        chapters.append(f'          <div class="chap" id="chap-{i}"><b>{i + 1:02d}</b>{label.upper()}</div>')
    if i > 0:
        sfx.append((f"sfx-cut-{i:02d}", "whoosh-short.mp3", round(a - 0.16, 2), 0.16))
for ln in timing["lines"]:
    vo.append(f'      <audio id="{ln["id"]}" src="assets/audio/vo/{ln["id"]}.wav" data-start="{ln["start"]}" '
              f'data-duration="{ln["dur"]}" data-track-index="21" data-volume="1" data-audio-group="voiceover"></audio>')
sfx += ACCENTS
lane_end = {22: -1.0, 23: -1.0}
sfx_tags = []
for sid, f, st, vol in sorted(sfx, key=lambda r: r[2]):
    d = dur(f"assets/audio/sfx/{f}")
    lane = 22 if lane_end[22] <= st else 23
    lane_end[lane] = st + d
    sfx_tags.append(f'      <audio id="{sid}" src="assets/audio/sfx/{f}" data-start="{st}" data-duration="{d}" '
                    f'data-track-index="{lane}" data-volume="{vol}" data-audio-group="sfx"></audio>')

chap_windows = json.dumps([[round(a, 2), round(b, 2)] for (_, _, a, b) in SLIDES[1:-1]])
template = open("tools/index.template.html").read()
html = (template.replace("{{SLOTS}}", "\n".join(slots))
        .replace("{{CHAPTERS}}", "\n".join(chapters))
        .replace("{{VO}}", "\n".join(vo))
        .replace("{{SFX}}", "\n".join(sfx_tags))
        .replace("{{CHAP_WINDOWS}}", chap_windows)
        .replace("{{TOTAL}}", str(TOTAL))
        .replace("{{SLIDE_COUNT}}", str(len(SLIDES) - 2)))
open("index.html", "w").write(html)
print("index.html written:", len(slots), "slides,", len(vo), "narration clips,", len(sfx_tags), "sfx")
