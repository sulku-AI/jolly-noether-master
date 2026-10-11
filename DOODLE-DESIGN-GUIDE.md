# HopeMUN Decorative Asset Guide

## Research Basis

- [Nielsen Norman Group: Visual Hierarchy in UX](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) recommends controlling emphasis through contrast, scale, and grouping. It also describes the squint test: blur the page and check that the intended content hierarchy still wins.
- [W3C WAI: Decorative Images](https://www.w3.org/WAI/tutorials/images/decorative/) says decorative imagery should use `alt=""` so it does not add noise for screen-reader users.
- [MDN: `mix-blend-mode`](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode) explains that blend modes combine an element with its backdrop; they do not remove pixels baked into a JPEG. Blend modes also create stacking contexts, so use them intentionally.
- [Pillow: Transparency](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#transparency) documents the RGBA alpha band used for genuine transparency.

## Background Removal

1. Keep the supplied JPEG/JFIF originals unchanged under `assets/doodle-elements/`.
2. Run `python3 -m pip install -r requirements-assets.txt` once for the asset tool.
3. Run `python3 tools/remove_doodle_backgrounds.py --only asset-2.jpg asset-3.jpg asset-13.jpg` for the pilot set.
4. Inspect each PNG over plum, lime, and paper backgrounds. Confirm there is no rectangular matte, fringe, missing outline, or lost enclosed white detail before processing the rest.
5. Run `python3 tools/remove_doodle_backgrounds.py` to process the unique `.doodle` image sources in `index.html`. It reads each original from `data-source`, writes the PNG to that image's `src` path, and removes stale PNG derivatives from the generated output folder.
6. Update those `<img>` paths to the PNG outputs only after the pilot passes. Keep the source files as the recoverable originals.

The processor removes only light, neutral pixels connected to the image edge (except the known checkerboard sample, which is explicitly color-keyed). A narrow edge band is decontaminated against the sampled matte color, then the cutout is trimmed with transparent padding. If a source uses a non-neutral backdrop, do not widen the global threshold; add a source-specific mask rule and visually inspect that file instead. One paper asset with an embedded stock-site watermark was excluded from the page.

## Placement And Hierarchy

1. Start with the page content hierarchy: the HopeMUN identity and mission first, conference information next, decorative material last.
2. Use one or two accent assets in each visual region, then vary their position, angle, and scale across sections. Do not anchor every element to the same corner.
3. Let decorative pieces extend into margins or section backgrounds, but keep headings, paragraphs, controls, and the Ata donation message clear of their silhouettes.
4. Prefer transparent PNGs over `mix-blend-mode` as a workaround for opaque backgrounds. Use blend modes only when a specific, tested effect is intended.
5. Keep every purely decorative image at `alt=""`; give meaningful text alternatives only to imagery that adds information.

## Outside-User Review

1. Open the page at 1440px and 390px widths with the menu closed and the page at the top.
2. Give the first viewport a three-second scan: the conference name, HopeMUN mark, and promise to support Ata should be immediate; no doodle should read as the primary message.
3. Apply the squint test to the hero, letters, conference, donation, and application sections. Headings and actions should remain the strongest shapes; reduce or remove any sticker that wins attention instead.
4. Read every section at normal scale. No doodle may cross text, buttons, focus outlines, or the `#atayaumutol` message.
5. Inspect all transparent cutouts over dark plum, lime, and light paper. Reject white halos, leftover rectangles, checkerboard pixels, clipped outlines, or unexpectedly erased white details.
6. Check 390px mobile: no horizontal scrolling, no text collision, and doodles stay within their owning section.
7. Check the first-visit experience and applications path from the viewpoint of someone unfamiliar with HopeMUN. If the visual decoration delays understanding or finding Applications, reduce the decoration before calling it done.

In `index.html`, each active cutout keeps its original JPEG/JFIF in a `data-source` attribute. The public `src` points to the transparent PNG, so rerunning the processor always starts from the untouched source and writes to the same published path.