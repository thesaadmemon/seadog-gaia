---
workflow: general-video
flow: automation
storyboard: no
message: "STARIQ makes commercial AI hardware reliable in orbit: hardened Linux, AI fault protection and automatic recovery in one platform."
destination: investor pitch (YouTube / embed / meeting screen)
aspect: "16:9"
language: en
audience: seed investors
length: "≈2:00"
angle: narrative elevator pitch
---

# STARIQ — two-minute orbital elevator pitch

## Intent

A rich motion-graphics elevator pitch with a techno-space satellite look: animated titles and
kinetic text, real imagery in motion, a futuristic space score and a convincing narrated story.
Source of truth for every claim is the founder's "STARIQ — Five-Minute Investor Guide" (October 2026).

The user asked for a draft first and an edit pass after it; both are rendered (`renders/`).

## Story spine

Orbit hook → title → onboard AI → the problem (radiation, crash, silent corruption) → the
evidence (IEEE / NASA NTRS study, 2–3× uptime) → the solution (hardened Linux + AI protection +
automatic recovery) → why now (Google, Starcloud, SpaceX, $1T space economy) → business
(compute modules, licences, Satellite Zero; EO, disaster monitoring, comms) → team → the
€1.5M ask with milestones → close.

## Assets

- Brief imagery: AI-satellite and AI-chip concept renders (background removed), founder
  portrait, NASA / ESA / Google / SpaceX marks, Linux Tux, all from the investor brief.
- Real imagery: Apollo photograph of Earth (NASA 3D Resources, public domain); Earth day /
  night / cloud textures and Milky Way sky (three.js examples, NASA Blue/Black Marble based);
  Landsat 8 3D model (NASA 3D Resources, public domain), rendered as photoreal orbital b-roll.
- Voice: local Kokoro-82M, voice `af_heart` (offline; not signed in to HeyGen).
- Music: procedural techno-space score written to the narration timing (`tools/score.py`).
- SFX: HyperFrames media-use bundle (Pixabay Content License).

## Customizations

- Brand: Manrope (from the brief), brief blue `#1556e8`, teal and gold accents; Orbitron for
  title moments; JetBrains Mono HUD telemetry.
- Persistent mission HUD (clock, chapter, telemetry, progress) over the story scenes.

## Notes

- Disclaimers carried from the brief: research result, not a product benchmark; integrated
  performance to be qualified; planned milestones; founder-supplied credentials.
