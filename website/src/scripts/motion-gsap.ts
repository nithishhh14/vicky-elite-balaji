import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Every animation below lives inside a matchMedia context, so under
// prefers-reduced-motion the callbacks never run at all — elements keep
// their plain HTML/CSS state (visible, static), which is the correct
// fallback rather than a stripped-down version of the motion.
//
// Motion budget: high-motion moments are the hero, material worlds, the
// custom stonecraft story and big image moments. Cards, filters and dialogs
// get CSS micro-interactions (global.css). Body copy stays still.
const mm = gsap.matchMedia();
const EASE = "power3.out";

// Touch: lets CSS :active states fire on iOS for tap feedback.
document.addEventListener("touchstart", () => {}, { passive: true });

// ───────────── Desktop-only: pinned horizontal story (Custom Stonecraft) ─────────────
// The section holds still while the steps travel sideways. Each step's image
// opens from a mask and settles from a slight scale as it crosses in, its
// text rises after it, and a step counter + progress rule track the journey.
// On touch/mobile the track stays a native swipe strip.
mm.add("(min-width: 1024px) and (prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll<HTMLElement>("[data-gsap-hscroll]").forEach((section) => {
    const track = section.querySelector<HTMLElement>("[data-hscroll-track]");
    const progress = section.querySelector<HTMLElement>("[data-hscroll-progress]");
    const counter = section.querySelector<HTMLElement>("[data-hscroll-counter]");
    if (!track) return;
    track.style.overflow = "visible";
    const distance = () => Math.max(0, track.scrollWidth - track.clientWidth);
    if (distance() < 40) return;
    const steps = gsap.utils.toArray<HTMLElement>(track.children);

    const tween = gsap.to(track, {
      x: () => -distance(),
      ease: "none",
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 0.8,
        invalidateOnRefresh: true,
        onUpdate: (self) => {
          if (progress) progress.style.transform = `scaleX(${self.progress})`;
          if (counter) {
            const n = Math.min(steps.length, Math.floor(self.progress * (steps.length - 0.001)) + 1);
            const label = String(n).padStart(2, "0");
            if (counter.textContent !== label) counter.textContent = label;
          }
        },
      },
    });

    steps.forEach((step, i) => {
      const frame = step.querySelector<HTMLElement>("[data-step-frame]");
      const img = frame?.querySelector("img, video");
      const text = step.querySelectorAll<HTMLElement>("[data-step-text]");
      // Steps already on screen at pin start stay fully revealed.
      if (i < 2) return;
      const st = { trigger: step, containerAnimation: tween, start: "left 92%", end: "left 45%", scrub: true };
      if (frame) gsap.fromTo(frame, { clipPath: "inset(0 0 0 35%)" }, { clipPath: "inset(0 0 0 0%)", ease: "none", scrollTrigger: st });
      if (img) gsap.fromTo(img, { scale: 1.14 }, { scale: 1, ease: "none", scrollTrigger: st });
      if (text.length) gsap.fromTo(text, { y: 24, opacity: 0.2 }, { y: 0, opacity: 1, stagger: 0.08, ease: "none", scrollTrigger: { ...st, start: "left 80%", end: "left 40%" } });
    });

    return () => {
      tween.scrollTrigger?.kill();
      tween.kill();
      track.style.overflow = "";
      gsap.set(track, { x: 0 });
    };
  });
});

// ───────────── All motion-allowed widths ─────────────
mm.add(
  {
    motion: "(prefers-reduced-motion: no-preference)",
    phone: "(max-width: 767px)",
    fine: "(hover: hover) and (pointer: fine)",
  },
  (ctx) => {
    const { motion, phone, fine } = ctx.conditions as { motion: boolean; phone: boolean; fine: boolean };
    if (!motion) return;
    // Phones: faster, lighter, no pointer effects.
    const speed = phone ? 0.7 : 1;

    // Page heroes (non-home): direct children stagger up and in.
    // fromTo (not from): the CSS pre-hide already sets opacity:0.
    document.querySelectorAll<HTMLElement>("[data-gsap-hero]").forEach((hero) => {
      const targets = hero.querySelectorAll(":scope > *");
      if (!targets.length) return;
      gsap.fromTo(
        targets,
        { y: 22, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.85 * speed, stagger: 0.1 * speed, ease: "power2.out", delay: Number(hero.dataset.gsapDelay ?? 0.1) }
      );
    });

    // Homepage opening, in one calm sequence:
    // dark field → gold line → image resolves → texture → eyebrow → headline
    // lines → supporting line → CTAs → trust panel → caption → slow drift.
    document.querySelectorAll<HTMLElement>("[data-hero-intro]").forEach((root) => {
      const q = <T extends Element = HTMLElement>(s: string) => root.querySelector<T>(s);
      const line = q("[data-intro-line]");
      const image = q("[data-intro-image]");
      const texture = q("[data-hero-texture]");
      const lines = root.querySelectorAll("[data-hero-line]");
      const seq = (name: string) => q(`[data-hero-seq="${name}"]`);
      const rule = q("[data-hero-rule]");
      const s = speed;

      const tl = gsap.timeline({ defaults: { ease: EASE } });
      if (line) tl.fromTo(line, { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.9 * s, ease: "power2.inOut" }).to(line, { opacity: 0, duration: 0.6 * s }, ">-0.05");
      if (image) tl.fromTo(image, { opacity: 0, scale: 1.08, filter: "brightness(0.55)" }, { opacity: 1, scale: 1, filter: "brightness(1)", duration: 2 * s, ease: "power2.out" }, 0.5 * s);
      if (texture) tl.fromTo(texture, { opacity: 0 }, { opacity: 1, duration: 1.4 * s, ease: "power1.out" }, 0.8 * s);
      const eyebrow = seq("eyebrow");
      if (eyebrow) tl.fromTo(eyebrow, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.8 * s }, 1.0 * s);
      if (lines.length) {
        gsap.set(lines, { yPercent: 110, opacity: 1 });
        tl.to(lines, { yPercent: 0, duration: 1.05 * s, stagger: 0.12 * s, ease: "power4.out" }, 1.1 * s);
      }
      const support = seq("support");
      if (support) tl.fromTo(support, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.9 * s }, 1.55 * s);
      const cta = seq("cta");
      if (cta) tl.fromTo(cta, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.9 * s }, 1.75 * s);
      const trust = seq("trust");
      if (trust) tl.fromTo(trust, { opacity: 0, x: 16 }, { opacity: 1, x: 0, duration: 1 * s }, 2.05 * s);
      if (rule) tl.fromTo(rule, { scaleX: 0 }, { scaleX: 1, duration: 0.9 * s, ease: "power2.inOut" }, 2.25 * s);
      const caption = seq("caption");
      if (caption) tl.fromTo(caption, { opacity: 0 }, { opacity: 1, duration: 1 * s }, 2.4 * s);

      // Ambient drift after the entrance; paused whenever the hero is off-screen.
      if (image && !phone) {
        const drift = gsap.to(image, { scale: 1.045, xPercent: -1.2, duration: 18, ease: "sine.inOut", yoyo: true, repeat: -1, paused: true });
        tl.eventCallback("onComplete", () => drift.play());
        ScrollTrigger.create({ trigger: root, start: "top bottom", end: "bottom top", onToggle: (self) => (self.isActive && tl.progress() === 1 ? drift.play() : drift.pause()) });
      }
    });

    // Masked image reveal: the frame opens upward like a slab being
    // uncovered, while the image inside settles from a slight scale.
    document.querySelectorAll<HTMLElement>("[data-gsap-reveal]").forEach((el) => {
      const img = el.tagName === "IMG" ? null : el.querySelector("img");
      const st = { trigger: el, start: "top 86%", once: true };
      gsap.fromTo(el, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 1.2 * speed, ease: "power3.out", scrollTrigger: st });
      gsap.fromTo(img ?? el, { scale: 1.06 }, { scale: 1, duration: 1.6 * speed, ease: "power2.out", scrollTrigger: st, clearProps: "scale,transform" });
    });

    // Batched image reveals for large grids (gallery, specimens): items below
    // the fold start masked; items already visible are left alone.
    const batchItems = gsap.utils.toArray<HTMLElement>("[data-reveal-img]");
    if (batchItems.length) {
      const below = batchItems.filter((el) => el.getBoundingClientRect().top > window.innerHeight * 0.92);
      gsap.set(below, { opacity: 0, y: 26, clipPath: "inset(0 0 14% 0)" });
      ScrollTrigger.batch(below, {
        start: "top 92%",
        once: true,
        onEnter: (els) =>
          gsap.to(els, { opacity: 1, y: 0, clipPath: "inset(0 0 0% 0)", duration: 0.9 * speed, ease: EASE, stagger: 0.06, clearProps: "clipPath,transform" }),
      });
    }

    // Gold rule that draws in beside section eyebrows.
    document.querySelectorAll<HTMLElement>("[data-gsap-line]").forEach((el) => {
      gsap.fromTo(el, { scaleX: 0 }, { scaleX: 1, transformOrigin: "left center", duration: 1 * speed, ease: "power2.out", scrollTrigger: { trigger: el, start: "top 90%", once: true } });
    });

    // Coordinated staggered reveal for a group of siblings.
    document.querySelectorAll<HTMLElement>("[data-gsap-stagger]").forEach((group) => {
      const items = group.querySelectorAll(":scope > *");
      if (!items.length) return;
      gsap.fromTo(
        items,
        { y: phone ? 16 : 28, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.7 * speed, stagger: 0.07 * speed, ease: "power2.out", clearProps: "transform", scrollTrigger: { trigger: group, start: "top 88%", once: true } }
      );
    });

    // Layered parallax: a data-parallax-photo layer drifts against scroll.
    document.querySelectorAll<HTMLElement>("[data-gsap-parallax]").forEach((section) => {
      const photo = section.querySelector<HTMLElement>("[data-parallax-photo]");
      if (!photo) return;
      const amount = phone ? 5 : 10;
      gsap.fromTo(photo, { yPercent: -amount, scale: 1.12 }, { yPercent: amount, scale: 1.12, ease: "none", scrollTrigger: { trigger: section, start: "top bottom", end: "bottom top", scrub: 0.6 } });
    });

    // Scroll momentum: large image cards drift a few px against fast
    // scrolling and settle when it stops. Cards only, never text blocks.
    if (!phone) {
      const drifters = gsap.utils.toArray<HTMLElement>("[data-velocity]");
      if (drifters.length) {
        const setters = drifters.map((el, i) => gsap.quickTo(el, "y", { duration: 0.9 + (i % 4) * 0.12, ease: "power3.out" }));
        let settle: number | undefined;
        ScrollTrigger.create({
          start: 0,
          end: "max",
          onUpdate: (self) => {
            const v = gsap.utils.clamp(-7, 7, self.getVelocity() / -260);
            setters.forEach((set) => set(v));
            window.clearTimeout(settle);
            settle = window.setTimeout(() => setters.forEach((set) => set(0)), 140);
          },
        });
      }
    }

    // ───── Fine pointer only (no phones, no touch) ─────
    if (!fine || phone) return;

    // Material depth: a large image follows the cursor by a few px.
    document.querySelectorAll<HTMLElement>("[data-depth]").forEach((frame) => {
      const layer = frame.querySelector<HTMLElement>("[data-intro-image], img, [data-ambient]") ?? frame.firstElementChild as HTMLElement | null;
      if (!layer) return;
      const target = frame.hasAttribute("data-hero-depth") ? frame : layer;
      const xTo = gsap.quickTo(target, "x", { duration: 1.1, ease: "power3.out" });
      const yTo = gsap.quickTo(target, "y", { duration: 1.1, ease: "power3.out" });
      const strength = Number(frame.dataset.depth || 10);
      gsap.set(target, { scale: 1.03 });
      const host = frame.closest("section") ?? frame;
      host.addEventListener("pointermove", (e) => {
        const r = host.getBoundingClientRect();
        xTo(((e.clientX - r.left) / r.width - 0.5) * -strength);
        yTo(((e.clientY - r.top) / r.height - 0.5) * -strength);
      });
      host.addEventListener("pointerleave", () => {
        xTo(0);
        yTo(0);
      });
    });

    // Tilt panels (material grids).
    document.querySelectorAll<HTMLElement>("[data-gsap-tilt]").forEach((panel) => {
      const img = panel.querySelector<HTMLElement>("img");
      if (!img) return;
      img.style.transition = "none";
      const xTo = gsap.quickTo(img, "x", { duration: 0.6, ease: "power2.out" });
      const yTo = gsap.quickTo(img, "y", { duration: 0.6, ease: "power2.out" });
      panel.addEventListener("mousemove", (e) => {
        const rect = panel.getBoundingClientRect();
        xTo(((e.clientX - rect.left) / rect.width - 0.5) * 10);
        yTo(((e.clientY - rect.top) / rect.height - 0.5) * 10);
      });
      panel.addEventListener("mouseleave", () => {
        xTo(0);
        yTo(0);
      });
    });

    // Magnetic buttons: primary CTAs ease toward the cursor within a small radius.
    document.querySelectorAll<HTMLElement>("[data-gsap-magnetic]").forEach((btn) => {
      const xTo = gsap.quickTo(btn, "x", { duration: 0.5, ease: "power3" });
      const yTo = gsap.quickTo(btn, "y", { duration: 0.5, ease: "power3" });
      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        xTo((e.clientX - rect.left - rect.width / 2) * 0.25);
        yTo((e.clientY - rect.top - rect.height / 2) * 0.25);
      });
      btn.addEventListener("mouseleave", () => {
        xTo(0);
        yTo(0);
      });
    });

    // The cursor is a light. Both the spotlight cards and the sheen on
    // imagery read the same two custom properties, so there is one gesture
    // across the site rather than two competing ones.
    //
    // Writes are coalesced into a frame: mousemove fires far faster than the
    // screen refreshes, and setting a custom property per event is work the
    // browser then throws away.
    const lit = document.querySelectorAll<HTMLElement>("[data-gsap-spotlight], [data-sheen]");
    lit.forEach((el) => {
      let queued = false;
      let px = 0;
      let py = 0;
      const paint = () => {
        queued = false;
        el.style.setProperty("--spot-x", `${px}%`);
        el.style.setProperty("--spot-y", `${py}%`);
      };
      el.addEventListener(
        "mousemove",
        (e) => {
          const rect = el.getBoundingClientRect();
          px = ((e.clientX - rect.left) / rect.width) * 100;
          py = ((e.clientY - rect.top) / rect.height) * 100;
          if (!queued) {
            queued = true;
            requestAnimationFrame(paint);
          }
        },
        { passive: true }
      );
    });
  }
);

// Layout changes after load (fonts, lazy images) can move trigger points.
window.addEventListener("load", () => ScrollTrigger.refresh());
