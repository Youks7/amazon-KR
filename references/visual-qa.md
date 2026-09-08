# Visual QA

Review each final image at full resolution. Apply requirements relevant to the request and changed content; audit-only work reports findings without repair. Classify each applicable check as pass, fail, or unverified, and exclude irrelevant checks as not applicable. A page is QA-passed only when applicable hard requirements pass and warnings have been resolved by inspection. An unverified requirement is not a pass; user approval is a separate record under [SKILL.md](../SKILL.md#execution-contract).

## Product fidelity

For an explicitly requested concept, compare against the recorded authorized transformation (such as a proposed color), while preserving unchanged product facts. Label the delivery as a concept; passing concept QA does not verify an existing sale variant or readiness for a real-product listing.

- The silhouette matches an authoritative source.
- Proportions, component, fastener, control, opening, accessory, and package-content counts are unchanged.
- Physical geometry and projection match the source view: a front-facing circular surface stays circular, while an oblique one may appear elliptical. Reject non-uniform stretching, not legitimate perspective.
- Logos, labels, controls, ports, seams, patterns, and variant-specific details are accurate and correctly placed.
- Product color and finish are consistent with the confirmed variant and with adjacent pages.
- Repeated product instances use a QA-passed fixed asset or demonstrably preserve the same physical product across legitimate changes of view and use state.

## Material fidelity

- Generated or changed material regions match supported visible properties in the product truth brief. Preserved regions retain their original appearance; hidden processes need evidence only when represented or claimed.
- Gloss, roughness, reflection behavior, transparency, texture direction, and texture scale remain plausible and consistent.
- Brushed metal has coherent directional grain and anisotropic highlights rather than chrome reflections or random scratches.
- Transparent materials retain believable thickness, edge definition, and refraction.
- Wood grain, textile weave, leather grain, coating texture, and molded plastic details follow the actual construction.
- Lighting reveals the material without recoloring it or erasing product form.

## Physical logic

- Every product interaction has visible, mechanically plausible contact, support, grip, insertion, connection, or motion.
- Hinges, lids, doors, buttons, cables, handles, blades, wheels, fabric, liquids, and accessories behave as the real construction permits.
- Supported, hanging, worn, held, poured, stacked, or mounted objects follow gravity and load paths naturally.
- No floating, penetration, fusion, duplicate fragments, impossible deformation, or unexplained attachment occurs.
- Sequential installation states preserve the same product and communicate one unambiguous action per step.

## Composition and text

- The hierarchy remains legible at the delivered size.
- Titles, labels, products, and contact points remain inside safe bounds.
- Text is spelled correctly, not AI-garbled, and contrast is adequate.
- Cropping does not remove a functional part or create a misleading shape.
- Added side or top/bottom fields are visually quiet and do not stretch or clone edge objects.

## Technical export

- Pixel dimensions exactly match the request.
- File format and color mode match the delivery requirement.
- JPEG exports contain no accidental alpha expectation; PNG transparency is real alpha, not a baked checkerboard.
- File names are ordered and descriptive.
- Masters, fixed assets, rejected drafts, and finals are separable.

## Claims

- Every performance or compatibility statement is supported by supplied product evidence.
- The page contains no invented capacity, durability, waterproof, permanence, or universal-surface claim.
- If current Amazon compliance is asserted or required for delivery, record the relevant official source, marketplace/category/module context, and check date. If inaccessible, record compliance as unverified; do not infer it from image dimensions or a script pass.

## Programmatic check scope

For local JPEG/PNG exports, use `scripts/validate_images.py` with explicit width, height, format, and any required mode/alpha constraint. Run homogeneous groups separately or use `--manifest` for mixed dimensions (see [README](../README.md#图片技术校验)). The script reports unreadable/unsupported files and mismatches for supplied targets. Missing targets are explicitly `NOT_CHECKED`; they are not inferred from the image being tested.

Checkerboard detection is heuristic and produces warnings, including on images with an alpha channel. Inspect any warning: a legitimate pattern can pass visual review, a baked fake background must be corrected, and uncertain cases remain unverified. A warning or alpha channel alone establishes neither truth nor falsity of transparency.

The script does not certify product geometry, text accuracy, physical interaction, ICC profile suitability, pure-white background regions, or current Amazon compliance. Inspect or use a suitable additional check when those requirements apply. If no suitable tool can check a required property, record it as unverified.

## Audit report template

Record each file's target and actual dimensions/format/mode, source evidence, applicable visual results, technical checks run, missing checks, warning dispositions, corrections, and output status. Record explicit user approval separately when requested. Name rejected drafts when necessary to prevent reuse. Repair and retry behavior follows [SKILL.md](../SKILL.md#correction-and-completion); an audit-only report can be complete while images fail.
