"""Per-line Kokoro narration (local, offline) + a timing sheet.

usage: python tts.py narration.json out_dir voice speed tail
Writes out_dir/<id>.wav and out_dir/timing.json: each line's start (after its
lead-in `gap`) and duration on the master timeline, plus total length.
"""
import json, os, sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

src, out, voice, speed, tail = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
os.makedirs(out, exist_ok=True)
cache = os.path.expanduser('~/.cache/hyperframes/tts')
k = Kokoro(f'{cache}/models/kokoro-v1.0.onnx', f'{cache}/voices/voices-v1.0.bin')
t = 0.0
rows = []
for ln in json.load(open(src)):
    audio, sr = k.create(ln['text'], voice=voice, speed=ln.get('speed', speed), lang='en-us')
    audio = np.asarray(audio, dtype=np.float32)
    f = int(0.006 * sr)
    audio[:f] *= np.linspace(0, 1, f)
    audio[-f:] *= np.linspace(1, 0, f)
    sf.write(os.path.join(out, ln['id'] + '.wav'), audio, sr, subtype='PCM_16')
    dur = len(audio) / sr
    t += ln['gap']
    rows.append({'id': ln['id'], 'scene': ln['scene'], 'start': round(t, 3), 'dur': round(dur, 3), 'end': round(t + dur, 3), 'text': ln['text']})
    t += dur
total = round(t + tail, 2)
json.dump({'voice': voice, 'speed': speed, 'total': total, 'lines': rows}, open(os.path.join(out, 'timing.json'), 'w'), indent=1)
for r in rows:
    print(f"{r['id']:6s} {r['scene']:9s} {r['start']:7.2f} -> {r['end']:7.2f}  ({r['dur']:.2f}s)")
print('TOTAL', total)
