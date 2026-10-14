# Draft → edit pass

`renders/stariq-pitch-draft-v1.mp4` is the first full cut. It was reviewed frame by frame
(contact sheets plus full-resolution stills of every scene), checked with `hyperframes check`
and measured for loudness. These changes make up `renders/stariq-pitch-final.mp4`.

## Picture

| Scene | Draft issue | Edit |
| --- | --- | --- |
| 02 Title | Wordmark landed without a "hit" | Added an anamorphic light streak through the wordmark as it lands |
| 03 Onboard AI | Tracking reticle sat ~120 px below the satellite; copy sat in the satellite's flight path | Re-measured the satellite's screen path on the rendered b-roll and re-fit the reticle; moved the copy to the lower left; softer glowing data packet; the tag hands off before it reaches the copy |
| 04 Problem | "Linux can crash." overprinted the previous headline and bit panel | The crash beat now owns the frame. The flipped bit's old value clears, and the corruption dashboard is centred |
| 05 Evidence | "2–3×" wrapped onto two lines | Wider value column, kept on one line |
| 06 Solution | Recovery-loop labels collided with the centre lockup | Narrower nodes, compact centre label |
| 07 Why now | Satellite counter unreadable over the bright globe; Starcloud mark overflowed its box | Counter on its own panel; resized mark; larger Google mark |
| 09–10 Team / Ask | Night-side Earth almost invisible under heavy shading | Lighter shades so the city lights read |
| Global | HUD clock and telemetry lost over bright Earth shots | Soft top and bottom legibility bands; brighter telemetry text |
| 01 Open | Kicker repeated the HUD chapter label | Kicker now gives altitude and orbit period |

## Sound

- Draft mix: −15.5 LUFS integrated, voice about 11 dB above the music between lines. Clear, but the
  score felt too timid for the futuristic tone. The edit raises the score about 3 dB. The voice-over
  carve still opens space under every narration line.

## Validation

- `hyperframes lint`: 0 errors.
- `hyperframes check` by range (0–13, 13–50, 50–66, 66–83, 83–96, 90–124.5 s): runtime, layout, motion
  and contrast all pass. What remains is informational: intentional crossfades, and rotating rings that
  overflow on purpose. The single full-length check times out on this machine's software GL, so it
  was run in ranges.
