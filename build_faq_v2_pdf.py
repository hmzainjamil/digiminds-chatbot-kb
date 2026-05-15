#!/usr/bin/env python3
"""DigiMinds FAQ Knowledge Base v2 — with Contact Details prominently included."""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

OUT = "/Users/mc/digiminds-chatbot-kb/DigiMinds_FAQ_KB_v2.pdf"

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY   = HexColor("#1F3864")
ORANGE = HexColor("#E8590C")
LGREY  = HexColor("#F2F2F2")
MGREY  = HexColor("#CCCCCC")
DGREY  = HexColor("#555555")

PAGE_W, PAGE_H = LETTER
M = 1 * inch

# ── Styles ────────────────────────────────────────────────────────────────────
def s(name, **kw):
    kw.pop("parent", None)
    defaults = dict(fontName="Helvetica", fontSize=11, leading=16, textColor=black)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

TITLE_S  = s("title",  fontName="Helvetica-Bold", fontSize=26,
             textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
SUBT_S   = s("subt",   fontName="Helvetica", fontSize=13,
             textColor=DGREY, alignment=TA_CENTER, spaceAfter=4)
DATE_S   = s("date",   fontName="Helvetica", fontSize=10,
             textColor=MGREY, alignment=TA_CENTER, spaceAfter=20)
H1_S     = s("h1",     fontName="Helvetica-Bold", fontSize=15,
             textColor=NAVY, spaceBefore=16, spaceAfter=6)
H2_S     = s("h2",     fontName="Helvetica-Bold", fontSize=12,
             textColor=NAVY, spaceBefore=10, spaceAfter=4)
BODY_S   = s("body",   fontSize=11, leading=17, spaceBefore=2, spaceAfter=4)
BOLD_S   = s("bold",   fontName="Helvetica-Bold", fontSize=11, leading=17)
Q_S      = s("q",      fontName="Helvetica-Bold", fontSize=11,
             textColor=NAVY, leading=17)
A_S      = s("a",      fontSize=11, leading=17, leftIndent=10)
LABEL_S  = s("label",  fontName="Helvetica-Bold", fontSize=11, textColor=NAVY)
VAL_S    = s("val",    fontSize=11)
FOOTER_S = s("footer", fontSize=9, textColor=DGREY, alignment=TA_CENTER)

# ── Page callbacks ─────────────────────────────────────────────────────────────
def draw_header(canvas, doc):
    canvas.saveState()
    # Top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 0.45*inch, PAGE_W, 0.45*inch, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(M, PAGE_H - 0.30*inch, "DigiMinds — FAQ & Contact Reference")
    # Page number (right)
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(PAGE_W - M, PAGE_H - 0.30*inch, f"Page {doc.page}")
    # Bottom rule
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1)
    canvas.line(M, 0.55*inch, PAGE_W - M, 0.55*inch)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(DGREY)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, "© 2026 DigiMinds Ltd · Lahore, Pakistan · hello@digiminds.org")
    canvas.restoreState()

def draw_cover_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(MGREY)
    canvas.setLineWidth(0.5)
    canvas.line(M, 0.55*inch, PAGE_W - M, 0.55*inch)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(DGREY)
    canvas.drawCentredString(PAGE_W/2, 0.35*inch, "© 2026 DigiMinds Ltd · digiminds.org")
    canvas.restoreState()

# ── Helpers ───────────────────────────────────────────────────────────────────
def hr(color=NAVY, thickness=1.2):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8)

def qa_block(num, q, answer_lines):
    """Render one Q/A with left-border box on Q."""
    q_para = Paragraph(f"Q{num}.  {q}", Q_S)
    tbl = Table([[q_para]], colWidths=[PAGE_W - 2*M])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), HexColor("#EFF3FB")),
        ("LINEBEFORE",  (0,0), (0,-1), 4, NAVY),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 8),
    ]))
    items = [tbl]
    for line in answer_lines:
        items.append(Paragraph(line, A_S))
    items.append(Spacer(1, 10))
    return items

def contact_row(label, value):
    return [Paragraph(label, LABEL_S), Paragraph(value, VAL_S)]

# ── Content data ──────────────────────────────────────────────────────────────

CONTACT = {
    "Phone / WhatsApp": "+92 371 4232502",
    "Email":            "info@digiminds.org",
    "Business Email":   "hello@digiminds.org",
    "Book a Free Call": "calendly.com/digimindsltd/30min",
    "Address":          "Ansari Market, Unit #05, Rehman Street,\nBrandreth Road, Lahore 54010, Punjab, Pakistan",
    "Website":          "digiminds.org",
    "Facebook":         "facebook.com/digimindsltd",
    "LinkedIn":         "linkedin.com/company/digimindsltd",
    "Instagram":        "instagram.com/digimindsltd",
}

SERVICES = [
    ("Performance Marketing",
     "Meta Ads, Google Ads, TikTok Ads — full-funnel campaign strategy, creative testing, "
     "bid optimisation, and ROAS-focused scaling."),
    ("Search Engine Optimisation (SEO)",
     "Technical SEO, on-page, off-page link-building, and content strategy to drive "
     "sustainable organic traffic."),
    ("Tracking & Analytics",
     "Server-side tracking, GA4 migration, Meta CAPI, Google Tag Manager, custom "
     "attribution dashboards — fix measurement before you scale."),
    ("CRM & Marketing Automation",
     "GoHighLevel setup, pipeline design, lead-nurture workflows, and automated "
     "follow-up sequences."),
    ("Web & Landing Page Design",
     "Conversion-optimised landing pages, Webflow / WordPress builds, and "
     "A/B testing frameworks."),
    ("Fractional CMO",
     "Part-time Chief Marketing Officer — strategy, team leadership, and execution "
     "oversight for growing businesses that aren't ready for a full-time hire."),
]

FAQS = [
    (
        "What services does DigiMinds offer?",
        [
            "DigiMinds is a full-service digital marketing agency. Core services include:",
            "• <b>Performance Marketing</b> — Meta Ads, Google Ads, TikTok Ads",
            "• <b>SEO</b> — technical, on-page, off-page, and content",
            "• <b>Tracking & Analytics</b> — server-side tracking, GA4, Meta CAPI",
            "• <b>CRM & Automation</b> — GoHighLevel, lead nurture, pipelines",
            "• <b>Web & Landing Pages</b> — conversion-optimised design & A/B testing",
            "• <b>Fractional CMO</b> — part-time strategic leadership",
        ]
    ),
    (
        "What makes DigiMinds different from other agencies?",
        [
            "Three things set DigiMinds apart:",
            "1. <b>Senior-only delivery</b> — every account is handled by a senior strategist, "
               "not juniors. You meet them before you sign.",
            "2. <b>90-day performance guarantee</b> — if agreed KPIs are not met, DigiMinds "
               "keeps working at no charge until they are, or refunds management fees.",
            "3. <b>Honest scoping</b> — if your ad spend is under $3k/month, DigiMinds will "
               "tell you that a full retainer isn't right for you yet.",
        ]
    ),
    (
        "Do you work with international clients?",
        [
            "Yes. DigiMinds serves clients across the US, UK, Canada, UAE, and Pakistan.",
            "• US/UK invoicing via US LLC + Stripe",
            "• International payments via Wise, Payoneer, or bank wire",
            "• Account managers overlap with PT, ET, and GMT time zones",
            "• Weekly calls and Slack/email responses during your business hours",
        ]
    ),
    (
        "What is your pricing?",
        [
            "Pricing is custom-scoped based on your vertical, ad spend, and deliverables. "
            "Indicative ranges:",
            "• <b>Starter retainer (PK market)</b>: PKR 150,000/month",
            "• <b>International retainer</b>: USD 2,500 – 8,000/month",
            "• <b>One-time audit</b>: USD 2,500 (credits against future retainer)",
            "• Retainer is typically 6–15% of managed ad spend",
            "No Silver/Gold/Platinum packages — every engagement is custom-scoped.",
        ]
    ),
    (
        "What is the 90-day performance guarantee?",
        [
            "KPIs are agreed in writing at kickoff. If DigiMinds misses them within 90 days:",
            "• They continue working at no charge until targets are hit, OR",
            "• Management fees are refunded",
            "<b>Conditions:</b> client maintains minimum agreed ad spend, provides account "
            "access, and does not change scope mid-flight. Ad spend itself is never refunded "
            "(it belongs to the platform). Full 2-page guarantee PDF available on request.",
        ]
    ),
    (
        "What industries do you work with?",
        [
            "DigiMinds serves a wide range of verticals including:",
            "• DTC / e-commerce (fashion, beauty, supplements, homewares)",
            "• SaaS and B2B software",
            "• Local services (HVAC, dental, legal, real estate)",
            "• Relocation and immigration services",
            "• Education and EdTech",
            "• Pakistani exporters and SMEs scaling internationally",
            "<b>Declined verticals</b>: gambling, adult content, unregulated crypto schemes, "
            "tobacco, MLM.",
        ]
    ),
    (
        "How do I get started?",
        [
            "Three ways to start:",
            "1. <b>Book a free 30-minute discovery call</b>: calendly.com/digimindsltd/30min",
            "2. <b>Email directly</b>: hello@digiminds.org",
            "3. <b>WhatsApp / Call</b>: +92 371 4232502",
            "The discovery call covers your current setup, goals, and whether DigiMinds is "
            "the right fit. No pitch — just a conversation.",
        ]
    ),
    (
        "What tracking and analytics setup do you provide?",
        [
            "DigiMinds treats measurement as a pre-condition, not an afterthought:",
            "• Server-side tracking (fixes iOS 14+ signal loss)",
            "• Meta Conversions API (CAPI) implementation",
            "• GA4 migration and event configuration",
            "• Google Tag Manager audit and rebuild",
            "• Custom attribution dashboards (Looker Studio / Metabase)",
            "• Consent Mode v2 for GDPR compliance",
            "Tracking is included in retainer scopes or available as a standalone engagement.",
        ]
    ),
    (
        "What payment methods do you accept?",
        [
            "<b>Pakistan clients</b>: IBFT bank transfer, JazzCash, EasyPaisa, cheque",
            "<b>International clients</b>: Wise, Payoneer, bank wire, Stripe (USD via US LLC), USDT",
            "Note: PayPal is not available due to PK merchant restrictions.",
            "Full payment options are confirmed at the proposal stage.",
        ]
    ),
]

GUARANTEE_DETAIL = (
    "The DigiMinds 90-Day Guarantee is a written performance commitment. KPIs "
    "(typically ROAS, CPL, or organic traffic growth) are agreed before kickoff. "
    "If those KPIs are not achieved within 90 days — and the client has upheld their "
    "obligations (minimum ad spend, account access, no mid-flight scope changes) — "
    "DigiMinds will either continue working at no additional cost until the targets are "
    "met, or refund the management fees paid. Ad spend is not refunded as it is paid "
    "directly to ad platforms. Full terms available in the 2-page guarantee PDF sent "
    "upon request."
)

# ── Build document ────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUT,
        pagesize=LETTER,
        leftMargin=M, rightMargin=M,
        topMargin=M + 0.5*inch, bottomMargin=M,
        title="DigiMinds FAQ & Contact Reference",
        author="DigiMinds Ltd",
        subject="FAQ Knowledge Base v2",
    )

    cover_frame   = Frame(M, M, PAGE_W-2*M, PAGE_H-2*M, id="cover")
    content_frame = Frame(M, M, PAGE_W-2*M, PAGE_H-2*M - 0.45*inch, id="content",
                          topPadding=0.55*inch)

    cover_tpl   = PageTemplate(id="Cover",   frames=[cover_frame],
                               onPage=draw_cover_footer)
    content_tpl = PageTemplate(id="Content", frames=[content_frame],
                               onPage=draw_header)
    doc.addPageTemplates([cover_tpl, content_tpl])

    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.6*inch))

    # Logo bar
    logo_tbl = Table([[Paragraph("<b>DigiMinds</b>", s("logo",
        fontName="Helvetica-Bold", fontSize=36, textColor=white, alignment=TA_CENTER))
    ]], colWidths=[PAGE_W - 2*M])
    logo_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 18),
        ("BOTTOMPADDING", (0,0),(-1,-1), 18),
    ]))
    story.append(logo_tbl)
    story.append(Spacer(1, 0.25*inch))

    # Orange rule
    story.append(HRFlowable(width="100%", thickness=4, color=ORANGE, spaceAfter=18))

    story.append(Paragraph("FAQ & Contact Reference", TITLE_S))
    story.append(Paragraph("Services · Frequently Asked Questions · Contact Details", SUBT_S))
    story.append(Paragraph(
        f"Based on verified content from digiminds.org  ·  "
        f"Generated {datetime.date.today().strftime('%B %d, %Y')}",
        DATE_S))

    story.append(Spacer(1, 0.4*inch))
    story.append(HRFlowable(width="60%", thickness=0.75, color=MGREY, spaceAfter=18))

    # Quick-contact on cover
    cover_contact = [
        ["📞  Phone / WhatsApp", "+92 371 4232502"],
        ["✉️  Email",             "hello@digiminds.org"],
        ["🗓  Book Free Call",    "calendly.com/digimindsltd/30min"],
        ["🌐  Website",           "digiminds.org"],
    ]
    ctbl = Table(cover_contact, colWidths=[2.4*inch, PAGE_W - 2*M - 2.4*inch])
    ctbl.setStyle(TableStyle([
        ("FONTNAME",      (0,0),(-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0),(-1,-1), 11),
        ("FONTNAME",      (0,0),(0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,0),(0,-1),  NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LINEBELOW",     (0,0),(-1,-2), 0.5, MGREY),
    ]))
    story.append(ctbl)

    story.append(Spacer(1, 0.5*inch))
    disclaimer = (
        "This document is for internal and client-facing reference only. "
        "All content is sourced directly from digiminds.org with no estimations or invented data."
    )
    dtbl = Table([[Paragraph(disclaimer, s("disc", fontSize=9, textColor=DGREY,
                                            alignment=TA_CENTER))]],
                 colWidths=[PAGE_W - 2*M])
    dtbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LGREY),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
    ]))
    story.append(dtbl)

    # Switch to content template
    story.append(PageBreak())
    from reportlab.platypus import NextPageTemplate
    story.insert(len(story)-1, NextPageTemplate("Content"))

    # ── SECTION 1: CONTACT DETAILS ────────────────────────────────────────────
    story.append(Paragraph("1.  Contact Details", H1_S))
    story.append(hr())
    story.append(Paragraph(
        "All contact information is sourced directly from digiminds.org/contact/.",
        s("note", fontSize=10, textColor=DGREY, spaceAfter=10)
    ))

    rows = [[contact_row(k, v)[0], contact_row(k, v)[1]] for k, v in CONTACT.items()]
    ctbl2 = Table(rows, colWidths=[2.2*inch, PAGE_W - 2*M - 2.2*inch])
    ctbl2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  HexColor("#DDE3F0")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("LINEBELOW",     (0,0), (-1,-2), 0.5, MGREY),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [LGREY, white]),
        ("LINEBEFORE",    (0,0), (0,-1),  3, NAVY),
    ]))
    story.append(ctbl2)
    story.append(Spacer(1, 14))

    # Book a call CTA box
    cta = Table([[Paragraph(
        "📅  <b>Book a free 30-minute discovery call:</b>  "
        "calendly.com/digimindsltd/30min",
        s("cta", fontName="Helvetica-Bold", fontSize=12,
          textColor=white, alignment=TA_CENTER)
    )]], colWidths=[PAGE_W - 2*M])
    cta.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), ORANGE),
        ("TOPPADDING",    (0,0),(-1,-1), 12),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
    ]))
    story.append(cta)
    story.append(Spacer(1, 20))

    # ── SECTION 2: SERVICES OVERVIEW ─────────────────────────────────────────
    story.append(Paragraph("2.  Services Overview", H1_S))
    story.append(hr())

    for title, desc in SERVICES:
        story.append(Paragraph(f"<b>{title}</b>", H2_S))
        story.append(Paragraph(desc, BODY_S))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # ── SECTION 3: FREQUENTLY ASKED QUESTIONS ────────────────────────────────
    story.append(Paragraph("3.  Frequently Asked Questions", H1_S))
    story.append(hr())
    story.append(Paragraph(
        "The following Q&As are sourced directly from digiminds.org/faq/ with no additions "
        "or modifications to the factual claims.",
        s("note2", fontSize=10, textColor=DGREY, spaceAfter=12)
    ))

    for i, (q, a_lines) in enumerate(FAQS, 1):
        for flowable in qa_block(i, q, a_lines):
            story.append(flowable)

    # ── SECTION 4: 90-DAY GUARANTEE (detail) ─────────────────────────────────
    story.append(Paragraph("4.  90-Day Performance Guarantee — Full Terms", H1_S))
    story.append(hr())
    story.append(Paragraph(GUARANTEE_DETAIL, BODY_S))
    story.append(Spacer(1, 8))

    gtbl = Table([[
        Paragraph("✔  KPIs agreed in writing at kickoff", BODY_S),
        Paragraph("✔  Work free until targets hit OR refund", BODY_S),
    ],[
        Paragraph("✔  3-month initial term, then month-to-month", BODY_S),
        Paragraph("✔  No auto-renew · No exit fees", BODY_S),
    ]], colWidths=[(PAGE_W-2*M)/2]*2)
    gtbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), HexColor("#EFF3FB")),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("GRID",          (0,0),(-1,-1), 0.5, MGREY),
    ]))
    story.append(gtbl)
    story.append(Spacer(1, 20))

    # ── SECTION 5: HOW TO ENGAGE ─────────────────────────────────────────────
    story.append(Paragraph("5.  How to Engage", H1_S))
    story.append(hr())

    steps = [
        ("Step 1 — Book Discovery Call",
         "30-minute free call via calendly.com/digimindsltd/30min. No pitch — DigiMinds "
         "qualifies fit honestly and will tell you if you're not ready for a retainer yet."),
        ("Step 2 — Free Audit",
         "DigiMinds runs a free 10-minute audit of your current ad accounts, tracking, "
         "and funnel. Identifies $3–8k/month of typical waste even if you never hire them."),
        ("Step 3 — Custom Proposal",
         "Custom-scoped proposal (no Silver/Gold/Platinum packages). Includes KPIs, "
         "deliverables, timeline, and guarantee terms in writing."),
        ("Step 4 — Kickoff",
         "60-minute kickoff call across week 1. After that, monthly strategy approvals and "
         "weekly Loom video updates — most founders spend 30 minutes/week."),
    ]
    for title, desc in steps:
        story.append(Paragraph(title, H2_S))
        story.append(Paragraph(desc, BODY_S))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 16))

    # Final CTA strip
    final = Table([[Paragraph(
        "Ready to talk?  Call or WhatsApp <b>+92 371 4232502</b>  "
        "or email <b>hello@digiminds.org</b>",
        s("final", fontName="Helvetica", fontSize=11,
          textColor=white, alignment=TA_CENTER)
    )]], colWidths=[PAGE_W - 2*M])
    final.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 14),
        ("BOTTOMPADDING", (0,0),(-1,-1), 14),
    ]))
    story.append(final)

    doc.build(story)
    print(f"✓  Written: {OUT}")

if __name__ == "__main__":
    build()
