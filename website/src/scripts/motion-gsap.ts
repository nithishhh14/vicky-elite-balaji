import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Every animation below lives inside this matchMedia context, so under
// prefers-reduced-motion the callback never runs at all — elements keep
// their plain HTML/CSS state (visible, static), which is the correct
// fallback rather than a stripped-down version of the motion.
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // Hero entrance: direct children of [data-gsap-hero] stagger up and in.
  // fromTo (not from) because the CSS pre-hide already sets opacity:0 on
  // these elements before this script runs — gsap.from() would read that
  // as the element's "current" end state and animate 0 -> 0.
  document.querySelectorAll<HTMLElement>("[data-gsap-hero]").forEach((hero) => {
    const targets = hero.querySelectorAll(":scope > *");
    if (!targets.length) return;
    gsap.fromTo(
      targets,
      { y: 22, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.85, stagger: 0.1, ease: "power2.out", delay: Number(hero.dataset.gsapDelay ?? 0.1) }
    );
  });

  // Homepage opening: near-black, a thin gold line draws across, then the
  // showroom image settles in (slight scale-down = weight, not float).
  document.querySelectorAll<HTMLElement>("[data-hero-intro]").forEach((root) => {
    const line = root.querySelector<HTMLElement>("[data-intro-line]");
    const image = root.querySelector<HTMLElement>("[data-intro-image]");
    const tl = gsap.timeline({ defaults: { ease: "power2.inOut" } });
    if (line) {
      tl.fromTo(line, { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: 0.9 }).to(line, { opacity: 0, duration: 0.6 }, "+=0.05");
    }
    if (image) {
      tl.fromTo(image, { opacity: 0, scale: 1.07 }, { opacity: 1, scale: 1, duration: 1.8, ease: "power2.out" }, line ? 0.55 : 0);
    }
  });

  // Masked image reveal: the frame opens upward like a slab being uncovered.
  document.querySelectorAll<HTMLElement>("[data-gsap-reveal]").forEach((el) => {
    gsap.fromTo(
      el,
      { clipPath: "inset(0 0 100% 0)" },
      { clipPath: "inset(0 0 0% 0)", duration: 1.2, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 85%" } }
    );
  });

  // Gold rule that draws in beside section eyebrows.
  document.querySelectorAll<HTMLElement>("[data-gsap-line]").forEach((el) => {
    gsap.fromTo(el, { scaleX: 0 }, { scaleX: 1, transformOrigin: "left center", duration: 1, ease: "power2.out", scrollTrigger: { trigger: el, start: "top 90%" } });
  });

  // Coordinated staggered reveal for a group of siblings, in one motion
  // instead of each card firing its own reveal at a slightly different
  // scroll offset.
  document.querySelectorAll<HTMLElement>("[data-gsap-stagger]").forEach((group) => {
    const items = group.querySelectorAll(":scope > *");
    if (!items.length) return;
    gsap.fromTo(
      items,
      { y: 28, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        stagger: 0.07,
        ease: "power2.out",
        scrollTrigger: {
          trigger: group,
          start: "top 88%",
        },
      }
    );
  });

  // Generic layered-parallax treatment: any section with data-gsap-parallax
  // gets its data-parallax-photo layer scrubbed against scroll position.
  // Not tied to any one piece of content -- reusable wherever a section
  // wants a photo to drift rather than sit static.
  document.querySelectorAll<HTMLElement>("[data-gsap-parallax]").forEach((section) => {
    const photo = section.querySelector<HTMLElement>("[data-parallax-photo]");
    if (!photo) return;
    gsap.fromTo(
      photo,
      { yPercent: -12, scale: 1.1 },
      {
        yPercent: 12,
        scale: 1.16,
        ease: "none",
        scrollTrigger: { trigger: section, start: "top bottom", end: "bottom top", scrub: 0.6 },
      }
    );
  });

  // Subtle pointer-driven depth on the material grid panels, desktop only
  // (fine pointer). Touch devices keep the existing tap-to-navigate and
  // CSS hover-scale fallback instead.
  if (window.matchMedia("(pointer: fine)").matches) {
    document.querySelectorAll<HTMLElement>("[data-gsap-tilt]").forEach((panel) => {
      const img = panel.querySelector<HTMLElement>("img");
      if (!img) return;
      const strength = 10;
      // GSAP now owns this element's transform every frame; the CSS
      // hover-scale transition (kept as the touch/no-JS fallback) would
      // otherwise fight it for the same property.
      img.style.transition = "none";

      panel.addEventListener("mousemove", (e) => {
        const rect = panel.getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width - 0.5;
        const py = (e.clientY - rect.top) / rect.height - 0.5;
        gsap.to(img, {
          x: px * strength,
          y: py * strength,
          scale: 1.06,
          duration: 0.6,
          ease: "power2.out",
        });
      });

      panel.addEventListener("mouseleave", () => {
        gsap.to(img, { x: 0, y: 0, scale: 1, duration: 0.5, ease: "power2.out" });
      });
    });

    // Magnetic buttons: the element eases toward the cursor within a small
    // radius, then springs back on leave. Applied to primary CTAs only --
    // this is a "the button noticed you" flourish, not something every
    // link should do.
    document.querySelectorAll<HTMLElement>("[data-gsap-magnetic]").forEach((btn) => {
      const xTo = gsap.quickTo(btn, "x", { duration: 0.5, ease: "power3" });
      const yTo = gsap.quickTo(btn, "y", { duration: 0.5, ease: "power3" });

      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        xTo((e.clientX - rect.left - rect.width / 2) * 0.35);
        yTo((e.clientY - rect.top - rect.height / 2) * 0.35);
      });
      btn.addEventListener("mouseleave", () => {
        xTo(0);
        yTo(0);
      });
    });

    // Spotlight cards: a soft terracotta glow follows the cursor across the
    // card on hover (CSS radial-gradient driven by --spot-x/--spot-y, see
    // global.css). Pure cursor-tracking, no GSAP tween needed here.
    document.querySelectorAll<HTMLElement>("[data-gsap-spotlight]").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty("--spot-x", `${((e.clientX - rect.left) / rect.width) * 100}%`);
        card.style.setProperty("--spot-y", `${((e.clientY - rect.top) / rect.height) * 100}%`);
      });
    });
  }

  return () => {
    // gsap.matchMedia() reverts every tween/ScrollTrigger created in this
    // context automatically if the media query stops matching.
  };
});
