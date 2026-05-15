#!/usr/bin/env python3
"""
DigiMinds FAQ Knowledge Base — MS Word-style PDF
Content sourced 100% verbatim from digiminds.org. No estimations, no invented content.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable, ListFlowable, ListItem
)

OUT_PDF = "/Users/mc/digiminds-chatbot-kb/DigiMinds_FAQ_Knowledge_Base.pdf"

# ---------- MS Word-like palette (subtle, professional) ----------
DOC_ACCENT   = HexColor("#1F3864")   # Word default dark blue
DOC_SUBTLE   = HexColor("#404040")   # body text
DOC_MUTED    = HexColor("#6B6B6B")   # captions / footer
DOC_RULE     = HexColor("#BFBFBF")   # rules
DOC_Q_BG     = HexColor("#F2F2F2")   # very light grey for Q callout

# ---------- Page setup (US Letter, 1" margins = Word default) ----------
PAGE_W, PAGE_H = LETTER
M = 1 * inch

# ---------- Paragraph styles (Word-like) ----------
# Helvetica = Arial equivalent, Times-Roman = Times New Roman equivalent
# Using Helvetica throughout for a clean "Calibri" feel
TITLE = ParagraphStyle(
    'Title', fontName='Helvetica-Bold', fontSize=26, leading=32,
    textColor=DOC_ACCENT, alignment=TA_LEFT, spaceAfter=6
)
SUBTITLE = ParagraphStyle(
    'SubT', fontName='Helvetica', fontSize=13, leading=18,
    textColor=DOC_MUTED, alignment=TA_LEFT, spaceAfter=14
)
H1 = ParagraphStyle(
    'H1', fontName='Helvetica-Bold', fontSize=18, leading=24,
    textColor=DOC_ACCENT, alignment=TA_LEFT, spaceBefore=18, spaceAfter=8
)
H2 = ParagraphStyle(
    'H2', fontName='Helvetica-Bold', fontSize=13, leading=18,
    textColor=DOC_ACCENT, alignment=TA_LEFT, spaceBefore=14, spaceAfter=4
)
BODY = ParagraphStyle(
    'Body', fontName='Helvetica', fontSize=11, leading=16,
    textColor=DOC_SUBTLE, alignment=TA_JUSTIFY, spaceAfter=6
)
BODY_LEFT = ParagraphStyle(
    'BodyL', parent=BODY, alignment=TA_LEFT
)
Q_STYLE = ParagraphStyle(
    'Q', fontName='Helvetica-Bold', fontSize=11.5, leading=16,
    textColor=DOC_ACCENT, alignment=TA_LEFT, spaceBefore=6, spaceAfter=6
)
A_STYLE = ParagraphStyle(
    'A', fontName='Helvetica', fontSize=11, leading=16,
    textColor=DOC_SUBTLE, alignment=TA_JUSTIFY, spaceAfter=4,
    leftIndent=12
)
CAPTION = ParagraphStyle(
    'Cap', fontName='Helvetica-Oblique', fontSize=9, leading=12,
    textColor=DOC_MUTED, alignment=TA_LEFT, spaceAfter=4
)
TOC_ENTRY = ParagraphStyle(
    'TOC', fontName='Helvetica', fontSize=11, leading=18,
    textColor=DOC_SUBTLE, alignment=TA_LEFT, spaceAfter=3
)

story = []

def header_footer(canv, doc):
    canv.saveState()
    # Minimal Word-style: subtle top line, simple footer
    canv.setStrokeColor(DOC_RULE)
    canv.setLineWidth(0.5)
    # Header rule
    canv.line(M, PAGE_H - 0.6 * inch, PAGE_W - M, PAGE_H - 0.6 * inch)
    canv.setFont("Helvetica", 9)
    canv.setFillColor(DOC_MUTED)
    canv.drawString(M, PAGE_H - 0.5 * inch, "DigiMinds  |  Frequently Asked Questions")
    canv.drawRightString(PAGE_W - M, PAGE_H - 0.5 * inch, "digiminds.org")
    # Footer rule
    canv.line(M, 0.6 * inch, PAGE_W - M, 0.6 * inch)
    canv.setFillColor(DOC_MUTED)
    canv.drawString(M, 0.45 * inch, f"© {datetime.now().year} DigiMinds. All Rights Reserved.")
    canv.drawRightString(PAGE_W - M, 0.45 * inch, f"Page {doc.page}")
    canv.restoreState()

def cover_page(canv, doc):
    canv.saveState()
    # Thin top accent bar (Word report template style)
    canv.setFillColor(DOC_ACCENT)
    canv.rect(0, PAGE_H - 0.35 * inch, PAGE_W, 0.08 * inch, fill=1, stroke=0)
    # Footer
    canv.setFillColor(DOC_MUTED)
    canv.setFont("Helvetica", 9)
    canv.drawCentredString(PAGE_W / 2, 0.55 * inch, f"© {datetime.now().year} DigiMinds  ·  digiminds.org  ·  info@digiminds.org  ·  +92 371 4232502")
    canv.restoreState()

def h1(t): story.append(Paragraph(t, H1))
def h2(t): story.append(Paragraph(t, H2))
def body(t): story.append(Paragraph(t, BODY))
def body_left(t): story.append(Paragraph(t, BODY_LEFT))

def qa_block(num, q, a_paragraphs):
    """Render a Q/A in Word-FAQ style: Q# in box, answer indented below."""
    # Q row as a subtle grey cell
    q_cell = Paragraph(f'<font color="{DOC_ACCENT.hexval()}"><b>Q{num}.</b></font>&nbsp;&nbsp;<b>{q}</b>', Q_STYLE)
    tbl = Table([[q_cell]], colWidths=[PAGE_W - 2*M])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DOC_Q_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (0,0), (0,-1), 3, DOC_ACCENT),
    ]))
    block = [tbl, Spacer(1, 6)]
    # A paragraphs
    for idx, p in enumerate(a_paragraphs):
        prefix = f'<font color="{DOC_ACCENT.hexval()}"><b>A.</b></font>&nbsp;&nbsp;' if idx == 0 else ''
        block.append(Paragraph(prefix + p, A_STYLE))
    block.append(Spacer(1, 10))
    story.append(KeepTogether(block))

def hr():
    story.append(HRFlowable(width="100%", thickness=0.5, color=DOC_RULE, spaceBefore=6, spaceAfter=6))

# =================================================================
# COVER / TITLE PAGE
# =================================================================
story.append(Spacer(1, 1.4 * inch))
story.append(Paragraph("FAQ Knowledge Base", TITLE))
story.append(Paragraph("Frequently Asked Questions &mdash; Reference Document", SUBTITLE))
hr()
story.append(Spacer(1, 0.15 * inch))

# Meta info (Word-document style)
meta_rows = [
    ["Document title", "DigiMinds — FAQ Knowledge Base"],
    ["Prepared for", "DigiMinds (digiminds.org)"],
    ["Source", "digiminds.org/faq/ — verbatim content"],
    ["Document date", datetime.now().strftime("%d %B %Y")],
    ["Version", "1.0"],
    ["Pages", "Generated automatically"],
]
mt = Table(meta_rows, colWidths=[1.6 * inch, 4.6 * inch])
mt.setStyle(TableStyle([
    ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 10),
    ('FONT', (1,0), (1,-1), 'Helvetica', 10),
    ('TEXTCOLOR', (0,0), (0,-1), DOC_MUTED),
    ('TEXTCOLOR', (1,0), (1,-1), DOC_SUBTLE),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LINEBELOW', (0,0), (-1,-1), 0.25, DOC_RULE),
]))
story.append(mt)

story.append(Spacer(1, 0.4 * inch))

# Company identity block
story.append(Paragraph("About this document", H2))
body(
    "This document compiles the Frequently Asked Questions published on <b>digiminds.org/faq/</b> "
    "into a single reference-ready format suitable for internal training, client onboarding, sales "
    "support, and chatbot knowledge-base ingestion. All questions and answers are reproduced "
    "verbatim from the DigiMinds website. No content has been added, paraphrased, or inferred."
)

# =================================================================
# TABLE OF CONTENTS
# =================================================================
story.append(PageBreak())
story.append(Paragraph("Contents", H1))
toc_entries = [
    ("1", "Company Overview", "Verified facts from digiminds.org"),
    ("2", "Services & Scope", "3 FAQs"),
    ("3", "Ecommerce & Scaling", "3 FAQs"),
    ("4", "Lead Generation, Tracking & Data", "2 FAQs"),
    ("5", "Process & The Audit", "1 FAQ"),
    ("6", "Free Profit Audit — What's Included", "Verbatim from site"),
    ("7", "Contact & Booking", "Channels and hours from site"),
]
for num, t, d in toc_entries:
    row = [[
        Paragraph(f'<font color="{DOC_ACCENT.hexval()}"><b>{num}</b></font>', TOC_ENTRY),
        Paragraph(f'<b>{t}</b>', TOC_ENTRY),
        Paragraph(f'<font color="{DOC_MUTED.hexval()}">{d}</font>', TOC_ENTRY),
    ]]
    tt = Table(row, colWidths=[0.4*inch, 2.5*inch, 3.6*inch])
    tt.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, DOC_RULE),
    ]))
    story.append(tt)

# =================================================================
# SECTION 1 — COMPANY OVERVIEW (verbatim facts only)
# =================================================================
story.append(PageBreak())
h1("1. Company Overview")
body_left("<i>The facts on this page are taken directly from digiminds.org. No estimates or inferred details are included.</i>")
story.append(Spacer(1, 8))

h2("Company Description")
body(
    "DigiMinds describes itself as: &ldquo;a globally operating performance agency and Fractional CMO "
    "partner. We don&rsquo;t just run ads; we build the underlying data, tracking, and CRM architecture.&rdquo;"
)

h2("Tagline")
body("&ldquo;Zero fluff. Pure ROI. Performance-backed, 90-day guarantee.&rdquo;")

h2("Footer Description")
body(
    "&ldquo;Global performance marketing agency specialized in high-growth e-commerce scaling "
    "and high-ticket lead generation systems.&rdquo;"
)

h2("Services Listed on Site")
overview_services = [
    "DTC Ecommerce Growth",
    "High-Ticket B2B/B2C",
    "CRM Automation &amp; GoHighLevel",
    "SEO &amp; (AEO)",
    "Data Analytics &amp; Server-Side Tracking",
    "SEM &amp; Paid Advertising",
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, BODY_LEFT), leftIndent=12, bulletColor=DOC_ACCENT) for s in overview_services],
    bulletType='bullet', start='•', leftIndent=20, bulletFontSize=10, bulletColor=DOC_ACCENT
))

h2("Headquarters")
body(
    "Ansari Market, Unit #05, Rehman Street, Brandreth Road, Lahore 54010, Punjab, Pakistan."
)

h2("Disclosure Statement")
body("&ldquo;Not affiliated with Meta, Google, or TikTok.&rdquo;")

# =================================================================
# SECTION 2 — SERVICES & SCOPE (Q1-Q3)
# =================================================================
story.append(PageBreak())
h1("2. Services &amp; Scope")
body_left("<i>Page introduction from digiminds.org/faq:</i> &ldquo;Clear answers on how DigiMinds scales revenue through precision performance marketing, CRM integration, and data-driven strategy.&rdquo;")
story.append(Spacer(1, 10))

qa_block(1,
    "What exactly does DigiMinds do as a digital marketing agency?",
    [
        "We engineer closed-loop revenue systems. Instead of just running ads and reporting on "
        "superficial clicks, we integrate advanced performance marketing with CRM automation. "
        "Our goal is to track every marketing dollar from the initial impression directly to "
        "closed-won revenue, ultimately lowering your Customer Acquisition Cost (CAC) and "
        "scaling predictable pipeline growth."
    ]
)

qa_block(2,
    "Why should I hire a Fractional CMO instead of an in-house marketer?",
    [
        "A Fractional CMO provides you with executive-level strategic direction without the "
        "overhead of a full-time C-suite salary. You gain access to seasoned leadership that "
        "builds your overarching growth architecture, manages specialized execution teams, and "
        "aligns your marketing efforts directly with your financial targets."
    ]
)

qa_block(3,
    "Do you build websites and landing pages?",
    [
        "Yes, but strictly for performance. We design and develop high-converting landing pages "
        "and conversion-rate-optimized (CRO) websites tailored specifically to capture leads, "
        "reduce bounce rates, and drive maximum sales from our advertising campaigns."
    ]
)

# =================================================================
# SECTION 3 — ECOMMERCE & SCALING (Q4-Q6)
# =================================================================
story.append(PageBreak())
h1("3. Ecommerce &amp; Scaling")

qa_block(4,
    "Do you work with dropshipping or only private-label brands?",
    [
        "We specialize in scaling established private-label brands and businesses with secure "
        "supply chains. Our aggressive performance marketing and retention strategies are designed "
        "for brands looking to maximize Customer Lifetime Value (LTV), which requires controlling "
        "product quality and the customer fulfillment experience."
    ]
)

qa_block(5,
    "How do you scale Shopify stores?",
    [
        "We scale Shopify brands by optimizing the entire unit economics equation. This includes "
        "deploying advanced media buying (like PMax and Advantage+), implementing dynamic "
        "retargeting, improving Average Order Value (AOV) through backend CRO, and building robust "
        "email and SMS retention funnels to drive repeat purchases."
    ]
)

qa_block(6,
    "Do you manage Performance Max and Advantage+ campaigns?",
    [
        "Absolutely. We heavily leverage AI-driven campaign types like Google&rsquo;s Performance Max "
        "(PMax) and Meta&rsquo;s Advantage+ Shopping. However, because these algorithms rely heavily "
        "on data, our true edge lies in feeding them superior creative assets and flawless "
        "server-side conversion data so they are forced to find your highest-value buyers."
    ]
)

# =================================================================
# SECTION 4 — LEAD GENERATION, TRACKING & DATA (Q7-Q8)
# =================================================================
story.append(PageBreak())
h1("4. Lead Generation, Tracking &amp; Data")

qa_block(7,
    "Do you do lead generation for service businesses?",
    [
        "Yes. We build end-to-end lead generation engines for B2B and high-ticket B2C service "
        "businesses. We don&rsquo;t just generate form fills; we integrate directly with your CRM "
        "(HubSpot, Salesforce, Zoho, etc.) to score, route, and track leads through to the final "
        "sale, ensuring zero pipeline leakage."
    ]
)

qa_block(8,
    "How do you track WhatsApp and COD (Cash on Delivery) sales for Pakistani and GCC ecommerce stores?",
    [
        "Tracking offline or chat-based conversions is a major challenge in the GCC and APAC "
        "regions. We solve this by implementing custom server-side tracking (CAPI) and advanced "
        "CRM integrations. We push finalized WhatsApp lead data and verified COD order statuses "
        "back into Google and Meta. This trains the ad algorithms to optimize for actual revenue, "
        "not just preliminary messages or unverified, returned orders."
    ]
)

# =================================================================
# SECTION 5 — PROCESS & THE AUDIT (Q9)
# =================================================================
story.append(PageBreak())
h1("5. Process &amp; The Audit")

qa_block(9,
    "What is included in the free DigiMinds digital marketing audit?",
    [
        "Our audit isn&rsquo;t an automated PDF; it&rsquo;s a manual, executive-level teardown of your "
        "current growth architecture. When you book an audit, you receive:",
        "<b>Full Funnel Deep Dive:</b> We identify the exact leaks in your current ad-to-CRM pipeline.",
        "<b>Creative Gap Analysis:</b> We review your current ad creatives and messaging against "
        "top-performing industry benchmarks.",
        "<b>Custom 60-90 Days Roadmap:</b> We provide a strategic blueprint detailing exactly how we "
        "will scale your revenue and drop your CAC."
    ]
)

# =================================================================
# SECTION 6 — FREE PROFIT AUDIT (verbatim from site)
# =================================================================
story.append(PageBreak())
h1("6. Free Profit Audit — What&rsquo;s Included")
body_left("<i>The following is reproduced verbatim from digiminds.org:</i>")
story.append(Spacer(1, 6))

body("<b>Stop Funding Ad Algorithms. Start Scaling.</b>")
body(
    "&ldquo;Schedule your free 30-minute Profit Audit. We&rsquo;ll show you exactly where your budget "
    "leaks are &mdash; and plug them with a proven system.&rdquo;"
)
story.append(Spacer(1, 4))

h2("The Three Deliverables")
deliverables = [
    "<b>Full Funnel Deep Dive</b>",
    "<b>Creative Gap Analysis</b>",
    "<b>Custom 90-Day Roadmap</b>",
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, BODY_LEFT), leftIndent=12, bulletColor=DOC_ACCENT) for s in deliverables],
    bulletType='bullet', start='•', leftIndent=20, bulletFontSize=10, bulletColor=DOC_ACCENT
))

h2("How to Book")
body(
    "Booking the free audit is done via Calendly at "
    "<b>calendly.com/digimindsltd/30min</b>, via the &ldquo;Book a free audit&rdquo; button on the site, "
    "or via direct WhatsApp message to the number listed below."
)

# =================================================================
# SECTION 7 — CONTACT & BOOKING
# =================================================================
story.append(PageBreak())
h1("7. Contact &amp; Booking")
body_left("<i>All contact details are published on digiminds.org.</i>")
story.append(Spacer(1, 10))

contact_rows = [
    ["Channel", "Detail"],
    ["Website", "digiminds.org"],
    ["Email", "info@digiminds.org"],
    ["Phone", "+92 371 4232502"],
    ["WhatsApp", "+92 371 4232502"],
    ["Calendly (free audit)", "calendly.com/digimindsltd/30min"],
    ["Headquarters", "Ansari Market, Unit #05, Rehman Street, Brandreth Road, Lahore 54010, Punjab, Pakistan"],
    ["Social — Facebook", "Listed on site"],
    ["Social — LinkedIn", "Listed on site"],
    ["Social — Instagram", "Listed on site"],
]
ct = Table(contact_rows, colWidths=[1.8*inch, 4.4*inch], repeatRows=1)
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DOC_ACCENT),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 10),
    ('FONT', (0,1), (-1,-1), 'Helvetica', 10),
    ('TEXTCOLOR', (0,1), (-1,-1), DOC_SUBTLE),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LINEBELOW', (0,0), (-1,-1), 0.25, DOC_RULE),
]))
story.append(ct)

h2("Related Pages on digiminds.org")
related = [
    "Home", "About Us", "Services", "DTC Ecommerce Growth", "High-Ticket B2B/B2C",
    "CRM Automation &amp; GoHighLevel", "SEO &amp; (AEO)", "Data Analytics &amp; Server-Side Tracking",
    "SEM &amp; Paid Advertising", "Careers &amp; Talent", "Portfolio", "Testimonials",
    "B2B/B2C Partnerships", "FAQ", "Case Studies", "Contact Us",
    "Terms &amp; Conditions", "Privacy Policy"
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, BODY_LEFT), leftIndent=12, bulletColor=DOC_ACCENT) for s in related],
    bulletType='bullet', start='•', leftIndent=20, bulletFontSize=10, bulletColor=DOC_ACCENT
))

# =================================================================
# END NOTE
# =================================================================
story.append(PageBreak())
h1("Source Notes")
body(
    "Every question and answer in this document is reproduced verbatim from the FAQ section "
    "published at <b>digiminds.org/faq/</b>. Contact details, service names, the tagline, and "
    "the audit deliverables were gathered directly from the corresponding pages on the DigiMinds "
    "website. No statistics, client names, pricing figures, case-study numbers, or interpretive "
    "commentary have been added."
)
body(
    "For any content that does not appear in this document — including pricing, case study "
    "outcomes, team biographies, awards, certifications, testimonials, or portfolio items — "
    "please refer directly to the relevant page on digiminds.org, as that information was not "
    "published on the FAQ or contact pages at the time of capture."
)

story.append(Spacer(1, 0.4 * inch))
story.append(HRFlowable(width="100%", thickness=1, color=DOC_ACCENT))
story.append(Spacer(1, 0.15 * inch))
body_left(
    f'<font color="{DOC_MUTED.hexval()}" size="9">Document prepared {datetime.now().strftime("%d %B %Y")} &middot; Version 1.0</font>'
)
body_left(
    f'<b>DIGIMINDS</b>  &middot;  Ansari Market, Unit #05, Rehman Street, Brandreth Road, Lahore 54010, Punjab &middot; digiminds.org &middot; info@digiminds.org &middot; +92 371 4232502'
)

# =================================================================
# DOC TEMPLATE
# =================================================================
class FAQDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=LETTER,
                         leftMargin=M, rightMargin=M,
                         topMargin=M, bottomMargin=M,
                         title="DigiMinds — FAQ Knowledge Base",
                         author="DigiMinds",
                         subject="FAQ Reference Document (Source: digiminds.org/faq)",
                         creator="DigiMinds")
        frame = Frame(M, M, PAGE_W - 2*M, PAGE_H - 2*M, id='body',
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[frame], onPage=cover_page),
            PageTemplate(id='content', frames=[frame], onPage=header_footer),
        ])
    def afterFlowable(self, flowable):
        pass

# Apply content template after cover
from reportlab.platypus import NextPageTemplate
# We need to switch template at the first PageBreak — add the NextPageTemplate before first break
# Easiest: insert into story after the cover content before the first PageBreak
# Find first PageBreak index
for i, f in enumerate(story):
    if isinstance(f, PageBreak):
        story.insert(i, NextPageTemplate('content'))
        break

def main():
    doc = FAQDoc(OUT_PDF)
    doc.build(story)
    size = os.path.getsize(OUT_PDF) / 1024
    print(f"[OK] PDF built: {OUT_PDF} ({size:.1f} KB)")

if __name__ == "__main__":
    main()
