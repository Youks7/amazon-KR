# Aspect-Ratio Adaptation

Use this branch when an existing design must fit a new pixel size.

## Start with the geometry

Compare source and target aspect ratios before editing. If they differ, four goals cannot all be guaranteed simultaneously: exact target canvas, full source content, no distortion, and no added field. State the conflict and preserve the priorities the user actually named. If priorities are unstated, preserve product proportions and critical content, then choose matching background extension or re-layout. Ask for a necessary tradeoff only when explicit hard requirements cannot all be met; continue independent files.

Never present a ratio change as a simple enlargement when the ratios differ. For example, 970 × 300 is about 3.23:1, while 1464 × 600 is 2.44:1; a faithful conversion needs re-layout, crop, or added canvas.

## Choose the fill that belongs to the design

- Flat e-commerce artwork: extend with robust colors sampled from quiet background regions. Preserve separate top and bottom bands when the source intentionally has different zones, such as a dark title bar over a light body.
- Light layouts with a continuous backdrop: use the dominant clean background for both added bands when an object or countertop contaminates one edge sample.
- Photographic scenes: use a scene-aware or softly extended background only when it blends naturally and does not create a visible frame.
- Pure-white source artwork: white padding is acceptable only when it reads as the original canvas, not as two accidental blocks.

Blurred extension is not a universal fix. It can look like a foreign border around flat Amazon graphics. Before batching, inspect a representative page for each background type actually present. Absent types are not requirements. This method check does not replace inspection of every final file.

## Preserve the content layer

- Keep the original product, typography, and layout as an undistorted foreground whenever the request is a mechanical resize.
- Use deterministic resampling for existing text and products; do not regenerate them merely to change dimensions.
- When the new ratio materially changes usable composition, rebuild the layout from fixed product assets and editable text instead of shrinking the old banner into a framed strip.
- Write to new files and preserve originals.

## Completion criteria

Every output has the exact requested dimensions and format, the product preserves physical proportions and valid perspective, critical content remains complete and accurate, and added fields match the source design. Inspect every final file for cropping, text, product distortion, and background seams, then run technical checks against its target. For mechanical resizing, retain the original foreground pixels except deterministic resampling; for authorized re-layout, accurately rebuild editable text/graphics without regenerating the product. Apply the shared QA and status rules in [visual-qa.md](visual-qa.md).
