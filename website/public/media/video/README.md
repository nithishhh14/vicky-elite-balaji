Drop real video files here (e.g. `showroom-loop.mp4`).

Wire one in via the `AmbientVideo` component (`src/components/AmbientVideo.astro`):

```astro
<AmbientVideo poster="/media/..." posterAlt="..." src="/media/video/showroom-loop.mp4" />
```

No video is generated or faked here — this folder stays empty until a real file exists.
