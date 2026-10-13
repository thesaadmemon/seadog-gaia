# STARIQ — orbital elevator pitch (HyperFrames)

A ≈2-minute narrated motion-graphics pitch built from the STARIQ five-minute investor guide.
Everything is reproducible from this folder.

| Path | What it is |
| --- | --- |
| `index.html` | Root composition: scene slots, mission HUD, grain, narration / score / SFX mix |
| `compositions/s01…s11-*.html` | One sub-composition per story beat |
| `broll/index.html` | Three.js orbital b-roll (Earth, atmosphere, Landsat 8, constellation) |
| `assets/broll/orbital.mp4` | Rendered b-roll used as scene backgrounds |
| `assets/audio/vo/` | Narration clips + `timing.json` |
| `assets/audio/score.wav` | Procedural techno-space score |
| `tools/` | `tts.py` (Kokoro narration), `phrases.py` (cue sheet), `score.py` (music) |
| `renders/` | Draft and final MP4s |

## Rebuild

```bash
# narration (local Kokoro; needs kokoro-onnx + soundfile in the python env)
python tools/tts.py tools/narration.json assets/audio/vo_raw af_heart 1.05 3.2
# master each clip (EQ, compression, -16 LUFS), then the phrase cue sheet
python tools/phrases.py assets/audio/vo/timing.json assets/audio/vo tools/cues.json
# score, written to the same timing
python tools/score.py assets/audio/score.wav 124.6
# b-roll, then the film
(cd broll && npx hyperframes render --output ../assets/broll/orbital.mp4)
npx hyperframes render --output renders/stariq-pitch.mp4
```

## Credits

- Earth photograph (Apollo) and Landsat 8 model: NASA 3D Resources — public domain.
- Earth day / night / cloud textures and Milky Way cube map: three.js examples (NASA Blue / Black Marble derived).
- Sound effects: HyperFrames media-use bundle, Pixabay Content License (`assets/audio/sfx/CREDITS.md`).
- Brand imagery, portrait and partner marks: the STARIQ investor brief.
- Fonts: Manrope (from the brief), Orbitron (OFL, @fontsource), JetBrains Mono (bundled by HyperFrames).
