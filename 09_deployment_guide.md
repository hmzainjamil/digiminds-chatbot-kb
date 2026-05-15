# DigiMinds Chatbot — Deployment Guide

How to ship this KB into a working chatbot on digiminds.org. Three deployment paths ranked by speed-to-live.

---

## PATH 1 — FAST DEPLOY (GoHighLevel + OpenAI) — 2-4 days

Best if DigiMinds already uses GoHighLevel internally (likely, given stack).

### Stack
- **LLM:** GPT-4o (primary) or Claude Sonnet 4.6 fallback
- **Chat widget:** GoHighLevel web chat + conversation AI
- **KB storage:** GHL workflows + vector DB (Pinecone or Supabase pgvector)
- **Calendar:** GHL appointments / Cal.com
- **CRM:** GoHighLevel pipelines
- **WhatsApp:** GHL + Twilio WhatsApp Business API

### Steps
1. **Create GHL sub-account** for digiminds.org chatbot.
2. **Embed KB in vector store**
   - Chunk `03_knowledge_base.json` entries as individual docs
   - Embed `question_variants` + `answer` with OpenAI text-embedding-3-small
   - Store: content, segment_tags, geo_tags, category, micro_action
3. **Paste system prompt from `00_system_prompt.md`** into GHL Conversation AI bot.
4. **Configure retrieval**: top-k=5, cosine threshold 0.7.
5. **Build GHL workflow** for each tier of micro-action:
   - Tier 1 call booking → send Cal.com link + create opportunity in "Discovery Call Booked" pipeline stage
   - Tier 2 form → capture in "Qualified Lead" stage + send internal Slack alert
   - Tier 3 email → add to "Nurture" tag + trigger 5-email drip
6. **WhatsApp integration**: for PK/UAE segments, trigger Twilio WA template after chat ends.
7. **Escalation webhook**: on handoff trigger, Slack alert #sales channel with full context.
8. **Deploy widget** on digiminds.org via script tag.

### Cost estimate
- GPT-4o: ~$0.005/session average = $50/mo per 10k sessions
- GHL: existing subscription
- Pinecone: free tier sufficient at launch
- Twilio WA: ~$0.005/message

---

## PATH 2 — PRODUCTION-GRADE (Custom Stack) — 2-3 weeks

Best for long-term flexibility and lower per-conversation cost at scale.

### Stack
- **LLM orchestration:** LangChain or LlamaIndex
- **LLM providers:** OpenAI GPT-4o (primary), Claude Sonnet (fallback), Gemini Flash (high volume)
- **Model routing:** Cheap model (Gemini Flash / GPT-4o-mini) for turns 1-2 classification, upgrade to GPT-4o only for complex turns — saves 60-80% cost
- **Vector DB:** Pinecone, Qdrant, or Weaviate
- **Chat widget:** Custom React + WebSocket OR Intercom/Drift with custom webhook
- **Backend:** Node.js/Express or Python/FastAPI
- **Session store:** Redis
- **CRM sync:** GoHighLevel API + webhook
- **Analytics:** PostHog or Mixpanel for chat funnel analytics
- **Voice:** ElevenLabs for future WhatsApp voice note support

### Model routing logic (critical for cost)
```
turn 1-2 classification → gemini-flash or gpt-4o-mini ($0.0001/turn)
turn 3+ (KB retrieval + answer) → gpt-4o ($0.003/turn)
de-escalation / ethics handling → gpt-4o (quality matters)
objection handling → claude sonnet (nuance matters)
technical deep-dive → gpt-4o with function calling
```

### Steps
1. Build retrieval API (`/retrieve?query=...`) on top of vector DB.
2. Build orchestration layer handling state machine from `08_conversion_engine.md`.
3. Build widget (or integrate with existing Intercom/Drift).
4. Build GHL sync (pipeline stage updates + contact creation).
5. Build analytics dashboard for the KPIs in `08_conversion_engine.md`.
6. A/B testing framework (LaunchDarkly or homebrew).
7. Load-test to 1000 concurrent sessions.
8. Ship.

---

## PATH 3 — ULTRA-FAST PROTOTYPE (Drift/Intercom + OpenAI Assistants) — 1 day

Quickest way to test the KB conceptually.

### Stack
- **OpenAI Assistants API** with Knowledge tool
- **Drift, Intercom, or Tawk.to** chat widget
- Direct OpenAI call on every message, no custom routing

### Steps
1. Create OpenAI Assistant with `00_system_prompt.md` as instructions.
2. Upload all JSON + MD files to the Assistant's file store.
3. Enable retrieval on files.
4. Wire Drift/Intercom to Assistants API via webhook.
5. Deploy.

**Tradeoff:** No segment detection, no state machine, no micro-action upgrade logic — but directionally correct and fast to test. Use for <500 sessions/month before graduating to Path 1 or 2.

---

## TRACKING & ANALYTICS SETUP

Fire these events to GA4 + PostHog:
- `chat_opened`
- `chat_first_message_sent`
- `chat_segment_detected` (with segment_id)
- `chat_objection_surfaced` (with objection_id)
- `chat_micro_action_offered` (with tier, type)
- `chat_micro_action_accepted`
- `chat_call_booked`
- `chat_form_submitted`
- `chat_email_captured`
- `chat_whatsapp_handoff`
- `chat_human_escalation` (with reason)
- `chat_session_ended` (with outcome, turn_count, trust_score)

Build Looker Studio / Metabase dashboard covering:
- Conversion funnel by segment
- Top unresolved questions (LLM couldn't answer well)
- Hostile session patterns for human review
- A/B test lift
- Cost-per-conversation by LLM model

---

## KB MAINTENANCE CADENCE

- **Weekly**: review unresolved questions → add to `03_knowledge_base.json`
- **Weekly**: review hostile sessions → refine `04_ethics_sensitive_playbook.json`
- **Monthly**: refresh competitor matrix + pricing ranges
- **Monthly**: review conversion analytics → A/B test winners become defaults
- **Quarterly**: full KB audit; re-embed with updated content
- **On demand**: update `01_business_profile.json` when DigiMinds ships new services, case studies, pricing, or certifications

---

## SECURITY & PRIVACY

- **PII handling**: emails, phones, names encrypted at rest (AES-256), stored only in GoHighLevel (SOC 2 compliant)
- **Transcripts**: retained 180 days, then anonymized or deleted
- **GDPR/UK GDPR**: consent banner before chat opens for EU/UK visitors; right-to-erasure endpoint
- **PECA 2016**: PK visitor data processed with consent; data center choice (prefer US/EU over offshore)
- **Never log**: credit cards, passwords, API keys (even if pasted by user — regex redact before storage)
- **Rate limiting**: 30 msgs/min/IP to block spam
- **Profanity filter**: detection only (don't block — de-escalate per playbook)

---

## LAUNCH CHECKLIST

- [ ] All 10 files in `digiminds-chatbot-kb/` reviewed by founder
- [ ] `01_business_profile.json` verified for accuracy (case studies, pricing, contact)
- [ ] System prompt tested with 20 scripted inputs across all 9 segments
- [ ] Hostile/vulgar inputs tested (full `04_` playbook)
- [ ] Calendar link tested end-to-end (invite, reminder, reschedule)
- [ ] WhatsApp Business green tick verified
- [ ] GHL pipelines created with correct stages
- [ ] Slack alerts configured for handoff triggers
- [ ] GDPR consent banner for EU traffic
- [ ] Fallback to human handoff email tested
- [ ] Analytics events firing correctly
- [ ] Mobile chat UX tested (thumb-friendly, readable)
- [ ] Load tested (100+ concurrent)
- [ ] First 50 real sessions manually reviewed for quality

---

## 30-60-90 DAY POST-LAUNCH PLAN

**Days 0-30**: Ship, monitor daily, fix gaps in KB from real conversations. Goal: baseline funnel working, top 20 unresolved questions added.

**Days 31-60**: A/B test 3 micro-action strategies per segment. Add 100+ entries to KB from real transcripts. Tune trust-score weights.

**Days 61-90**: Optimize cost via model routing (Path 2 migration). Add voice note support for PK WhatsApp. Hit stretch KPIs in `08_conversion_engine.md`.

---

**You're ready to ship. Hand the `digiminds-chatbot-kb/` folder to whoever implements the chatbot — all context, rules, and logic are in these 10 files.**
