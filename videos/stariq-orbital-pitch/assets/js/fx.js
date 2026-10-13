// STARIQ motion helpers — deterministic text effects shared by every scene.
// Every effect is a pure function of timeline progress, so any seek lands the same frame.
(function () {
  const C = window.SQ_CUES;
  const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+<>/=";

  function hash(n) {
    n = (n ^ 61) ^ (n >>> 16);
    n = n + (n << 3);
    n = n ^ (n >>> 4);
    n = Math.imul(n, 0x27d4eb2d);
    n = n ^ (n >>> 15);
    return (n >>> 0) / 4294967296;
  }

  window.SQ = {
    hash,
    // Scene-local cue lookup: const at = SQ.local(sceneStart); at("vo04", 1) -> phrase 1 start.
    local(t0) {
      return (id, k = 0) => (k === "end" ? C.lines[id].e : C.phrases[id][k][0]) - t0;
    },
    splitWords(el) {
      const out = [];
      const walk = (node) => {
        Array.from(node.childNodes).forEach((ch) => {
          if (ch.nodeType === 3) {
            const frag = document.createDocumentFragment();
            ch.textContent.split(/(\s+)/).forEach((p) => {
              if (!p) return;
              if (/^\s+$/.test(p)) {
                frag.appendChild(document.createTextNode(" "));
              } else {
                const s = document.createElement("span");
                s.className = "word";
                s.textContent = p;
                frag.appendChild(s);
                out.push(s);
              }
            });
            node.replaceChild(frag, ch);
          } else if (ch.nodeType === 1) {
            walk(ch);
          }
        });
      };
      walk(el);
      return out;
    },
    splitChars(el) {
      const text = el.textContent;
      el.textContent = "";
      return Array.from(text).map((c) => {
        const s = document.createElement("span");
        s.className = "word";
        s.textContent = c === " " ? " " : c;
        el.appendChild(s);
        return s;
      });
    },
    // Decode-style reveal: glyph noise resolving left to right into the final text.
    scramble(tl, el, at, dur, seed = 1) {
      const final = el.getAttribute("data-text") || el.textContent;
      el.setAttribute("data-text", final);
      el.textContent = "";
      const proxy = { p: 0 };
      tl.fromTo(
        proxy,
        { p: 0 },
        {
          p: 1,
          duration: dur,
          ease: "none",
          onUpdate() {
            const p = proxy.p;
            const n = final.length;
            const frame = Math.floor(p * dur * 30);
            const head = p * (n + 5) - 5;
            let s = "";
            for (let i = 0; i < n; i++) {
              const ch = final[i];
              if (i < head) s += ch;
              else if (i < head + 5) s += ch === " " ? " " : GLYPHS[Math.floor(hash(i * 131 + frame * 7 + seed) * GLYPHS.length)];
            }
            el.textContent = s;
          },
        },
        at,
      );
    },
    // Number count-up with a formatter; text steps only when the formatted value changes.
    count(tl, el, from, to, at, dur, fmt, ease = "power2.out") {
      const proxy = { v: from };
      el.textContent = fmt(from);
      let last = el.textContent;
      tl.fromTo(
        proxy,
        { v: from },
        {
          v: to,
          duration: dur,
          ease,
          onUpdate() {
            const s = fmt(proxy.v);
            if (s !== last) {
              el.textContent = s;
              last = s;
            }
          },
        },
        at,
      );
    },
  };
})();
