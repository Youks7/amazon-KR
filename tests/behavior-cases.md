# Behavior acceptance cases

These are scenario checks, not tests of exact wording. Use them after changing the execution contract or branches. Record the skill revision and whether the run is a text walkthrough or actual execution. A walkthrough without images/tools is not an end-to-end production test.

For actual runs, provide the stated source assets in an isolated workspace and use only authorized tools/actions. Record first action, produced artifacts, waiting scope, verification performed, and completion status. A text walkthrough may assess routing and decisions only; it must not invent files, checks, or tool results.

| Request and inputs | Observable acceptance criteria |
|---|---|
| Supplied front product photo; replace only the background with white | Local edit; preserve product pixels and perspective; no questionnaire about unseen manufacturing process; new output, edge/background and export checks |
| Five existing images and an explicit replacement title for image 2 | Change image 2 title only; inspect affected layout; no new product master or repeated material approval |
| Supplied product photos and copy; A+ uploader screenshot will follow | Prepare supported masters/copy; pause ratio-dependent layout only if ratio is unknown, and final export until target is resolved; do not claim whole task complete |
| User explicitly requests master approval before other pages | Show internally checked master, then wait before dependent page production; internal QA or silence does not count as approval |
| Audit five existing images without authoritative product photos | Read-only report covering every image and evidence limits; inspectable defects reported; missing product evidence marked unverified without blocking the whole report |
| Replicate oblique circular product with same-angle authoritative photo | Preserve valid elliptical projection; no forced circle or unnecessary confirmation; compare product and reference fidelity |
| Three required secondary images, one requires an undocumented back view | Ask only for needed back-view evidence; continue two independent outputs; never invent back geometry, silently drop a required output, or claim full completion |
| Production requested but no permitted image-capable method exists | Report capability blocker and useful possible fallback; mark affected production blocked; no invented generation, purchase, or service access |
| Explicit black concept colorway, not a sale variant | Apply requested color as recorded concept QA target, preserve other facts; label concept; do not repeatedly ask whether a sale variant exists |
| Optional waterproof claim lacks evidence | Omit and report that unsupported optional claim, continue other content; do not turn the request to add copy into proof |
| A+ files have different dimensions | Use per-file targets or homogeneous groups; report actual check coverage, not one universal dimension |
| Existing title defect during an authorized production run | Repair title/layout without asking whether to continue or rebuilding a sound product master |
| Unavailable required verification tool | Use an equivalent permitted check if feasible; otherwise report unverified, not passed |
| Only light-background images in a resize batch | Sample existing background types for the method; inspect every final file, without demanding an absent dark page |

Reference commands for script behavior are maintained in [test_validate_images.py](test_validate_images.py). Visual truth, layout quality, real generated text accuracy, and platform acceptance still require actual evidence and inspection.
