"""StarIQ deck pitch score — a calm, simple techno-space bed for the 3:31 deck video.

usage: python score.py out.wav [total_seconds]

D minor, 96 BPM (one bar = 2.5 s). Everything is synthesized here (no samples):
sub drone, detuned-saw pads, pluck arpeggio with ping-pong delay, pulse bass,
drums, satellite telemetry beeps, radio static, risers and impacts, all through
a synthetic stereo reverb. Seeded, so the same input always gives the same file.
"""
import sys

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
OUT = sys.argv[1]
TOTAL = float(sys.argv[2]) if len(sys.argv) > 2 else 210.7
N = int(TOTAL * SR)
BPM = 96
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(20261013)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def buf():
    return np.zeros((N, 2), dtype=np.float32)


def place(dst, x, t0, gain=1.0, pan=0.0):
    """Add mono or stereo x into dst at time t0 (seconds)."""
    i0 = int(round(t0 * SR))
    if i0 >= N:
        return
    if x.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4)
        r = np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * l, x * r], axis=1)
    j0 = max(0, -i0)
    i0 = max(0, i0)
    n = min(len(x) - j0, N - i0)
    if n > 0:
        dst[i0:i0 + n] += (x[j0:j0 + n] * gain).astype(np.float32)


def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    sus = max(0, n - a - d - r)
    e = np.concatenate([
        np.linspace(0, 1, max(a, 1), endpoint=False),
        np.linspace(1, s, max(d, 1), endpoint=False),
        np.full(sus, s),
        np.linspace(s, 0, max(r, 1)),
    ])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def lp(x, fc, order=2):
    sos = signal.butter(order, min(fc, SR * 0.45), 'low', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0).astype(np.float32)


def hp(x, fc, order=2):
    sos = signal.butter(order, fc, 'high', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0).astype(np.float32)


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, min(hi, SR * 0.45)], 'band', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0).astype(np.float32)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return signal.sawtooth(2 * np.pi * f * t + phase).astype(np.float32)


def curve(points):
    """Piecewise-linear automation over the whole timeline: [(t, v), ...]."""
    ts = np.array([p[0] for p in points])
    vs = np.array([p[1] for p in points])
    return np.interp(np.arange(N) / SR, ts, vs).astype(np.float32)


def reverb_ir(seconds=3.6, damp=5000):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-t * 6.9 / seconds)
    ir = np.stack([rng.standard_normal(n) * decay, rng.standard_normal(n) * decay], axis=1).astype(np.float32)
    ir = lp(ir, damp)
    ir[: int(0.012 * SR)] = 0  # pre-delay
    return ir / np.sqrt((ir ** 2).sum(axis=0))


IR = reverb_ir()


def reverb(x, wet=0.35):
    y = np.stack([signal.fftconvolve(x[:, c], IR[:, c])[:N] for c in range(2)], axis=1).astype(np.float32)
    return x * (1 - wet * 0.3) + y * wet


def delay_pingpong(x, t_delay, fb=0.38, taps=6):
    out = x.copy()
    d = int(t_delay * SR)
    g = 1.0
    for k in range(1, taps + 1):
        g *= fb
        sh = np.zeros_like(x)
        if d * k < N:
            src = x[: N - d * k]
            if k % 2:  # swap channels on odd taps
                src = src[:, ::-1]
            sh[d * k:] = src
        out += sh * g
    return out


# ---------------------------------------------------------------- harmony
CH = {
    'Dm': [50, 53, 57, 64], 'Bb': [46, 50, 53, 60], 'F': [41, 53, 57, 60], 'C': [48, 52, 55, 62],
    'Gm': [43, 50, 55, 58], 'Asus': [45, 50, 52, 57], 'A': [45, 49, 52, 57], 'D': [50, 54, 57, 64],
}
# Section map (seconds) follows the narration: title, sovereignty, race, reliability, pain,
# demo, solution, evidence, market, team, moat, ask, close.
SECTIONS = [
    (0.0, 9.5, ['Dm', 'Bb']),
    (9.5, 27.6, ['Dm', 'Bb', 'Gm', 'Asus']),
    (27.6, 49.6, ['Dm', 'Bb', 'F', 'C']),
    (49.6, 65.0, ['Gm', 'Asus', 'Gm', 'A']),
    (65.0, 93.5, ['Dm', 'Bb', 'Gm', 'Asus']),
    (93.5, 103.6, ['Bb', 'F', 'C', 'Dm']),
    (103.6, 121.9, ['Bb', 'F', 'C', 'Dm']),
    (121.9, 134.0, ['Dm', 'F', 'C', 'Gm']),
    (134.0, 148.7, ['Bb', 'C', 'Dm', 'F']),
    (148.7, 169.3, ['Dm', 'Bb', 'F', 'C']),
    (169.3, 182.8, ['Dm', 'Bb', 'F', 'C']),
    (182.8, 202.7, ['Bb', 'C', 'Dm', 'Asus']),
    (202.7, TOTAL, ['D']),
]
PROG = []
for a, b, seq in SECTIONS:
    t, k = a, 0
    step = BAR * 2 if len(seq) > 1 else (b - a)
    while t < b - 1e-6:
        e = min(b, t + step)
        PROG.append((t, e, seq[k % len(seq)]))
        t, k = e, k + 1


def chord_at(t):
    for a, b, c in PROG:
        if a <= t < b:
            return c
    return PROG[-1][2]


# ---------------------------------------------------------------- layers
def make_pad():
    out = buf()
    for a, b, c in PROG:
        dur = b - a + 1.6
        n = int(dur * SR)
        for i, m in enumerate(CH[c]):
            f = mtof(m)
            x = np.zeros(n, dtype=np.float32)
            for det in (-0.07, 0.0, 0.065):
                x += saw(f * 2 ** (det / 12), n, rng.uniform(0, 6.28))
            x /= 3
            x *= env_adsr(n, 1.1, 0.5, 0.85, 1.5)
            place(out, x, a - 0.4, 0.095, pan=(-0.5, 0.5, -0.25, 0.3)[i % 4])
    dark = lp(out, 900)
    bright = lp(out, 3200)
    b = curve([(0, 0.1), (9.5, 0.35), (27.6, 0.4), (49.6, 0.2), (65, 0.3), (93.5, 0.6), (121.9, 0.55),
               (148.7, 0.5), (182.8, 0.8), (202.7, 1.0), (TOTAL, 0.6)])[:, None]
    return dark * (1 - b) + bright * b


def make_sub():
    out = buf()
    for a, b, c in PROG:
        root = CH[c][0] - 12
        while mtof(root) > 70:
            root -= 12
        n = int((b - a + 0.8) * SR)
        t = np.arange(n) / SR
        x = np.sin(2 * np.pi * mtof(root) * t) * 0.8 + np.sin(2 * np.pi * mtof(root) * 2 * t) * 0.2
        x = np.tanh(x * 1.6) * env_adsr(n, 0.6, 0.2, 0.9, 0.8)
        place(out, x.astype(np.float32), a - 0.2, 0.12)
    return out


def pluck(f, dur=0.35, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = (saw(f, n) * 0.6 + np.sign(np.sin(2 * np.pi * f * t)) * 0.25).astype(np.float32)
    x *= np.exp(-t * (9 / dur * 0.35)).astype(np.float32)
    x = lp(x, 1600 + 2600 * bright)
    return x


def make_arp(sections):
    out = buf()
    pat = [0, 2, 1, 3, 2, 1, 3, 2]
    for (a, b, octv, bright, gain) in sections:
        t = a
        k = 0
        while t < b - 1e-6:
            c = CH[chord_at(t + 0.01)]
            notes = sorted(c[1:]) + [c[1] + 12]
            m = notes[pat[k % len(pat)] % len(notes)] + 12 * octv
            accent = 1.0 if k % 4 == 0 else 0.72
            place(out, pluck(mtof(m), 0.32, bright), t, gain * accent, pan=0.35 if k % 2 else -0.35)
            t += BEAT / 4
            k += 1
    return delay_pingpong(out, BEAT * 0.75, fb=0.33)


def make_bass(sections):
    out = buf()
    for (a, b, gain, octjump) in sections:
        t = a
        k = 0
        while t < b - 1e-6:
            c = CH[chord_at(t + 0.01)]
            root = c[0]
            while root > 45:
                root -= 12
            m = root + (12 if (octjump and k % 4 == 3) else 0)
            n = int(BEAT / 2 * SR * 0.95)
            tt = np.arange(n) / SR
            x = saw(mtof(m), n) * np.exp(-tt * 5.0).astype(np.float32)
            x = lp(x, 520)
            x += (np.sin(2 * np.pi * mtof(m) * tt) * np.exp(-tt * 3.0)).astype(np.float32) * 0.6
            place(out, np.tanh(x * 1.4), t, gain)
            t += BEAT / 2
            k += 1
    return out


def kick():
    n = int(0.40 * SR)
    t = np.arange(n) / SR
    f = 46 + 90 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 9.0) * 0.8
    x[:240] += rng.standard_normal(240) * np.linspace(0.4, 0, 240)
    return np.tanh(x * 1.5).astype(np.float32)


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    e = np.exp(-t * 18) + 0.6 * np.exp(-np.maximum(t - 0.011, 0) * 20) * (t > 0.011)
    return bp(noise * e.astype(np.float32), 900, 5200)


def hat(open_=False):
    n = int((0.16 if open_ else 0.05) * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n).astype(np.float32) * np.exp(-t * (18 if open_ else 70)).astype(np.float32)
    return hp(x, 7000)


def make_drums(sections):
    out = buf()
    K, C = kick(), clap()
    for (a, b, mode, gain) in sections:
        t = a
        k = 0
        while t < b - 1e-6:
            beat_in_bar = k % 4
            if mode in ('heart',) and beat_in_bar in (0, 2):
                place(out, K, t, gain * 0.9)
            if mode in ('four', 'full', 'peak'):
                place(out, K, t, gain)
            if mode in ('full', 'peak') and beat_in_bar in (1, 3):
                place(out, C, t, gain * 0.45)
            if mode in ('soft', 'four', 'full', 'peak'):
                for s in range(4):
                    acc = 0.5 if s == 2 else 0.22
                    place(out, hat(open_=(s == 2 and mode == 'peak')), t + s * BEAT / 4, gain * acc * (0.6 if mode == 'soft' else 1),
                          pan=0.25 if s % 2 else -0.15)
            t += BEAT
            k += 1
    return out


def blip(f, dur=0.06):
    n = int(dur * SR)
    t = np.arange(n) / SR
    mod = 1 + 0.004 * np.sin(2 * np.pi * 37 * t)
    x = np.sin(2 * np.pi * f * mod * t) * np.minimum(1, t / 0.004) * np.exp(-t * 18)
    return x.astype(np.float32)


def make_telemetry(windows):
    """Satellite telemetry: seeded beep patterns + a morse-like call sign."""
    out = buf()
    for (a, b, density, gain) in windows:
        t = a
        while t < b:
            if rng.random() < density:
                f = rng.choice([1568, 1760, 2093, 2349, 2637, 3136])
                for j in range(int(rng.integers(1, 4))):
                    place(out, blip(f * (1 + 0.5 * (j % 2)), 0.05), t + j * 0.07, gain, pan=float(rng.uniform(-0.8, 0.8)))
            t += BEAT / 4
    return out


def make_static(windows):
    out = buf()
    for (a, b, gain) in windows:
        n = int((b - a) * SR)
        x = rng.standard_normal(n).astype(np.float32)
        x = bp(x, 1800, 4200)
        gate = (np.sin(2 * np.pi * 0.7 * np.arange(n) / SR) * 0.5 + 0.5) ** 3
        x *= gate.astype(np.float32) * env_adsr(n, 0.8, 0.1, 1.0, 1.2)
        place(out, x, a, gain, pan=-0.2)
    return out


def riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    u = t / dur
    f = 180 * (2 ** (u * 4.2))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) * 0.35 + np.sin(ph * 1.5) * 0.2
    noise = rng.standard_normal(n)
    # sweep noise brightness by crossfading two filters
    nz = lp(noise.astype(np.float32), 900) * (1 - u) + hp(noise.astype(np.float32), 2500) * u
    x = (tone + nz * 0.5) * (u ** 2.2)
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return x.astype(np.float32)


def impact(size=1.0):
    n = int(3.2 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    boom = np.sin(ph) * np.exp(-t * 1.6)
    noise = lp(rng.standard_normal(n).astype(np.float32), 2500) * np.exp(-t * 7).astype(np.float32)
    shimmer = sum(np.sin(2 * np.pi * mtof(m) * t) for m in (74, 81, 86)) * np.exp(-t * 1.2) * 0.08
    return (np.tanh(boom * 1.8) * 0.9 + noise * 0.35 + shimmer) .astype(np.float32) * size


def glitch(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * 180 * t)) * (np.floor(t * 40) % 2)
    x = x + rng.standard_normal(n) * 0.4
    crush = np.repeat(x[::24], 24)[:n]
    return (hp(crush.astype(np.float32), 300) * np.exp(-t * 4)).astype(np.float32)


def eerie(a, b):
    n = int((b - a) * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 2349 * t) * 0.5 + np.sin(2 * np.pi * 2353.5 * t) * 0.5
    return (x * env_adsr(n, 0.4, 0.1, 1.0, 1.0)).astype(np.float32)


# ---------------------------------------------------------------- arrangement
pad = make_pad()
sub = make_sub()
arp = make_arp([
    (27.6, 49.6, 1, 0.45, 0.05),
    (93.5, 121.9, 2, 0.6, 0.05),
    (134.0, 182.8, 1, 0.55, 0.045),
    (182.8, 202.7, 1, 0.8, 0.065),
])
bass = make_bass([(27.6, 49.6, 0.08, False), (103.6, 121.9, 0.08, False), (182.8, 202.7, 0.11, True)])
drums = make_drums([(27.6, 49.6, 'soft', 0.22), (93.5, 103.6, 'soft', 0.2), (134.0, 148.7, 'soft', 0.2),
                    (182.8, 202.7, 'four', 0.3)])
tele = make_telemetry([(0.3, 9.5, 0.14, 0.035), (202.8, TOTAL - 0.5, 0.12, 0.03)])
static = make_static([(0.0, 9.0, 0.03)])

fx = buf()
place(fx, riser(2.6), 93.5 - 2.6, 0.18)
place(fx, impact(0.5), 93.5, 0.28)
place(fx, riser(2.8), 182.8 - 2.8, 0.2)
place(fx, impact(0.6), 182.8, 0.32)
place(fx, riser(2.8), 202.7 - 2.8, 0.22)
place(fx, impact(0.9), 202.7, 0.45)

music_gain = curve([(0, 0.0), (1.2, 1.0), (49.4, 1.0), (49.8, 0.7), (64.8, 0.7), (65.2, 1.0),
                    (TOTAL - 4.0, 1.0), (TOTAL, 0.0)])[:, None]

dry = (pad + sub + arp + bass + drums) * music_gain
wet_send = pad * 0.9 + arp * 0.8 + tele + fx * 0.6 + static
mix = dry + tele + static + fx
mix = mix + (reverb(wet_send, wet=1.0) - wet_send * 0.7) * 0.42

# master: tidy the lows, lift the air, soft clip, normalize to about -16 dBFS RMS
mix = hp(mix, 32)
mix = mix - lp(mix, 140) * 0.35 + hp(mix, 4500) * 0.35
mix = np.tanh(mix * 1.15) / 1.15
rms = np.sqrt(np.mean(mix ** 2))
mix *= (10 ** (-16 / 20)) / max(rms, 1e-9)
peak = np.abs(mix).max()
if peak > 0.97:
    mix *= 0.97 / peak
fade = int(0.05 * SR)
mix[:fade] *= np.linspace(0, 1, fade)[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype='PCM_24')
print('wrote', OUT, f'{TOTAL:.2f}s', 'peak', float(np.abs(mix).max()), 'rms dB', 20 * np.log10(np.sqrt(np.mean(mix ** 2))))
