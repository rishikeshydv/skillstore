#!/usr/bin/env python3
import argparse, json, os, tempfile
from pathlib import Path

import yaml
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / 'assets'


def rgb(hexstr):
    h = hexstr.strip().lstrip('#')
    return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_margins(cell, top=120, start=140, bottom=120, end=140):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar')
        tcPr.append(tcMar)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tcMar.find(qn(f'w:{m}'))
        if node is None:
            node = OxmlElement(f'w:{m}')
            tcMar.append(node)
        node.set(qn('w:w'), str(v))
        node.set(qn('w:type'), 'dxa')


def set_cell_border(cell, **edges):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = tcPr.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcPr.append(borders)
    for edge_name, edge_data in edges.items():
        tag = 'w:' + edge_name
        edge = borders.find(qn(tag))
        if edge is None:
            edge = OxmlElement(tag)
            borders.append(edge)
        for key, val in edge_data.items():
            edge.set(qn('w:' + key), str(val))


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = ' PAGE '
    fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2)


def ensure_png(path: Path):
    if path.suffix.lower() != '.svg':
        return path
    import cairosvg
    out = Path(tempfile.mkstemp(suffix='.png')[1])
    cairosvg.svg2png(url=str(path), write_to=str(out), output_width=1500)
    return out


def apply_font(run, name, size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if size is not None: run.font.size = Pt(size)
    if bold is not None: run.bold = bold
    if italic is not None: run.italic = italic
    if color is not None: run.font.color.rgb = color


def configure_styles(doc, brand, compact=False):
    heading_font = brand['fonts'].get('heading') or brand['fonts'].get('fallback', 'Arial')
    body_font = brand['fonts'].get('body') or brand['fonts'].get('fallback', 'Arial')
    active = rgb(brand['colors']['active_red'])
    body = rgb(brand['colors'].get('body_text', '1B2430'))
    grey = rgb(brand['colors'].get('body_grey', '5A6673'))

    normal = doc.styles['Normal']
    normal.font.name = body_font
    normal._element.rPr.rFonts.set(qn('w:eastAsia'), body_font)
    normal.font.size = Pt(9.5 if compact else 10.5)
    normal.font.color.rgb = body
    normal.paragraph_format.space_after = Pt(3 if compact else 6)
    normal.paragraph_format.line_spacing = 1.04 if compact else 1.12

    heading_specs = [('Title', 18, 0, 5), ('Heading 1', 11.3, 6, 3), ('Heading 2', 10.3, 5, 2), ('Heading 3', 10, 4, 2)] if compact else [('Title', 28, 0, 12), ('Heading 1', 18, 18, 7), ('Heading 2', 13.5, 14, 5), ('Heading 3', 11.5, 10, 4)]
    for name, size, before, after in heading_specs:
        s = doc.styles[name]
        s.font.name = heading_font
        s._element.rPr.rFonts.set(qn('w:eastAsia'), heading_font)
        s.font.size = Pt(size)
        s.font.bold = True
        s.font.color.rgb = active if name != 'Title' else body
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True
        pPr = s.element.get_or_add_pPr()
        old_bdr = pPr.find(qn('w:pBdr'))
        if old_bdr is not None:
            pPr.remove(old_bdr)

    if 'Proposal Subtitle' not in [s.name for s in doc.styles]:
        s = doc.styles.add_style('Proposal Subtitle', WD_STYLE_TYPE.PARAGRAPH)
        s.font.name = body_font
        s._element.rPr.rFonts.set(qn('w:eastAsia'), body_font)
        s.font.size = Pt(13)
        s.font.color.rgb = grey
        s.paragraph_format.space_after = Pt(18)

    if 'Code Block' not in [s.name for s in doc.styles]:
        s = doc.styles.add_style('Code Block', WD_STYLE_TYPE.PARAGRAPH)
        s.font.name = 'Courier New'
        s._element.rPr.rFonts.set(qn('w:eastAsia'), 'Courier New')
        s.font.size = Pt(8.5)
        s.font.color.rgb = body
        s.paragraph_format.left_indent = Inches(0.15)
        s.paragraph_format.right_indent = Inches(0.15)
        s.paragraph_format.space_before = Pt(4)
        s.paragraph_format.space_after = Pt(8)


def add_brand_header(section, brand):
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_path = ASSETS_DIR / brand['logo']['black']['png']
    if logo_path.exists():
        p.add_run().add_picture(str(logo_path), width=Inches(1.55))


def add_footer(section, brand):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run('LG Ad Solutions   |   ')
    apply_font(run, brand['fonts'].get('body', 'Arial'), size=8, color=rgb(brand['colors']['body_grey']))
    add_page_number(p)
    set_cell = None
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:top')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '10'); bottom.set(qn('w:space'), '6'); bottom.set(qn('w:color'), brand['colors']['heritage_red'])
    pBdr.append(bottom); pPr.append(pBdr)


def add_metadata_table(doc, metadata, brand):
    if not metadata: return
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    table.columns[0].width = Inches(1.65)
    table.columns[1].width = Inches(4.9)
    for k, v in metadata.items():
        cells = table.add_row().cells
        cells[0].width = Inches(1.65); cells[1].width = Inches(4.9)
        for c in cells:
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(c, 90, 120, 90, 120)
            set_cell_border(c, bottom={'val':'single','sz':'4','color':'D9DDE2'})
        r = cells[0].paragraphs[0].add_run(str(k))
        apply_font(r, brand['fonts'].get('body','Arial'), size=9, bold=True, color=rgb(brand['colors']['body_grey']))
        r = cells[1].paragraphs[0].add_run(str(v))
        apply_font(r, brand['fonts'].get('body','Arial'), size=9.5, color=rgb(brand['colors']['body_text']))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_callout(doc, label, text, brand):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = table.cell(0,0)
    set_cell_shading(cell, 'F7F7F7')
    set_cell_margins(cell, 160, 180, 160, 180)
    set_cell_border(cell, start={'val':'single','sz':'18','color':brand['colors']['active_red']})
    p = cell.paragraphs[0]
    if label:
        r = p.add_run(label + ': ')
        apply_font(r, brand['fonts'].get('heading','Arial'), size=10.5, bold=True, color=rgb(brand['colors']['active_red']))
    r = p.add_run(text)
    apply_font(r, brand['fonts'].get('body','Arial'), size=10.2, color=rgb(brand['colors']['body_text']))
    after = doc.add_paragraph(); after.paragraph_format.space_after = Pt(3)


def add_table(doc, headers, rows, brand):
    cols = max(len(headers), max([len(r) for r in rows], default=0))
    if cols == 0: return
    table = doc.add_table(rows=1, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    hdr = table.rows[0].cells
    for i in range(cols):
        txt = headers[i] if i < len(headers) else ''
        set_cell_shading(hdr[i], brand['colors']['heritage_red'])
        set_cell_margins(hdr[i], 110, 120, 110, 120)
        hdr[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = hdr[i].paragraphs[0]
        r = p.add_run(str(txt))
        apply_font(r, brand['fonts'].get('body','Arial'), size=8.8, bold=True, color=RGBColor(255,255,255))
    for row in rows:
        cells = table.add_row().cells
        for i in range(cols):
            set_cell_margins(cells[i], 110, 120, 110, 120)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_border(cells[i], bottom={'val':'single','sz':'3','color':'D9DDE2'})
            p = cells[i].paragraphs[0]
            r = p.add_run(str(row[i]) if i < len(row) else '')
            apply_font(r, brand['fonts'].get('body','Arial'), size=8.8, color=rgb(brand['colors']['body_text']))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_block(doc, block, brand, base_dir):
    typ = block.get('type','paragraph')
    if typ == 'paragraph':
        p = doc.add_paragraph()
        p.add_run(block.get('text',''))
    elif typ in ('bullets','numbered'):
        style = 'List Bullet' if typ == 'bullets' else 'List Number'
        items = block.get('items',[])
        for idx, item in enumerate(items):
            p = doc.add_paragraph(style=style)
            p.paragraph_format.keep_together = True
            if idx < len(items)-1:
                p.paragraph_format.keep_with_next = True
            p.add_run(str(item))
    elif typ == 'table':
        add_table(doc, block.get('headers',[]), block.get('rows',[]), brand)
    elif typ == 'callout':
        add_callout(doc, block.get('label',''), block.get('text',''), brand)
    elif typ == 'image':
        raw = block.get('path')
        if not raw: return
        path = Path(raw)
        if not path.is_absolute(): path = (base_dir / path).resolve()
        if not path.exists():
            add_callout(doc, 'Diagram unavailable', f'Image not found: {raw}', brand)
            return
        img = ensure_png(path)
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(img), width=Inches(float(block.get('width_inches', 6.7))))
        if block.get('caption'):
            cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cap.add_run(block['caption'])
            apply_font(r, brand['fonts'].get('body','Arial'), size=8.5, italic=True, color=rgb(brand['colors']['body_grey']))
    elif typ == 'code':
        p = doc.add_paragraph(style='Code Block')
        p.add_run(block.get('text',''))
        pPr = p._p.get_or_add_pPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:fill'),'F2F3F5'); pPr.append(shd)
    elif typ == 'page_break':
        doc.add_page_break()


def build(input_path, output_path):
    with open(ASSETS_DIR / 'brand.yaml', 'r', encoding='utf-8') as f:
        brand = yaml.safe_load(f)
    with open(input_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    kind = spec.get('document_type', 'hld').lower().strip()
    if kind not in {'one-pager', 'hld', 'lld'}:
        raise ValueError('document_type must be one-pager, hld, or lld')
    compact = kind == 'one-pager'
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.64 if compact else 0.72); sec.bottom_margin = Inches(0.62 if compact else 0.7)
    sec.left_margin = Inches(0.72 if compact else 0.82); sec.right_margin = Inches(0.72 if compact else 0.82)
    configure_styles(doc, brand, compact=compact)
    add_brand_header(sec, brand)
    add_footer(sec, brand)

    # Compact One-Pager is exactly one page when the supplied content fits;
    # HLD/LLD retain the original branded cover treatment.
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0 if compact else 34)
    p.paragraph_format.space_after = Pt(3 if compact else 6)
    status = str(spec.get('status','Draft')).upper()
    r = p.add_run(status)
    apply_font(r, brand['fonts'].get('heading','Arial'), size=8.5 if compact else 9.5,
               bold=True, color=rgb(brand['colors']['active_red']))

    title = doc.add_paragraph(style='Title'); title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    title.add_run(spec.get('title','Architecture Proposal'))
    if spec.get('subtitle'):
        sub = doc.add_paragraph(style='Proposal Subtitle'); sub.add_run(spec['subtitle'])
        if compact:
            sub.paragraph_format.space_after = Pt(4)
            for run in sub.runs: apply_font(run, brand['fonts'].get('body','Arial'), size=9)

    if compact:
        meta = spec.get('metadata',{})
        if meta:
            mp = doc.add_paragraph()
            mp.paragraph_format.space_after = Pt(6)
            mr = mp.add_run('   |   '.join(f'{k}: {v}' for k,v in meta.items()))
            apply_font(mr, brand['fonts'].get('body','Arial'), size=8.5,
                       color=rgb(brand['colors']['body_grey']))
    else:
        add_metadata_table(doc, spec.get('metadata',{}), brand)
        if spec.get('decision_requested'):
            add_callout(doc, 'Decision requested', spec['decision_requested'], brand)
        doc.add_page_break()

    base_dir = Path(input_path).resolve().parent
    for secspec in spec.get('sections', []):
        title_text = secspec.get('title','')
        level = int(secspec.get('level',1))
        style = 'Heading 1' if level <= 1 else ('Heading 2' if level == 2 else 'Heading 3')
        if title_text:
            doc.add_paragraph(title_text, style=style)
        for block in secspec.get('blocks',[]):
            add_block(doc, block, brand, base_dir)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print(out)


def main():
    ap = argparse.ArgumentParser(description='Render a branded LG Ad Solutions architecture proposal DOCX from JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    build(args.input, args.output)

if __name__ == '__main__':
    main()
