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
      { y: 0, opacity: 1, duration: 0.85, stagger: 0.1, ease: "power2.out", delay: 0.1 }
    );
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
  }

  return () => {
    // gsap.matchMedia() reverts every tween/ScrollTrigger created in this
    // context automatically if the media query stops matching.
  };
});
