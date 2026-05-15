# DigiMinds AI Chatbot — Knowledge Base & Conversion Engine

**Goal:** Convert 99% of chat visitors to a lead, call, or commitment *before they leave*.
**Scope:** digiminds.org — performance agency HQ Lahore, serving PK + US + CA + UK + UAE.
**Services:** SEM/paid media, high-ticket lead gen, DTC ecom growth, data/tracking/CRM (GoHighLevel/GA4/server-side), SEO/AEO.
**Guarantee:** 90-day performance guarantee.

## File Index

| # | File | Purpose |
|---|------|---------|
| 0 | `00_system_prompt.md` | Master system prompt — paste into LLM provider |
| 1 | `01_business_profile.json` | Ground-truth facts about DigiMinds |
| 2 | `02_psychographic_segments.json` | 9 visitor segments × tone × path |
| 3 | `03_knowledge_base.json` | Main Q→A→micro-action KB (indexed, tagged) |
| 4 | `04_ethics_sensitive_playbook.json` | Ethics, vulgar, hostile, abuse handling |
| 5 | `05_competitor_matrix.json` | 25 global + 25 PK competitors + counters |
| 6 | `06_conversation_flows.md` | 12 full sample flows per segment |
| 7 | `07_objection_playbook.json` | 40 objections × preempt + rebuttal + close |
| 8 | `08_conversion_engine.md` | Micro-action logic, escalation, handoff rules |
| 9 | `09_deployment_guide.md` | Integration notes (GHL, Intercom, Drift, etc.) |

## Design Principles

1. **Every turn ends with a micro-action.** No passive replies. Always nudge toward commit (call, form, WhatsApp, offer).
2. **Specificity > generic warmth.** Name the service, the vertical, the number, the next step.
3. **Trust stack in every third message.** Certifications, real clients, guarantee, ownership of data.
4. **Segment detection in first 2 messages.** Route instantly — PK SMB gets different tone than US SaaS founder.
5. **De-escalate hostility once, disengage if persistent.** Never match tone. Log for human.
6. **Human handoff = last resort.** Exhaust self-serve answers first. Capture contact before any handoff.

## Success Metric

Target chat→lead conversion: **25–40%** of qualified sessions (vs industry 5–15%).
Target chat→booked call: **8–15%** of qualified sessions.
Fallback form submission: **45–60%** of sessions that did not escalate to call.
