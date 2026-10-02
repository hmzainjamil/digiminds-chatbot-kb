# DigiMinds Chatbot Knowledge Base

Static content for a proposed DigiMinds website and sales assistant. The repository contains prompt and conversation guidance, JSON knowledge files, and generated PDF exports. It contains no chatbot application, retrieval service, vector database, live integrations, or deployment configuration.

| Status | Evidence |
|---|---|
| Source reviewed | 2026-10-02; full recursive tree and principal content files |
| Runtime | None included |
| Content validation | Not evidenced; business, client, competitor, performance, guarantee, and compliance claims require owner review |
| Privacy review | Required before external model or chatbot use |
| Tests and evaluation | No tests, evaluation set, or results included |
| License | No license file or declared license identified |

## Repository map

- `00_system_prompt.md`: assistant behavior guidance. It now requires disclosure, consent, and source-backed claims.
- `01_business_profile.json`: business profile and service descriptions.
- `02_psychographic_segments.json`: audience-segment guidance.
- `03_knowledge_base.json`: question and answer content.
- `04_ethics_sensitive_playbook.json`: sensitive-topic guidance.
- `05_competitor_matrix.json`: competitor comparison content.
- `06_conversation_flows.md` and `07_objection_playbook.json`: conversation and objection guidance.
- `08_conversion_engine.md`: proposed conversion logic.
- `09_deployment_guide.md`: unverified deployment proposal, not an install procedure.
- `build_pdf.py`, `build_faq_pdf.py`, `build_faq_v2_pdf.py`: PDF generation scripts.
- Three PDFs: generated content snapshots. Their contents and consistency with source files require review.

## Review before use

Treat all claims about customers, results, guarantees, certifications, partners, prices, competitors, and legal or compliance status as unverified until an accountable owner provides current evidence. The repository includes contact and business profile details; classify and approve these before sending content to an external model or publishing a chatbot.

The system prompt must not pressure visitors or invent proof, availability, pricing, results, or credentials. Collect only information needed for a visitor-requested next step, and obtain consent before storing or forwarding contact details.

See [content review](CONTENT_REVIEW.md), [security and privacy](SECURITY.md), and the [deployment proposal status](09_deployment_guide.md).

## Use boundary

These files are content inputs, not a functioning chatbot. No provider call, website deployment, lead capture, CRM write, booking, WhatsApp message, or other external action is implemented or verified in this repository. No generated PDF was rebuilt or visually checked in this review.

## Maintainer

[hmzainjamil](https://github.com/hmzainjamil)
