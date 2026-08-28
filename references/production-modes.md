# Production Modes

Choose the branch implied by the request. Unless the user asks only for planning, prompts, or review, every branch ends in rendered image files.

When any branch is driven by a reference image or reference A+ set, also follow [reference-replication.md](reference-replication.md).

## Amazon main image

Produce the primary listing image from authoritative product sources.

- Preserve exact product geometry, included quantity, packaging, colorway, labels, and material.
- Isolate and retouch the real product when possible; use generation only for narrowly controlled reconstruction or cleanup.
- Use the target marketplace/category's current official main-image requirements. When compliance matters and current requirements were not supplied, verify official Amazon/Seller Central documentation.
- Build the requested canvas and color profile deterministically. When a pure-white background is required, verify actual RGB 255/255/255 rather than relying on visual appearance.
- Keep product scale, crop, shadow, props, text, badges, borders, and accessories within the confirmed category rules.

Completion: the final main-image file is rendered, visually compared with the authoritative product source, and checked for exact dimensions, format, background, and prohibited additions.

## Secondary listing images

Produce a coherent sequence that answers the buyer's highest-value questions. Possible pages include benefit hero, feature detail, dimensions, material close-up, use, installation, compatibility, package contents, comparison, and lifestyle context.

- Put one primary message on each image.
- Reuse approved product masters across the sequence.
- Use editable/deterministic typography whenever possible; do not depend on generated text.
- Keep copy readable at listing-thumbnail and mobile viewing size.
- Use supported claims only.

When the user requests “a complete listing image set” without a count, a reasonable baseline is one main image plus five secondary images. State that assumption and proceed when the supplied material supports it; reduce or expand the set when the product needs fewer or more buyer questions answered.

Completion: all final files are rendered in sequence, named clearly, previewed, and checked as a set for consistency and duplicated messaging.

## A+ images

Produce the image assets for the confirmed Basic or Premium A+ modules.

- Use the actual uploader screenshot or exact module dimensions when supplied.
- Design each module for its role rather than stretching one banner across incompatible ratios.
- Maintain a coherent visual system across hero, construction/material, benefits, use/installation, compatibility/care, comparison, and brand story modules.
- Keep important product details and text safe for responsive/mobile crops when the module behavior is known.
- Render final files at each exact upload size and preserve editable/high-resolution masters when practical.

When the user requests “a set of A+ images” without a module plan, choose a compact evidence-backed sequence, state the assumed module count and dimensions, and produce it. If current upload dimensions cannot be inferred safely, ask for the uploader/module screenshot before final export while continuing product-master and copy preparation.

Completion: every requested A+ module exists at its exact size, the set has been visually reviewed in order, and an upload-ready folder contains only approved finals.

## Full launch set

If the user requests both listing and A+ assets, create one shared product truth brief and shared product-master library, then produce separate main-image, secondary-image, and A+ outputs. Do not repurpose incompatible aspect ratios by stretching.

## Reference-driven replication

Replication may apply to a single main image, a secondary-image sequence, an A+ set, or the full launch set. Treat it as an execution method layered onto the relevant production mode, not as a request for analysis only. The reference supplies the visual blueprint; the user's sources supply the product. Deliver rebuilt final files and a short replication note listing any deliberate deviations required for product truth, supported claims, or current upload requirements.

## Revision, resize, and audit

- Revision ends with corrected image files, not only a defect list.
- Resize ends with new files at the target dimensions and preserved originals.
- Audit is read-only when the user asks only for review; return findings and do not mutate assets.

## Delivery structure

Use clear folders when the workspace permits:

```text
output/
├── listing-main/
├── listing-secondary/
├── a-plus/
├── masters/
└── audit-report.md
```

Do not create empty folders for modes the user did not request. Keep rejected drafts outside the upload-ready final folders.
