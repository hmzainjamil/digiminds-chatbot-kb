# DigiMinds Chatbot — Conversion Engine

Micro-action logic, escalation rules, human handoff protocols, and KPI tracking. This is the "brain" that turns conversations into measurable conversions.

---

## THE MICRO-ACTION HIERARCHY

Every message ends with ONE micro-action. Rank ordered by value to DigiMinds. Upgrade as trust grows.

### Tier 1 — Highest Value (push when trust is established)
1. **Book discovery call** (Calendly/Cal.com link)
2. **WhatsApp handoff** to senior strategist (PK/UAE)
3. **Sign scoping agreement / send proposal**

### Tier 2 — Qualified Capture
4. **Contact form submission** with: name, email, service, budget, timeline
5. **Free audit request** (URL + email)
6. **Scoping call** with junior (for smaller budgets)

### Tier 3 — Low-Commitment Anchor
7. **Email capture** for case study pack / guarantee PDF / pricing guide
8. **Newsletter subscription** (last resort — still better than bounce)
9. **WhatsApp opt-in** for one-off message

### Tier 4 — Retention (if they decline all above)
10. **Come back soft-close** — "When you're ready, we're here. hello@digiminds.org."

---

## MICRO-ACTION SELECTION LOGIC

```
def pick_micro_action(segment, turn_count, trust_score, objections_unresolved):
  # Turn 1-2 — discovery only, no push
  if turn_count <= 2:
    return tier_3_email_capture  # soft offer

  # Turn 3-4 — first conversion attempt
  if turn_count in [3,4]:
    if segment in [SEG_05, SEG_06, SEG_04]:
      return tier_1_whatsapp_handoff
    elif segment in [SEG_01, SEG_02, SEG_08]:
      return tier_1_book_call
    elif segment == SEG_07:
      return tier_2_proposal_request
    else:
      return tier_2_audit

  # Turn 5-6 — upgrade or downgrade based on response
  if trust_score >= 0.7 and objections_unresolved == 0:
    return tier_1  # push hard
  elif trust_score >= 0.4:
    return tier_2  # audit / form
  else:
    return tier_3  # email capture only

  # Turn 7+ — last-chance soft close
  if turn_count >= 7 and no_action_taken:
    return tier_3_case_study_pack + tier_4_come_back
```

---

## TRUST SCORE CALCULATION

Score 0-1, updated every turn.

| Signal | Weight |
|--------|--------|
| Visitor shared name | +0.1 |
| Visitor shared email | +0.15 |
| Visitor shared phone/WhatsApp | +0.15 |
| Visitor shared company name | +0.1 |
| Visitor shared specific KPIs (ROAS, CAC, revenue) | +0.15 |
| Visitor asked pricing | +0.1 |
| Visitor asked about process/onboarding | +0.15 |
| Visitor asked about guarantee | +0.2 |
| Visitor engaged with proof points | +0.1 |
| Visitor mentioned timeline/urgency | +0.1 |
| Visitor raised an objection | +0.05 (shows engagement, not disengagement) |
| Visitor vulgarity/hostility | -0.3 |
| Visitor ignored 2 micro-actions | -0.2 |
| Session pause >2 min | -0.05 |

**Thresholds:**
- `trust < 0.3` → tier 3 capture only
- `0.3 ≤ trust < 0.7` → tier 2 audit/form
- `trust ≥ 0.7` → tier 1 call/proposal push

---

## ESCALATION RULES (chatbot → human)

Hand off to a human when ANY of these fire:

1. **Custom enterprise pricing** — visitor mentions budget > $15k/mo OR enterprise vertical (Fortune 500, government, regulated industry)
2. **Technical deep-dive beyond KB** — three consecutive tech questions the KB can't answer semantically (cosine < 0.65)
3. **Contract / legal / NDA question** — anything beyond template language
4. **User explicitly asks** — "connect me to a human," "real person," "talk to someone"
5. **Vulgar/hostile — 2nd offense** — log + exit, flag for human follow-up
6. **Crisis signals** — "lawsuit," "FBR," "FIA," "banned account," "urgent" triple-flag
7. **Visitor stuck in loop** — same question asked 3 times with no progress

**Before any handoff:**
- Capture: name, email, WhatsApp, one-line context summary
- Send visitor: "I'm connecting you to [Senior Strategist / Founder / Support]. Expected response time: [SLA]. Meanwhile, here's [guarantee PDF / case study / calendar link] to review."
- Log: full transcript + trust score + segment + unresolved questions

---

## HUMAN HANDOFF SLA TARGETS

| Time of day (PKT) | Handoff SLA | Escalation if breached |
|-------------------|-------------|------------------------|
| 9am–8pm (business) | <30 min | Founder phone |
| 8pm–11pm | <2 hours | On-call strategist WhatsApp |
| 11pm–9am | Next business morning | Auto-send overnight welcome + guarantee PDF |
| PK weekend (Sat-Sun) | Emergency only for existing clients | Others: auto-send case study pack + Monday callback promise |

---

## CONVERSATION STATE MACHINE

```
STATE: OPENING
  ↓ visitor sends message
STATE: DISCOVERY  (turns 1-2)
  Goals: detect segment, lock tone, capture 1 qualifying signal
  Exit: segment locked + at least 1 of [geo/role/service/pain/budget]
  ↓
STATE: EDUCATION + PROOF  (turns 3-4)
  Goals: answer their real question, stack proof, resolve 1 objection
  Exit: 1 proof delivered + 1 objection resolved
  ↓
STATE: CONVERSION ATTEMPT  (turn 5)
  Goals: tier 1 or tier 2 micro-action accepted
  Branch:
    - accepted → CLOSING
    - declined → OBJECTION LOOP
    - silent → SOFT CLOSE
  ↓
STATE: OBJECTION LOOP  (turns 6-7 max)
  Goals: surface real blocker, resolve or downgrade micro-action
  Exit: accept tier 2 or tier 3 OR mark as nurture
  ↓
STATE: CLOSING
  Confirm details, send confirmation, set expectation for next touch
  ↓
STATE: POST-SESSION
  Log full session, update CRM, trigger follow-up sequence
```

---

## SESSION LOGGING SCHEMA

Every session logs to CRM (GoHighLevel pipeline) with:

```json
{
  "session_id": "uuid",
  "started_at": "ISO timestamp",
  "ended_at": "ISO timestamp",
  "turn_count": 8,
  "segment_detected": "SEG_01",
  "geo": "US",
  "language": "en",
  "final_trust_score": 0.78,
  "service_of_interest": ["DTC", "tracking"],
  "budget_hint": "$5-10k/mo",
  "timeline_hint": "30 days",
  "objections_surfaced": ["OBJ_01", "OBJ_03"],
  "objections_resolved": ["OBJ_01"],
  "micro_actions_offered": ["tier_2_audit", "tier_1_book_call"],
  "micro_action_accepted": "tier_1_book_call",
  "contact_captured": { "email": "x@y.com", "name": "...", "phone": null },
  "hostility_flags": 0,
  "ethics_flags": [],
  "handoff_triggered": false,
  "handoff_reason": null,
  "transcript_url": "s3://...",
  "next_step_pipeline_stage": "Discovery Call Booked"
}
```

---

## FOLLOW-UP SEQUENCE (post-session)

Based on final outcome, GoHighLevel auto-fires:

| Outcome | Immediate | 24h | 72h | 7 days | 14 days |
|---------|-----------|-----|-----|--------|---------|
| Booked call | Confirmation + prep doc | — | Reminder | Post-call recap if no-show | — |
| Form submission | Tailored audit / proposal | Follow-up email | WhatsApp (if PK/UAE) | Case study pack | Check-in |
| Email capture only | Case study pack | — | Free audit offer | Objection-specific content | Soft close |
| Hostile/abandoned | None (silent log) | — | — | — | Quarterly re-engagement drip |
| Come-back nurture | Resource pack | — | — | Monthly newsletter | Quarterly check-in |

---

## CHATBOT KPIs — OPTIMIZATION TARGETS

| Metric | Baseline | Target (90 days) | Stretch |
|--------|----------|------------------|---------|
| First-turn retention (visitor sends 2nd msg) | 60% | 75% | 85% |
| Segment detection accuracy by turn 2 | — | 80% | 90% |
| Avg turns per session | 3 | 6 | 8 |
| Micro-action acceptance rate | 15% | 35% | 50% |
| Booked call rate | 3% | 10% | 18% |
| Form submission rate | 8% | 20% | 30% |
| Email capture rate | 25% | 45% | 60% |
| Hostile-session auto-handled | — | 95% | 100% |
| Handoff-to-human rate | — | <15% | <8% |
| Avg response time | <5s | <3s | <2s |

---

## A/B TESTS TO RUN (first 90 days)

1. **Opener formality** — Balanced vs warmer vs sharper
2. **Price reveal** — Give range vs pivot to call
3. **Guarantee placement** — Turn 1 vs turn 3 vs turn 5
4. **Calendar direct vs email-first** — which segments convert better with which
5. **Proof order** — Numbers-first vs story-first vs certification-first
6. **WhatsApp offer** — For US visitors, does it help or hurt?
7. **Urdu-switch aggressiveness** — switch after 1 Urdu word vs 2 vs explicit confirmation
8. **Audit length** — 10-min vs 48-hour deep audit
9. **Decline-to-close** — Hard soft-close at turn 7 vs turn 10
10. **Human handoff threshold** — Aggressive vs conservative triggering

---

## FAIL-SAFE BEHAVIORS

- If LLM returns empty/nonsense → fallback to: "Quick one — want me to connect you directly with our team? Drop your email and I'll make the intro."
- If retrieval returns no match (score < 0.5) → "Good question, let me get the right person on this. Email for a 24-hour response?"
- If session >15 turns with no conversion → soft close + email capture + end gracefully
- If visitor sends image/file → "I can't process that directly — share the details in text, or email to hello@digiminds.org and we'll review it."
- If server error → "One sec — small hiccup. While I reconnect, grab our guarantee PDF: [LINK]."
