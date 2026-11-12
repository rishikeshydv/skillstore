# Branded document authoring and QA

## LG Ad Solutions brand source
The canonical palette and logo usage constraints are in `assets/brand.yaml`; use that file, not recolored approximations.

- White/light document pages: black LG Ad Solutions logo from `assets/logo_black.png` (SVG variant also included).
- Active Red `#FD312E`: titles/heading accents, sparingly; Heritage Red `#A50034`: filled table headings, horizontal rules/footer accents.
- Body text neutral dark; secondary purple/magenta family only for supporting graphics and charts.
- Font: Roboto when available, Arial fallback. Proprietary LG EI font files are **not** bundled or redistributed.
- No logo distortion, recoloring, shadow, outline, crowded placement. Respect minimum 3 mm logo printed height and clear space.
- Use restrained white backgrounds and deliberate spacing; make tables and diagrams readable.

## JSON content format for renderer

Write a UTF-8 JSON file with this shape and call `scripts/render_proposal.py`:

```json
{
  "document_type": "one-pager",
  "title": "[Feature Name]",
  "subtitle": "[Optional short description]",
  "status": "Draft",
  "metadata": {"Author": "[Name]", "Last Updated": "[Date]"},
  "sections": [
    {"title": "Problem & Motivation", "level": 1, "blocks": [
      {"type": "paragraph", "text": "[Problem and motivation]"}
    ]}
  ]
}
```

Set `document_type` explicitly to `one-pager`, `hld` or `lld`. HLD and LLD may have nested `level: 2` subsections. For All Three, prepare **three JSON inputs and three DOCX outputs**.

Valid block types:
- `paragraph`: `{"type":"paragraph","text":"..."}`
- `bullets` / `numbered`: `{"type":"bullets","items":["..."]}`
- `table`: `{"type":"table","headers":["Name","Contract"],"rows":[["X","Y"]]}`
- `callout`: `{"type":"callout","label":"Assumption","text":"..."}`
- `image`: `{"type":"image","path":"./diagram.png","caption":"Architecture","width_inches":6.3}`
- `code`: `{"type":"code","text":"..."}`
- `page_break`: use only in long HLD/LLD when necessary.

Use `metadata` only for supplied fields; do not invent dates/owners. Omit `decision_requested` for One-Pager and HLD unless user specifically requests a decision block (but still no HLD Approval heading). The One-Pager renderer deliberately suppresses a cover page and decision callout.

## Render command

```
python scripts/render_proposal.py --input /path/to/content.json --output /path/to/output.docx
```

Bundled renderer accepts all three document profiles; defaults to `hld` if missing (but always provide it). It uses the provided brand YAML and logos and can include diagram images. A generic technical figure is **not** a replacement for a user-specific architecture diagram.

## Visual verification (mandatory)

Render to page PNGs using the environment's DOCX skill renderer, e.g.:

```
python /home/oai/skills/docx/render_docx.py /path/to/output.docx --output_dir /path/to/rendered
```

Inspect each page image and check spacing, fonts, tables, diagram legibility, logo proportions, margins, and page boundaries. Iterate until clean. For One-Pager, confirm **page count = 1**; tighten content first before layout tweaks. If infrastructure lacks DOCX/PDF rendering, say verification is incomplete rather than claiming success.

For long HLD/LLD, balance readability and depth; no artificial page cap. For one-pager, prefer concise text and a single compact illustration over tiny fonts or squeezed tables.

## Multiple documents
Use consistent terminology, requirement IDs and cross references across the selected documents. Each stands alone: it needs its own short title, status and pertinent references. Do not automatically prepend a One-Pager when HLD or LLD alone is requested.
