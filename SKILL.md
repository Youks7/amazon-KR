---
name: amazon-kr
description: Produce final Amazon main images, secondary listing images, and A+ image modules for physical products in any category, including faithful reconstruction from reference designs; also revise, resize, or audit existing assets. Use for white-background product images, infographics, lifestyle scenes, installation or use graphics, material and finish fidelity, comparison modules, and export QA. Do not use for PPC, catalog operations, inventory, or account management.
---

# Amazon KR

Treat a product truth brief as the constraint system and the image model as a scene generator. A polished image is rejected when the product geometry, scale, material, interaction, included parts, color, branding, or claim is wrong.

## Execution Contract

Direct production is the default. When the user asks to create, make, generate, design, or produce images, use the available image-generation/editing and local composition tools to deliver actual final image files. A plan, storyboard, copy deck, prompt set, or audit without rendered assets is incomplete unless the user explicitly requested only that intermediate deliverable.

Route the request through [references/production-modes.md](references/production-modes.md). If a product-defining ambiguity would create visibly different goods, ask one concise blocking question; otherwise state a reasonable assumption and continue production. If required product images are absent, request those images rather than inventing the product. If no image-capable tool is available, state that limitation plainly and provide the most useful production-ready fallback without claiming images were created.

## Workflow

1. Inventory every supplied source, draft, client brief, package list, logo, uploader screenshot, and target specification. Rank sources by authority and distinguish approved finals from experiments. Completion: every output has a named purpose, marketplace/module when relevant, exact pixel target, and authoritative product source.
2. Create the product truth brief using [references/product-intake.md](references/product-intake.md). Separate confirmed facts from visual inferences. Proactively remind the user about any missing material or finish requirements before generation. Completion: every visually consequential unknown is confirmed, explicitly assumed, or reported as blocking.
3. Route only to relevant detail:
   - When the user asks to replicate, recreate, reproduce, imitate, match, or reference an existing main image, listing image, or A+ design, read [references/reference-replication.md](references/reference-replication.md).
   - For metal, wood, glass, plastic, ceramic, rubber, leather, textile, coated, transparent, or mixed-material products, read [references/material-fidelity.md](references/material-fidelity.md).
   - For aspect-ratio conversion, read [references/resizing.md](references/resizing.md).
   - For a suction-hook task matching the historical case, optionally read [references/suction-hook-profile.md](references/suction-hook-profile.md) as an example; current product evidence always wins.
4. Select the production mode and page set. Plan only the images that sell or explain this product: compliant main image, alternate views, feature or construction detail, dimensions, use or installation, lifestyle context, compatibility or care, package contents, variant/finish comparison, product comparison, or A+ hero/module. This is a menu, not a fixed page count.
5. Build fixed product assets first. Use authoritative product images for geometry, branding, parts, color, and material; make one approved product master per angle, variant, finish, or use state. Reuse these masters instead of asking an image model to redraw the product in every scene.
6. Separate generative and deterministic work:
   - Use image generation or editing for backgrounds, atmosphere, contextual props, and narrowly scoped product-use composites.
   - Use code-native composition for crops, cards, type, icons, arrows, numbering, spacing, and final export.
   - Preserve aspect ratio. Reach the target canvas by intentional crop, contain, re-layout, or source-matched extension; never stretch the product.
7. Audit full-size exports against [references/visual-qa.md](references/visual-qa.md). Run `scripts/validate_images.py` for deterministic format and dimension checks when files are local.
8. Deliver the actual approved image files plus a concise audit report naming the product truth sources, material specification, target size, rejected defects, corrections, and result for each file. Completion: every requested image exists, has been visually inspected at full size, passes programmatic checks, and contains no unsupported factual claim.

## Decision Rules

- Product fidelity outranks scene richness. Prefer a simpler composition with a correct product.
- In reference replication, match the reference's visual system while the user's authoritative sources control the product. Reference products, branding, copy, accessories, and claims never override the product truth brief.
- Production outranks narration. Keep intermediate explanation brief and spend the work on finished assets and verification.
- Material fidelity is product fidelity. A shape-correct item with the wrong brushed direction, gloss, transparency, coating, grain, weave, or reflectivity is a failed product image.
- Every depicted interaction must be mechanically intelligible: contact, grip, support, insertion, attachment, pouring, opening, folding, load path, and gravity must match the real product.
- Preserve the same geometry, scale, branding, parts, colorway, and finish through sequential instructions and across the image set.
- Treat apparent transparency cautiously. A checkerboard baked into pixels is an opaque image, not an alpha channel.
- Preserve original masters and approved fixed assets. Create new versions for experiments and clearly exclude rejected drafts from delivery.
- Derive claims only from supplied evidence. Ask for substantiation before adding load capacity, waterproofing, permanence, compatibility, or performance claims.
- Treat observed dimensions as project requirements, not universal Amazon policy. When the user asks whether an asset complies with current Amazon rules, verify against current official Amazon/Seller Central documentation.
- When a generic label such as “Basic A+” conflicts with the dimensions shown by the actual upload slot, stop treating the label as a complete specification. Name the conflict and use the confirmed module/upload target; different aspect ratios require separate layouts, not a nominal resize.
