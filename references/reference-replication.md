# Reference Replication

Use this branch when the user asks to 复刻, recreate, reproduce, imitate, match, or closely reference an Amazon main image, secondary image, or A+ design. The task ends with rendered files unless the user explicitly requests analysis or prompts only.

## Two truth chains

Keep these sources separate throughout production:

- **Reference-design truth:** aspect ratio, composition, grid, camera language, product placement, background, lighting, shadow, color system, typography hierarchy, icon style, decorative elements, spacing, and module rhythm.
- **Product truth:** silhouette, proportions, parts, included quantity, accessories, controls, labels, logo, material, finish, colorway, use, packaging, and supported claims.

The reference controls presentation. The user's authoritative product sources control the goods. If they conflict, preserve product truth and adapt the design.

## Intake for replication

Identify:

- Which image or page is the reference for each requested output.
- Whether the user wants close layout reconstruction, a looser style match, or only selected elements.
- Target marketplace, image role, dimensions, language, and number of outputs.
- Authoritative product views, brand assets, required copy, and material reference.
- Which reference elements must be replaced: competitor product, logo, text, badges, dimensions, claims, packaging, and accessories.

If the desired fidelity level is not stated, default to close composition/style reconstruction with the user's product facts and branding.

## Build a replication map

Decompose the reference before generation:

| Layer | Extract from reference | Replace or verify |
|---|---|---|
| Canvas | Aspect ratio, margins, safe areas | Target module dimensions |
| Composition | Grid, focal point, relative scale, alignment | User product proportions and count |
| Camera | Angle, elevation, perspective, crop | Achievable user-product view |
| Lighting | Direction, softness, contrast, shadow | Material-accurate response |
| Background | Palette, gradient, texture, environment | Remove incompatible brand/category cues |
| Typography | Hierarchy, alignment, weight, spacing | User language, copy, brand font when supplied |
| Graphics | Icons, rules, cards, badges, arrows | User-supported facts and editable elements |
| Product | Placement and visual role only | Entire object from product truth sources |

Completion: every visible reference element is assigned to `match`, `adapt`, `replace`, or `omit`.

## Main-image replication

1. Verify the current main-image constraints for the target marketplace/category when compliance is part of the request.
2. Isolate or reconstruct the user's real product master before matching the reference composition.
3. Match the reference camera angle, rotation, crop, relative scale, lighting softness, contact shadow, and whitespace as closely as product truth and current requirements permit.
4. Replace the reference product, quantity, packaging, accessories, and labels with the user's actual set. Do not transfer reference-only props or badges into a main image when the confirmed rules exclude them.
5. Build white or other required backgrounds deterministically and verify pixel values when relevant.

Completion: the final file reads like the reference at thumbnail scale while remaining unmistakably and accurately the user's product at full size.

## Secondary-image replication

1. Preserve the reference's information hierarchy and visual rhythm.
2. Replace every product view with an approved user-product master.
3. Rewrite headings, callouts, measurements, and benefits using supported product facts.
4. Rebuild text, icons, arrows, dimension lines, and cards deterministically.
5. Adapt scenes and human interaction to the user's product mechanics rather than copying an incompatible pose.

## A+ replication

1. Map each reference screen/module to its communication role: hero, material, construction, benefit, use, compatibility, comparison, or brand story.
2. Preserve the reference's grid, pacing, palette, hierarchy, image-to-text balance, and scene language where they suit the user's product.
3. Replace the reference product and claims module by module; do not force the user's product into a reference message it cannot support.
4. Rebuild each module at the exact confirmed upload dimensions. One source banner is not stretched across different module ratios.
5. Reuse the same approved product masters across the set so reference matching does not cause product drift.

Completion: every requested A+ module has a direct reference counterpart or a documented adaptation, and all final modules form one coherent upload-ready set.

## Replication QA

Judge two axes separately:

### Product fidelity — hard gate

- Geometry, count, parts, labels, logo, color, material, finish, use, and accessories match the user's authoritative sources.
- No competitor-specific product feature or claim has leaked into the result.

### Reference fidelity — matching gate

- Focal placement, relative scale, whitespace, camera language, palette, lighting direction, shadow, hierarchy, card/icon language, and module rhythm visibly match the selected reference.
- Compare both at thumbnail scale and full resolution. Use overlays or normalized bounding boxes when exact placement matters.

Product fidelity wins every conflict. If exact visual matching would make the product false, adapt that portion and report the deviation.
