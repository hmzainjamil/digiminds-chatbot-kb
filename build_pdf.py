#!/usr/bin/env python3
"""
DigiMinds Chatbot Knowledge Base — Professional PDF Builder
Generates a selectable-text, professionally formatted PDF from all KB files.
"""
import json
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Image, ListFlowable, ListItem, HRFlowable, PageTemplate,
    Frame, NextPageTemplate, BaseDocTemplate
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------- Brand palette ----------------
BRAND_PRIMARY   = HexColor("#0B1F3A")   # Deep navy
BRAND_ACCENT    = HexColor("#E85D2C")   # DigiMinds orange
BRAND_MUTED     = HexColor("#5A6F8C")   # Slate blue-grey
BRAND_LIGHT_BG  = HexColor("#F4F6FA")   # Off-white panel
BRAND_RULE      = HexColor("#D8DEE9")   # Soft line
BRAND_CODE_BG   = HexColor("#F7F4EC")   # Warm cream for code blocks
BRAND_SUCCESS   = HexColor("#1E7F4F")
BRAND_WARNING   = HexColor("#C6821C")

KB_DIR = "/Users/mc/digiminds-chatbot-kb"
OUT_PDF = os.path.join(KB_DIR, "DigiMinds_Chatbot_Knowledge_Base.pdf")

# ---------------- Page dimensions ----------------
PAGE_W, PAGE_H = A4
MARGIN_L = 18 * mm
MARGIN_R = 18 * mm
MARGIN_T = 22 * mm
MARGIN_B = 22 * mm

# ---------------- Styles ----------------
styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    'TitleStyle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=34, leading=40,
    textColor=BRAND_PRIMARY, alignment=TA_LEFT, spaceAfter=10
)
SUBTITLE_STYLE = ParagraphStyle(
    'SubtitleStyle', parent=styles['Normal'],
    fontName='Helvetica', fontSize=14, leading=20,
    textColor=BRAND_MUTED, alignment=TA_LEFT, spaceAfter=20
)
H1_STYLE = ParagraphStyle(
    'H1', fontName='Helvetica-Bold', fontSize=22, leading=28,
    textColor=BRAND_PRIMARY, spaceBefore=18, spaceAfter=10
)
H2_STYLE = ParagraphStyle(
    'H2', fontName='Helvetica-Bold', fontSize=16, leading=22,
    textColor=BRAND_PRIMARY, spaceBefore=14, spaceAfter=6
)
H3_STYLE = ParagraphStyle(
    'H3', fontName='Helvetica-Bold', fontSize=12, leading=16,
    textColor=BRAND_ACCENT, spaceBefore=10, spaceAfter=4
)
BODY_STYLE = ParagraphStyle(
    'Body', fontName='Helvetica', fontSize=10, leading=15,
    textColor=black, alignment=TA_LEFT, spaceAfter=6
)
BODY_JUSTIFY = ParagraphStyle(
    'BodyJ', parent=BODY_STYLE, alignment=TA_JUSTIFY
)
BULLET_STYLE = ParagraphStyle(
    'Bullet', parent=BODY_STYLE, leftIndent=14, bulletIndent=4,
    spaceAfter=3
)
CODE_STYLE = ParagraphStyle(
    'Code', fontName='Courier', fontSize=8.5, leading=11,
    textColor=HexColor("#2B2B2B"), backColor=BRAND_CODE_BG,
    leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8,
    borderPadding=6
)
CAPTION_STYLE = ParagraphStyle(
    'Caption', fontName='Helvetica-Oblique', fontSize=9, leading=12,
    textColor=BRAND_MUTED, spaceAfter=6
)
TOC_ENTRY = ParagraphStyle(
    'TOC', fontName='Helvetica', fontSize=11, leading=18,
    textColor=BRAND_PRIMARY, leftIndent=0, spaceAfter=2
)
TOC_NUM = ParagraphStyle(
    'TOCNum', fontName='Helvetica-Bold', fontSize=11, leading=18,
    textColor=BRAND_ACCENT
)

def safe(text):
    """Escape for reportlab paragraphs."""
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s

def md_inline(text):
    """Convert basic markdown inline formatting to reportlab tags."""
    if text is None:
        return ""
    text = safe(text)
    # bold **x** -> <b>x</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # italic *x* -> <i>x</i>
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', text)
    # inline code `x` -> <font face="Courier">x</font>
    text = re.sub(r'`([^`]+?)`', r'<font face="Courier" size="9" color="#5A4A2A">\1</font>', text)
    return text

# ---------------- Page decorators ----------------
def cover_page(canv, doc):
    canv.saveState()
    # Full-bleed dark band on top
    canv.setFillColor(BRAND_PRIMARY)
    canv.rect(0, PAGE_H - 90*mm, PAGE_W, 90*mm, fill=1, stroke=0)
    # Accent strip
    canv.setFillColor(BRAND_ACCENT)
    canv.rect(0, PAGE_H - 93*mm, PAGE_W, 3*mm, fill=1, stroke=0)
    # Logo mark (typographic)
    canv.setFillColor(white)
    canv.setFont("Helvetica-Bold", 13)
    canv.drawString(MARGIN_L, PAGE_H - 20*mm, "DIGIMINDS")
    canv.setFillColor(BRAND_ACCENT)
    canv.setFont("Helvetica-Bold", 13)
    canv.drawString(MARGIN_L + 35*mm, PAGE_H - 20*mm, "·")
    canv.setFillColor(white)
    canv.setFont("Helvetica", 10)
    canv.drawString(MARGIN_L + 38*mm, PAGE_H - 20*mm, "Performance Agency · Lahore · Global")
    # Footer
    canv.setFillColor(BRAND_MUTED)
    canv.setFont("Helvetica", 9)
    canv.drawCentredString(PAGE_W/2, 15*mm, f"© {datetime.now().year} DigiMinds · digiminds.org · Confidential — Internal & Client-Partner Use")
    canv.restoreState()

def content_page(canv, doc):
    canv.saveState()
    # Header strip
    canv.setStrokeColor(BRAND_RULE)
    canv.setLineWidth(0.5)
    canv.line(MARGIN_L, PAGE_H - 15*mm, PAGE_W - MARGIN_R, PAGE_H - 15*mm)
    canv.setFillColor(BRAND_PRIMARY)
    canv.setFont("Helvetica-Bold", 8)
    canv.drawString(MARGIN_L, PAGE_H - 12*mm, "DIGIMINDS")
    canv.setFillColor(BRAND_MUTED)
    canv.setFont("Helvetica", 8)
    canv.drawString(MARGIN_L + 20*mm, PAGE_H - 12*mm, "Chatbot Knowledge Base · v1.0")
    canv.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 12*mm, "digiminds.org")
    # Footer
    canv.setStrokeColor(BRAND_RULE)
    canv.line(MARGIN_L, 15*mm, PAGE_W - MARGIN_R, 15*mm)
    canv.setFillColor(BRAND_MUTED)
    canv.setFont("Helvetica", 8)
    canv.drawString(MARGIN_L, 11*mm, "Confidential")
    canv.drawCentredString(PAGE_W/2, 11*mm, "DigiMinds AI Chatbot · Knowledge Base & Conversion Engine")
    canv.setFillColor(BRAND_ACCENT)
    canv.setFont("Helvetica-Bold", 9)
    canv.drawRightString(PAGE_W - MARGIN_R, 11*mm, f"Page {doc.page}")
    canv.restoreState()

# ---------------- Content builders ----------------
story = []

def section_break():
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_RULE,
                            spaceBefore=4, spaceAfter=10))

def h1(text):
    story.append(Paragraph(md_inline(text), H1_STYLE))
    story.append(HRFlowable(width="30%", thickness=2, color=BRAND_ACCENT,
                            spaceBefore=0, spaceAfter=10))

def h2(text):
    story.append(Paragraph(md_inline(text), H2_STYLE))

def h3(text):
    story.append(Paragraph(md_inline(text), H3_STYLE))

def body(text, justify=False):
    sty = BODY_JUSTIFY if justify else BODY_STYLE
    story.append(Paragraph(md_inline(text), sty))

def bullet_list(items):
    flows = []
    for it in items:
        flows.append(ListItem(Paragraph(md_inline(it), BODY_STYLE),
                              leftIndent=12, bulletColor=BRAND_ACCENT))
    story.append(ListFlowable(flows, bulletType='bullet', start='•',
                              leftIndent=16, bulletFontSize=10,
                              bulletColor=BRAND_ACCENT))
    story.append(Spacer(1, 4))

def code_block(text):
    # Split into lines — reportlab doesn't handle \n in Paragraph well without <br/>
    lines = text.split("\n")
    content = "<br/>".join(safe(l).replace(" ", "&nbsp;") for l in lines)
    story.append(Paragraph(content, CODE_STYLE))

def info_table(rows, col_widths=None, header=True):
    if not rows:
        return
    # Pre-wrap cells as paragraphs
    wrapped = []
    for i, row in enumerate(rows):
        wrapped_row = []
        for cell in row:
            style = ParagraphStyle(
                f'cell{i}', fontName='Helvetica-Bold' if i == 0 and header else 'Helvetica',
                fontSize=9, leading=12,
                textColor=white if i == 0 and header else black
            )
            wrapped_row.append(Paragraph(md_inline(str(cell)), style))
        wrapped.append(wrapped_row)
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header else 0)
    ts = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, BRAND_RULE),
    ]
    if header:
        ts.extend([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, BRAND_ACCENT),
        ])
    # Alternate row shading
    for r in range(1, len(wrapped), 2):
        ts.append(('BACKGROUND', (0, r), (-1, r), BRAND_LIGHT_BG))
    t.setStyle(TableStyle(ts))
    story.append(t)
    story.append(Spacer(1, 8))

def callout(text, color=BRAND_ACCENT, label="NOTE"):
    p = Paragraph(f'<b><font color="{color.hexval()}">{label}:</font></b> {md_inline(text)}', BODY_STYLE)
    tbl = Table([[p]], colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 4*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BRAND_LIGHT_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (0,0), (0,-1), 3, color),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8))

# ---------------- Build: COVER ----------------
def build_cover():
    story.append(Spacer(1, 65*mm))
    # Document label (above title, on accent)
    label = ParagraphStyle('Lbl', fontName='Helvetica-Bold', fontSize=10,
                           textColor=BRAND_ACCENT, spaceAfter=6)
    story.append(Paragraph("KNOWLEDGE BASE & CONVERSION ENGINE · v1.0", label))
    story.append(Paragraph("DigiMinds AI<br/>Chatbot System", TITLE_STYLE))
    story.append(Paragraph(
        "A complete operational playbook for the chat agent deployed on digiminds.org — "
        "covering business profile, psychographic segmentation, 30+ indexed Q&A entries, "
        "ethics and de-escalation, competitive intelligence, conversation flows, "
        "objection handling, and deployment.",
        SUBTITLE_STYLE
    ))
    story.append(Spacer(1, 18*mm))

    # Meta block
    meta_rows = [
        ["PREPARED FOR", "DigiMinds — Performance Digital Marketing Agency"],
        ["HEADQUARTERS", "Ansari Market, Rehman Street, Lahore, Pakistan"],
        ["MARKETS", "Pakistan · United States · Canada · United Kingdom · UAE"],
        ["DOCUMENT DATE", datetime.now().strftime("%d %B %Y")],
        ["VERSION", "1.0 — Initial Release"],
        ["CLASSIFICATION", "Confidential — Internal & Implementation Partners"],
    ]
    mt = Table(meta_rows, colWidths=[45*mm, 120*mm])
    mt.setStyle(TableStyle([
        ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 8),
        ('FONT', (1,0), (1,-1), 'Helvetica', 9.5),
        ('TEXTCOLOR', (0,0), (0,-1), BRAND_MUTED),
        ('TEXTCOLOR', (1,0), (1,-1), BRAND_PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, BRAND_RULE),
    ]))
    story.append(mt)
    story.append(Spacer(1, 20*mm))
    # Bottom tagline
    tagline = ParagraphStyle('TL', fontName='Helvetica-Oblique', fontSize=11,
                             textColor=BRAND_MUTED, alignment=TA_LEFT)
    story.append(Paragraph('<font color="#E85D2C"><b>—</b></font> Zero fluff. Pure ROI. Performance-backed, 90-day guarantee.', tagline))

# ---------------- Build: EXECUTIVE SUMMARY ----------------
def build_exec_summary():
    story.append(PageBreak())
    h1("Executive Summary")
    body(
        "This document is the complete operational specification for <b>DigiBot</b>, the AI-powered "
        "conversational agent deployed on digiminds.org. The system is engineered for a single primary "
        "outcome: converting website visitors into qualified leads, booked calls, or WhatsApp "
        "conversations <b>before</b> they leave the chat — with human handoff reserved as a "
        "last-resort fallback.",
        justify=True
    )
    body(
        "The knowledge base was constructed from four inputs: (1) DigiMinds' own service architecture "
        "and guarantee framework, (2) analysis of the top 25 global and top 25 Pakistani competitors in "
        "the performance-marketing vertical, (3) voice-of-customer synthesis from Reddit, Quora, LinkedIn, "
        "Facebook, and Twitter/X threads covering agency hiring decisions, and (4) psychographic, "
        "demographic, and geographic segmentation across the five markets DigiMinds serves.",
        justify=True
    )

    h2("Design Principles")
    bullet_list([
        "<b>Every turn ends with a micro-action.</b> No passive replies — every message moves the visitor one step closer to commitment.",
        "<b>Specificity over generic warmth.</b> Responses name the service, the vertical, the number, and the next step.",
        "<b>Trust stack in every third message.</b> Certifications, real client outcomes, the 90-day guarantee, and data-ownership commitments.",
        "<b>Segment detection in the first two turns.</b> A US DTC founder receives a different tone, price range, and proof point than a Pakistani SMB owner or a UK enterprise buyer.",
        "<b>De-escalate hostility once; disengage on the second offense.</b> Never match tone. Log every hostile session for human review.",
        "<b>Human handoff is the last resort.</b> Exhaust self-serve answers first. Always capture a contact before escalating.",
    ])

    h2("Target Outcomes")
    info_table([
        ["METRIC", "BASELINE", "90-DAY TARGET", "STRETCH"],
        ["First-turn retention", "60%", "75%", "85%"],
        ["Segment detection accuracy", "—", "80%", "90%"],
        ["Average turns per session", "3", "6", "8"],
        ["Micro-action acceptance rate", "15%", "35%", "50%"],
        ["Booked call rate", "3%", "10%", "18%"],
        ["Form submission rate", "8%", "20%", "30%"],
        ["Email capture rate", "25%", "45%", "60%"],
        ["Handoff-to-human rate", "—", "< 15%", "< 8%"],
    ], col_widths=[55*mm, 30*mm, 35*mm, 30*mm])

# ---------------- Build: TABLE OF CONTENTS ----------------
def build_toc():
    story.append(PageBreak())
    h1("Table of Contents")
    toc_entries = [
        ("01", "Business Profile", "Ground-truth facts: services, guarantee, pricing, payment, declined verticals"),
        ("02", "Psychographic Segmentation", "Nine visitor segments × tone × path × micro-action"),
        ("03", "Core Knowledge Base", "Thirty indexed Q&A entries with conversion micro-actions"),
        ("04", "Ethics & De-Escalation Playbook", "Hostile visitors, vulgarity, and ethical edge-case handling"),
        ("05", "Competitive Intelligence Matrix", "Twenty-five global + twenty-five Pakistani competitors"),
        ("06", "Sample Conversation Flows", "Twelve end-to-end dialogues across all major segments"),
        ("07", "Objection Handling Playbook", "Twenty common objections with preempt, rebuttal, and close"),
        ("08", "Conversion Engine & Logic", "Micro-action hierarchy, trust scoring, escalation rules, KPIs"),
        ("09", "Deployment Guide", "Three shipping paths, stack options, launch checklist, analytics"),
        ("10", "Master System Prompt", "Copy-paste ready for any LLM provider"),
    ]
    for num, title, desc in toc_entries:
        row = [[
            Paragraph(f'<font color="{BRAND_ACCENT.hexval()}"><b>{num}</b></font>', TOC_NUM),
            Paragraph(f'<b>{title}</b><br/><font size="9" color="{BRAND_MUTED.hexval()}">{desc}</font>', TOC_ENTRY),
        ]]
        t = Table(row, colWidths=[12*mm, 150*mm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 0.25, BRAND_RULE),
            ('TOPPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)

# ---------------- Section 01: Business Profile ----------------
def section_business_profile():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "01_business_profile.json")) as f:
        d = json.load(f)
    h1("01 · Business Profile")
    body("Verified facts about DigiMinds used as the authoritative source for all chatbot responses. Never contradict, embellish, or invent beyond the data on this page.", justify=True)

    h2("Company")
    c = d["company"]
    info_table([
        ["FIELD", "VALUE"],
        ["Name", c["name"]],
        ["Tagline", c["tagline"]],
        ["Website", c["website"]],
        ["Founded", c["founded"]],
        ["Headquarters", f'{c["hq"]["address"]}'],
        ["Markets Served", " · ".join(c["markets_served"])],
        ["Positioning", c["positioning"]],
    ], col_widths=[40*mm, 125*mm])

    h2("Service Pillars")
    for key, svc in d["services"].items():
        h3(svc["label"])
        lines = []
        for k, v in svc.items():
            if k == "label": continue
            if isinstance(v, list):
                v = ", ".join(v)
            elif isinstance(v, dict):
                v = " · ".join(f"{kk}: {vv if not isinstance(vv, list) else ', '.join(vv)}" for kk, vv in v.items())
            lines.append(f"<b>{k.replace('_',' ').title()}:</b> {v}")
        for line in lines:
            body(line)

    h2("Certifications & Partners")
    bullet_list(d["certifications_and_partners"])

    h2("90-Day Performance Guarantee")
    g = d["guarantee"]
    callout(g["definition"], color=BRAND_ACCENT, label="DEFINITION")
    h3("Conditions")
    bullet_list(g["conditions"])

    h2("Pricing Framework")
    body(f'<b>Public pricing policy:</b> {d["pricing_framework"]["public_pricing_policy"]}')
    ranges = d["pricing_framework"]["approved_ranges_for_chatbot"]
    info_table(
        [["TIER", "RANGE"]] + [[k.replace("_", " ").title(), v] for k, v in ranges.items()],
        col_widths=[65*mm, 100*mm]
    )

    h3("Payment Methods")
    pm = d["pricing_framework"]["payment_methods"]
    body(f'<b>Pakistan clients:</b> {" · ".join(pm["pakistan_clients"])}')
    body(f'<b>International:</b> {" · ".join(pm["international"])}')
    body(f'<b>Not accepted:</b> {" · ".join(pm["not_accepted"])}')

    h2("Case Study Outcome Templates")
    callout(d["case_study_templates"]["instruction_for_chatbot"], color=BRAND_WARNING, label="INSTRUCTION")
    for k, v in d["case_study_templates"].items():
        if k == "instruction_for_chatbot": continue
        h3(k.replace("_", " ").title())
        body(v)

    h2("Brand Voice")
    bv = d["brand_voice"]
    body(f'<b>Voice adjectives:</b> {", ".join(bv["adjectives"])}')
    body(f'<b>Avoid:</b> {", ".join(bv["avoid"])}')
    h3("Signature Phrases")
    bullet_list([f'"{p}"' for p in bv["signature_phrases"]])

    h2("Declined Verticals")
    callout("DigiMinds does not accept engagements in the following categories under any circumstance.", color=BRAND_WARNING, label="POLICY")
    bullet_list(d["declined_verticals"])

    h2("Contact Channels")
    cc = d["contact_channels"]
    info_table([["CHANNEL", "DETAIL"]] + [[k.replace("_", " ").title(), v] for k, v in cc.items()], col_widths=[45*mm, 120*mm])

# ---------------- Section 02: Segments ----------------
def section_segments():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "02_psychographic_segments.json")) as f:
        d = json.load(f)
    h1("02 · Psychographic Segmentation")
    body(d["meta"]["purpose"], justify=True)

    h2("Detection Signals")
    bullet_list(d["meta"]["detection_signals"])

    for seg in d["segments"]:
        story.append(PageBreak())
        h2(f'{seg["id"]} · {seg["label"]}')
        dem = seg["demographics"]
        info_table([
            ["DEMOGRAPHIC", "VALUE"],
            *[[k.replace("_", " ").title(),
               ", ".join(v) if isinstance(v, list) else str(v)] for k, v in dem.items()]
        ], col_widths=[45*mm, 120*mm])

        psy = seg["psychographics"]
        h3("Psychographics")
        body(f'<b>Values:</b> {", ".join(psy["values"])}')
        body(f'<b>Motivation:</b> {psy["motivation"]}')
        body(f'<b>Decision style:</b> {psy["decision_style"]}')
        body(f'<b>Frictions:</b> {", ".join(psy["frictions"])}')

        h3("Engagement Blueprint")
        info_table([
            ["FIELD", "VALUE"],
            ["Language", seg["language"]],
            ["Tone", seg["tone"]],
            ["Proof Points", " · ".join(seg["proof_points_to_lead_with"])],
            ["Pricing Range", seg["pricing_range"]],
            ["Preferred Micro-Action", seg["preferred_micro_action"]],
            ["Channels", " · ".join(seg["channels"])],
            ["Likely Objections", ", ".join(seg["objections_likely"])],
            ["Messaging Hooks", " · ".join(seg["messaging_hooks"])],
        ], col_widths=[45*mm, 120*mm])

    story.append(PageBreak())
    h2("Segment Detection Rules")
    rules = d["segment_detection_rules"]
    info_table(
        [["SIGNAL", "ROUTE TO"]] + [[r["signal"], r["route_to"]] for r in rules],
        col_widths=[110*mm, 55*mm]
    )

# ---------------- Section 03: Core KB ----------------
def section_kb():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "03_knowledge_base.json")) as f:
        d = json.load(f)
    h1("03 · Core Knowledge Base")
    body("Indexed Q→A→micro-action entries. Each entry is retrieval-ready: semantic search on <i>question_variants</i> returns the response. The <b>micro-action</b> field is the conversion nudge delivered at the end of every reply.", justify=True)

    callout(f'Version {d["meta"]["version"]} contains {len(d["entries"])} entries. See the expansion plan at the end of this section for the 300–500 entry roadmap.', color=BRAND_ACCENT, label="SCOPE")

    # Group by category
    from collections import defaultdict
    by_cat = defaultdict(list)
    for e in d["entries"]:
        by_cat[e["category"]].append(e)

    for cat, entries in by_cat.items():
        h2(cat.replace("_", " ").title())
        for e in entries:
            # Entry card
            cells = [
                [Paragraph(f'<b><font color="{BRAND_ACCENT.hexval()}">{e["id"]}</font></b>  <font color="{BRAND_MUTED.hexval()}" size="8">{e["stage"].upper()} · {e["tone"].upper()}</font>', BODY_STYLE)],
                [Paragraph(f'<b>Question variants:</b><br/>{" · ".join(f"&ldquo;{md_inline(q)}&rdquo;" for q in e["question_variants"])}', BODY_STYLE)],
                [Paragraph(f'<b>Answer:</b><br/>{md_inline(e["answer"])}', BODY_STYLE)],
            ]
            if e.get("proof_point"):
                cells.append([Paragraph(f'<b>Proof point:</b><br/>{md_inline(e["proof_point"])}', BODY_STYLE)])
            cells.append([Paragraph(f'<b><font color="{BRAND_ACCENT.hexval()}">Micro-action →</font></b>  {md_inline(e["micro_action"])}', BODY_STYLE)])
            cells.append([Paragraph(f'<font size="8" color="{BRAND_MUTED.hexval()}">Segments: {", ".join(e["segment_tags"])}  ·  Geo: {", ".join(e["geo_tags"])}</font>', BODY_STYLE)])
            t = Table(cells, colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 4*mm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), BRAND_LIGHT_BG),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LINEBEFORE', (0,0), (0,-1), 3, BRAND_ACCENT),
                ('LINEBELOW', (0, 0), (-1, 0), 0.25, BRAND_RULE),
            ]))
            story.append(KeepTogether(t))
            story.append(Spacer(1, 6))

    h2("Expansion Roadmap")
    body(d["expansion_plan"]["note"], justify=True)
    bullet_list(d["expansion_plan"]["priority_expansion_categories"])

# ---------------- Section 04: Ethics ----------------
def section_ethics():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "04_ethics_sensitive_playbook.json")) as f:
        d = json.load(f)
    h1("04 · Ethics & De-Escalation Playbook")
    body(d["meta"]["purpose"], justify=True)

    h2("Universal Rules")
    bullet_list(d["meta"]["universal_rules"])

    h2("Vulgar & Hostile Visitor Patterns")
    for key, p in d["vulgar_hostile_patterns"].items():
        h3(key.replace("_", " ").title())
        body(f"<b>Example triggers:</b>")
        bullet_list([f'&ldquo;{md_inline(x)}&rdquo;' for x in p["examples"]])
        body(f"<b>Response pattern:</b> {p['response_pattern']}", justify=True)
        body("<b>Response templates:</b>")
        for t in p["response_templates"]:
            callout(t, color=BRAND_ACCENT, label="TEMPLATE")
        body(f"<b>Micro-action:</b> {p['micro_action']}")
        body(f"<b>Disengage trigger:</b> {p['disengage_trigger']}")
        section_break()

    story.append(PageBreak())
    h2("Ethical Edge-Case Requests")
    for key, e in d["ethical_edge_case_requests"].items():
        h3(key.replace("_", " ").title())
        body("<b>Request examples:</b>")
        bullet_list([f'&ldquo;{md_inline(x)}&rdquo;' for x in e["visitor_request_examples"]])
        body(f"<b>Response:</b> {e['response']}", justify=True)
        body(f"<b>Micro-action:</b> {e['micro_action']}")
        decline = str(e.get("decline_firmly", ""))
        if decline == "True":
            callout("Decline firmly under all circumstances.", color=BRAND_WARNING, label="POLICY")
        elif decline == "conditional":
            callout("Conditional — proceed only with full compliance documentation.", color=BRAND_WARNING, label="POLICY")
        section_break()

    h2("De-Escalation Matrix")
    rows = [["TURN", "ACTION"]]
    for k, v in d["de_escalation_matrix"].items():
        if k == "never_do": continue
        rows.append([k.replace("_", " ").title(), v])
    info_table(rows, col_widths=[50*mm, 115*mm])

    h3("Never-Do List")
    bullet_list(d["de_escalation_matrix"]["never_do"])

    h2("Logging Triggers")
    bullet_list(d["logging_triggers"])

# ---------------- Section 05: Competitors ----------------
def section_competitors():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "05_competitor_matrix.json")) as f:
        d = json.load(f)
    h1("05 · Competitive Intelligence Matrix")
    body(d["meta"]["purpose"], justify=True)
    h2("DigiMinds Core Differentiators")
    bullet_list(d["meta"]["digiminds_core_differentiators"])

    h2("Top 25 Global Competitors")
    rows = [["#", "AGENCY", "POSITIONING", "WEAKNESS", "DIGIMINDS WINS WHEN"]]
    for i, c in enumerate(d["global_competitors"], 1):
        rows.append([str(i), c["name"], c["positioning"], c["weakness"], c["digiminds_wins_when"]])
    info_table(rows, col_widths=[8*mm, 30*mm, 42*mm, 42*mm, 45*mm])

    story.append(PageBreak())
    h2("Top 25 Pakistani Competitors")
    rows = [["#", "AGENCY", "CITY", "STRENGTH", "DIGIMINDS WINS WHEN"]]
    for i, c in enumerate(d["pakistani_competitors"], 1):
        rows.append([str(i), c["name"], c["city"], c["strength"], c["digiminds_wins_when"]])
    info_table(rows, col_widths=[8*mm, 35*mm, 22*mm, 50*mm, 50*mm])

    h2("Battle-Card Templates")
    for k, v in d["battle_card_templates"].items():
        h3(k.replace("_", " ").title())
        callout(v, color=BRAND_ACCENT, label="POSITIONING")

# ---------------- Section 06: Conversation Flows ----------------
def section_flows():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "06_conversation_flows.md")) as f:
        raw = f.read()
    h1("06 · Sample Conversation Flows")
    body("Twelve end-to-end dialogues illustrating segment detection, objection handling, and conversion across every major visitor profile. Use as reference, not rigid script.", justify=True)
    _render_markdown(raw, skip_h1=True)

# ---------------- Section 07: Objections ----------------
def section_objections():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "07_objection_playbook.json")) as f:
        d = json.load(f)
    h1("07 · Objection Handling Playbook")
    body(d["meta"]["principle"], justify=True)

    for obj in d["objections"]:
        cells = [
            [Paragraph(f'<b><font color="{BRAND_ACCENT.hexval()}">{obj["id"]}</font></b>  <b>{obj["name"]}</b>', H3_STYLE)],
            [Paragraph(f'<b>Trigger phrases:</b> {" · ".join(f"&ldquo;{md_inline(p)}&rdquo;" for p in obj["trigger_phrases"])}', BODY_STYLE)],
            [Paragraph(f'<b>Preempt:</b> {md_inline(obj["preempt"])}', BODY_STYLE)],
            [Paragraph(f'<b>Rebuttal:</b> {md_inline(obj["rebuttal"])}', BODY_STYLE)],
        ]
        if obj.get("proof"):
            cells.append([Paragraph(f'<b>Proof:</b> {md_inline(obj["proof"])}', BODY_STYLE)])
        cells.append([Paragraph(f'<b><font color="{BRAND_ACCENT.hexval()}">Micro-action →</font></b> {md_inline(obj["micro_action"])}', BODY_STYLE)])
        cells.append([Paragraph(f'<b><font color="{BRAND_WARNING.hexval()}">Do not say:</font></b> {", ".join(f"&ldquo;{md_inline(x)}&rdquo;" for x in obj["do_not_say"])}', BODY_STYLE)])
        t = Table(cells, colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 4*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BRAND_LIGHT_BG),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LINEBEFORE', (0,0), (0,-1), 3, BRAND_ACCENT),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 8))

    h2("Signals of Hesitation to Preempt")
    bullet_list(d["common_signals_of_hesitation_to_preempt"])

    callout(d["rebuttal_stacking_rule"], color=BRAND_WARNING, label="STACKING RULE")

# ---------------- Section 08: Conversion Engine ----------------
def section_conversion_engine():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "08_conversion_engine.md")) as f:
        raw = f.read()
    h1("08 · Conversion Engine & Logic")
    _render_markdown(raw, skip_h1=True)

# ---------------- Section 09: Deployment Guide ----------------
def section_deployment():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "09_deployment_guide.md")) as f:
        raw = f.read()
    h1("09 · Deployment Guide")
    _render_markdown(raw, skip_h1=True)

# ---------------- Section 10: Master System Prompt ----------------
def section_system_prompt():
    story.append(PageBreak())
    with open(os.path.join(KB_DIR, "00_system_prompt.md")) as f:
        raw = f.read()
    h1("10 · Master System Prompt")
    body("Copy-paste directly into the system message field of GPT-4o, Claude Sonnet 4.6, Gemini 2.0, or any compatible LLM. All retrieval context references the JSON and Markdown files in this knowledge base.", justify=True)
    _render_markdown(raw, skip_h1=True)

# ---------------- Final page ----------------
def build_close():
    story.append(PageBreak())
    h1("End of Document")
    body("This knowledge base is a living system. Every real chat conversation produces signal — route unresolved questions, surprising objections, and new visitor patterns back into the source files weekly, then re-embed the vector store.", justify=True)
    story.append(Spacer(1, 6*mm))
    callout(
        "Hand the <b>digiminds-chatbot-kb/</b> folder to your implementation partner. Everything needed to ship is in these ten files. Path 1 (GoHighLevel + OpenAI) is live in two to four business days.",
        color=BRAND_ACCENT, label="NEXT STEP"
    )
    story.append(Spacer(1, 10*mm))

    story.append(HRFlowable(width="100%", thickness=1, color=BRAND_PRIMARY))
    story.append(Spacer(1, 4*mm))
    body(f'<font color="{BRAND_MUTED.hexval()}" size="9">Prepared {datetime.now().strftime("%d %B %Y")} · Version 1.0 · Confidential</font>')
    body(f'<font color="{BRAND_PRIMARY.hexval()}"><b>DIGIMINDS</b></font> <font color="{BRAND_MUTED.hexval()}" size="9">· Ansari Market, Rehman Street, Lahore · digiminds.org · hello@digiminds.org</font>')

# ---------------- Markdown mini-renderer (for .md files) ----------------
def _render_markdown(text, skip_h1=False):
    """Render a markdown file into reportlab flowables. Minimal: headings, paragraphs, lists, tables, code blocks, horizontal rules."""
    lines = text.split("\n")
    i = 0
    n = len(lines)
    in_code = False
    code_buf = []
    list_buf = []

    def flush_list():
        nonlocal list_buf
        if list_buf:
            bullet_list(list_buf)
            list_buf = []

    def flush_code():
        nonlocal code_buf, in_code
        if code_buf:
            code_block("\n".join(code_buf))
            code_buf = []
        in_code = False

    while i < n:
        line = lines[i].rstrip()
        # Code fence
        if line.startswith("```"):
            if in_code:
                flush_code()
            else:
                flush_list()
                in_code = True
            i += 1; continue
        if in_code:
            code_buf.append(line)
            i += 1; continue

        if not line.strip():
            flush_list()
            story.append(Spacer(1, 3))
            i += 1; continue

        # Horizontal rule
        if re.match(r'^-{3,}$', line.strip()):
            flush_list()
            story.append(HRFlowable(width="100%", thickness=0.4, color=BRAND_RULE, spaceBefore=4, spaceAfter=6))
            i += 1; continue

        # Headings
        if line.startswith("# "):
            flush_list()
            if not skip_h1:
                h1(line[2:].strip())
            else:
                # promote to h2 since we already have the section h1
                h2(line[2:].strip())
            i += 1; continue
        if line.startswith("## "):
            flush_list()
            h2(line[3:].strip())
            i += 1; continue
        if line.startswith("### "):
            flush_list()
            h3(line[4:].strip())
            i += 1; continue
        if line.startswith("#### "):
            flush_list()
            h3(line[5:].strip())
            i += 1; continue

        # Tables
        if "|" in line and i+1 < n and re.match(r'^\s*\|?\s*[-:| ]+\s*\|?\s*$', lines[i+1]):
            flush_list()
            # Collect table
            tbl_lines = [line]
            sep = lines[i+1]
            j = i + 2
            while j < n and "|" in lines[j] and lines[j].strip():
                tbl_lines.append(lines[j])
                j += 1
            rows = []
            for tl in [tbl_lines[0]] + tbl_lines[1:]:
                cells = [c.strip() for c in tl.strip().strip("|").split("|")]
                rows.append(cells)
            # Auto column widths
            total_w = PAGE_W - MARGIN_L - MARGIN_R - 4*mm
            n_cols = len(rows[0])
            cw = [total_w / n_cols] * n_cols
            info_table(rows, col_widths=cw)
            i = j; continue

        # Bullet
        if re.match(r'^\s*[-*+]\s+', line):
            m = re.match(r'^\s*[-*+]\s+(.*)', line)
            list_buf.append(m.group(1))
            i += 1; continue

        # Numbered bullet (just render as paragraph to avoid complexity)
        if re.match(r'^\s*\d+\.\s+', line):
            flush_list()
            body(line.strip())
            i += 1; continue

        # Blockquote
        if line.startswith(">"):
            flush_list()
            callout(line[1:].strip(), color=BRAND_MUTED, label="NOTE")
            i += 1; continue

        # Normal paragraph (may span)
        flush_list()
        para = [line]
        j = i + 1
        while j < n and lines[j].strip() and not any(lines[j].startswith(x) for x in ["#", "- ", "* ", "+ ", "```", ">"]) and "|" not in lines[j]:
            para.append(lines[j].rstrip())
            j += 1
        body(" ".join(para))
        i = j

    flush_list()
    flush_code()

# ---------------- Page Template setup ----------------
class KBDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4,
                         leftMargin=MARGIN_L, rightMargin=MARGIN_R,
                         topMargin=MARGIN_T, bottomMargin=MARGIN_B,
                         title="DigiMinds Chatbot Knowledge Base",
                         author="DigiMinds",
                         subject="AI Chatbot Knowledge Base v1.0",
                         creator="DigiMinds")
        frame_full = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                           PAGE_H - MARGIN_T - MARGIN_B, id='full',
                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[frame_full], onPage=cover_page),
            PageTemplate(id='content', frames=[frame_full], onPage=content_page),
        ])

# ---------------- Assemble ----------------
def main():
    build_cover()
    story.append(NextPageTemplate('content'))
    build_exec_summary()
    build_toc()
    section_business_profile()
    section_segments()
    section_kb()
    section_ethics()
    section_competitors()
    section_flows()
    section_objections()
    section_conversion_engine()
    section_deployment()
    section_system_prompt()
    build_close()

    doc = KBDoc(OUT_PDF)
    doc.build(story)
    size_kb = os.path.getsize(OUT_PDF) / 1024
    print(f"[OK] PDF built: {OUT_PDF} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
