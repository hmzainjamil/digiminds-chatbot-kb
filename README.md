# digiminds-chatbot-kb
DigiMinds AI chatbot knowledge base — agency services, pricing, FAQs, lead qualification flows

![Knowledge Base](https://img.shields.io/badge/KB-Chatbot-blue?style=flat&labelColor=555)
![DigiMinds](https://img.shields.io/badge/DigiMinds-Agency-black?style=flat&labelColor=555)
![Claude](https://img.shields.io/badge/Claude-Powered-cc785c?style=flat&labelColor=555)
![Lead Gen](https://img.shields.io/badge/Goal-Lead_Qualification-green?style=flat&labelColor=555)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat&labelColor=555)

[Concepts](#-concepts) · [How It Works](#️-how-it-works) · [Install](#-install) · [KB Structure](#-knowledge-base-structure) · [Tips](#-tips-and-tricks-10) · [Startups](#️-startups--businesses)

---

## 🧠 CONCEPTS

| Feature | Location | Description |
|---------|----------|-------------|
| [**Service KB**](kb/services/) | `kb/services/` | Google Ads, Meta Ads, SEO, website services with pricing |
| [**FAQ Database**](kb/faqs/) | `kb/faqs/` | 150+ Q&A pairs covering objections, process, results |
| [**Lead Qual Flow**](flows/) | `flows/qualification.json` | Decision tree: budget → service fit → handoff to HMZ |
| [**Pricing Logic**](kb/pricing/) | `kb/pricing/` | Tiered pricing rules — chatbot quotes based on scope |
| [**Objection Handlers**](kb/objections/) | `kb/objections/` | Price, trust, timing objections with response templates |
| [**Handoff Protocol**](flows/) | `flows/handoff.json` | Qualified lead → calendar link → HMZ notification |

### 🔥 Hot

| Feature | Location | Description |
|---------|----------|-------------|
| [**Auto-qualification**](flows/qualification.json) | `flows/` | 5-question flow scores lead 0-10 → routes to right service |
| [**Live pricing**](kb/pricing/) | `kb/pricing/` | Chatbot quotes real price ranges without HMZ involvement |
| [**Objection KB**](kb/objections/) | 150+ handlers | Never lose a lead to "too expensive" or "need to think" |

---

## ⚙️ HOW IT WORKS

```
Visitor lands on digiminds.org
         ↓
Chatbot greeting: "What's your #1 marketing challenge?"
         ↓
Qualification flow (5 questions):
  1. Monthly ad budget?
  2. Current channels?
  3. Main goal? (leads/sales/brand)
  4. Timeline?
  5. Team size?
         ↓
Score 0-10 → Route:
  8-10: Hot lead → instant calendar link + HMZ notification
  5-7:  Warm lead → service recommendation + follow-up sequence
  0-4:  Nurture → content offer + email sequence
```

---

## 🚀 INSTALL

```bash
git clone https://github.com/hmzainjamil/digiminds-chatbot-kb
cd digiminds-chatbot-kb
pip install anthropic fastapi uvicorn
# Wire to website: add chatbot widget script
python3 server.py
# API: POST /chat {"message": "...", "session_id": "..."}
```

---

## 📚 KNOWLEDGE BASE STRUCTURE

| Section | Files | Content |
|---|---|---|
| Services | `kb/services/*.md` | Google Ads, Meta Ads, SEO, Web, UGC |
| Pricing | `kb/pricing/*.json` | Starter/Growth/Premium tiers per service |
| FAQs | `kb/faqs/*.json` | 150+ Q&A pairs |
| Objections | `kb/objections/*.json` | Price, trust, timing, competitor |
| Case Studies | `kb/cases/*.md` | DigiMinds client results (anonymized) |
| Handoff | `flows/handoff.json` | Calendar links, notification rules |

---

## 💡 TIPS AND TRICKS (10)

[qualification](#tips-qualification) · [kb](#tips-kb) · [objections](#tips-objections) · [handoff](#tips-handoff)

<a id="tips-qualification"></a>■ **Qualification (3)**

| Tip | Source |
|-----|--------|
| Budget question first — disqualify <$500/mo immediately, don't waste bot on them | [HMZ](https://github.com/hmzainjamil) |
| "What's your #1 challenge?" opener beats "How can I help?" — 3x more responses | [DigiMinds](https://github.com/hmzainjamil) |
| Score 8+ = call within 5min rule — hot leads go cold in 30min | [HMZ](https://github.com/hmzainjamil) |

<a id="tips-kb"></a>■ **Knowledge Base (3)**

| Tip | Source |
|-----|--------|
| Update pricing KB monthly — outdated quotes = trust damage | [HMZ](https://github.com/hmzainjamil) |
| Add competitor comparison docs — "vs Agency X" pages convert well | [DigiMinds](https://github.com/hmzainjamil) |
| Case study KB: format as problem → solution → result → client quote | [HMZ](https://github.com/hmzainjamil) |

<a id="tips-objections"></a>■ **Objections (2)**

| Tip | Source |
|-----|--------|
| Price objection: "Our minimum is $X because [specific reason]" — justify, don't discount | [HMZ](https://github.com/hmzainjamil) |
| "Need to think": offer a free audit instead — converts 40% of thinking-leads | [DigiMinds](https://github.com/hmzainjamil) |

<a id="tips-handoff"></a>■ **Handoff (2)**

| Tip | Source |
|-----|--------|
| Calendar link in chat, not email — every extra step loses 30% of leads | [HMZ](https://github.com/hmzainjamil) |
| Notify via WhatsApp + email — WhatsApp notification = 95% open rate | [DigiMinds](https://github.com/hmzainjamil) |

---

## ☠️ STARTUPS / BUSINESSES

| This Repo / Feature | Replaced |
|-|-|
| **Chatbot KB system** | [Intercom](https://intercom.com), [Drift](https://drift.com), [Tidio](https://tidio.com) — $100-500/mo |
| **Lead qualification flow** | [Typeform](https://typeform.com), [Jotform](https://jotform.com) — separate tool |
| **Objection handlers** | Sales coaching sessions — documented here |
| **Pricing logic** | Sales rep pricing calls — automated |

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hmzainjamil/digiminds-chatbot-kb&type=Date)](https://star-history.com/#hmzainjamil/digiminds-chatbot-kb&Date)

---

<div align="center">
Built by <a href="https://github.com/hmzainjamil">HMZ</a> · <a href="https://digiminds.org">DigiMinds</a> · Zero-human lead qualification
</div>
