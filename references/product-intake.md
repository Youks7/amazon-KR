# Product Truth Intake

Build this brief for every product category before generation or substantial editing. Do not silently convert uncertain visual guesses into product facts.

## Required truth fields

- Product identity and category.
- Authoritative source images and which source controls each angle or detail.
- Exact silhouette, proportions, component count, included accessories, openings, controls, connectors, seams, fasteners, labels, and logo placement.
- Variant structure: size, color, material, finish, packaging, and included-parts differences.
- Real use and interaction: how it is held, attached, opened, installed, worn, poured, folded, connected, supported, cleaned, or stored.
- Material and surface specification. If visually relevant, read [material-fidelity.md](material-fidelity.md).
- Supported benefits and claims, plus claims that require evidence.
- Target marketplace, language, module or image role, exact dimensions, file format, and required copy.
- Must-preserve and must-avoid details supplied by the user.

## Material reminder gate

Before producing a material-sensitive product, tell the user what is confirmed and what remains unspecified. At minimum consider:

- Base material: stainless steel, aluminum, brass, ABS, acrylic, glass, ceramic, silicone, wood, leather, textile, or another material.
- Surface process: brushed, polished, mirror-plated, bead-blasted, anodized, powder-coated, painted, glazed, frosted, embossed, woven, or unfinished.
- Gloss level: mirror, glossy, satin, matte, or ultra-matte.
- Direction and scale of grain, brushing, weave, or texture.
- Color reference and whether multiple variants must match.
- Acceptable fingerprints, patina, wear, pores, seams, machining marks, or molding lines.
- A close-up reference that represents the desired finish.

Use a concise reminder such as:

> 开始生成前，请确认产品材质与表面工艺：基础材质、拉丝/镜面/哑光等处理、光泽度、纹理方向、准确颜色，以及哪张近景图作为质感基准。若未指定，我只能把当前图片中的表现视为暂定参考。

Ask only for gaps that would materially change the result. When a safe reversible choice exists, state the assumption and continue; when different answers would produce visibly different products, obtain confirmation before generating the product master.

## Source precedence

Use explicit current user instructions first, then current authoritative product photographs or drawings, then packaging/manual evidence, then approved masters. Style references control presentation only unless the user explicitly says they also represent the actual product. Competitor images never establish this product's geometry, included parts, branding, or claims.

## Completion format

Summarize the brief in a compact table with `Confirmed`, `Inferred`, and `Missing/Blocking` states. The brief is complete when every product-defining decision needed by the requested images has a state and a source.

