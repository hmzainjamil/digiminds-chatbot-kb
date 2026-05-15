# digiminds-chatbot-kb

DigiMinds agency chatbot knowledge base: FAQs, SOPs, service catalog, pricing logic, and objection handling — structured for RAG retrieval.

![Chatbot](https://img.shields.io/badge/Chatbot-RAG-blue?style=flat&labelColor=555) ![Agency](https://img.shields.io/badge/Agency-DigiMinds-green?style=flat&labelColor=555) ![KB](https://img.shields.io/badge/KB-Live-brightgreen?style=flat&labelColor=555) ![License](https://img.shields.io/badge/License-MIT-yellow?style=flat&labelColor=555)

[Concepts](#-concepts) · [How It Works](#-how-it-works) · [Install](#-install) · [Usage](#-usage) · [Config](#-configuration) · [Tips](#-tips-and-tricks-12) · [Troubleshooting](#-troubleshooting) · [Architecture](#-architecture) · [Startups](#️-startups--businesses)

---

## 🧠 CONCEPTS

| Feature | Location | Description |
|---|---|---|
| Service Catalog | `catalog/services.yaml` | All DigiMinds services with scope, deliverables, timelines |
| Pricing Logic | `pricing/logic.md` | Tiered pricing rules, discount conditions, upsell triggers |
| FAQ Bank | `faqs/general.md` | 200+ answered questions categorized by service area |
| Objection Handlers | `objections/handlers.md` | 50+ sales objections with scripted responses |
| SOP Library | `sops/` | Internal process docs for onboarding, reporting, escalation |
| Personas | `personas/` | Ideal client personas — triggers, pain points, goals |
| Case Studies | `case_studies/` | Anonymized wins with metrics — used in chatbot proofpoints |
| Embeddings | `scripts/embed.py` | Chunk → embed → upsert to Pinecone/Chroma |
| Retrieval | `scripts/retrieve.py` | Query → embed → top-K chunks → LLM answer |
| Eval Suite | `eval/` | Ragas-based RAG evaluation — faithfulness, relevancy, recall |
| Sync Watcher | `scripts/sync_watch.py` | File watcher — re-embeds changed KB docs automatically |
| Chat Interface | `ui/chat.py` | Gradio chat UI for testing retrieval quality |

### 🔥 Hot

| Feature | Location | Description |
|---|---|---|
| Objection Handlers | `objections/handlers.md` | 50 scripted rebuttals — closes deals without human rep |
| Pricing Logic | `pricing/logic.md` | Rule-based engine routes to correct package by need |
| RAG Eval Suite | `eval/` | Ragas metrics prevent hallucinated KB responses in prod |
| Sync Watcher | `scripts/sync_watch.py` | Auto re-embed on KB update — chatbot always current |
| Case Studies | `case_studies/` | Social proof injected into chatbot answers automatically |

---

## ⚙️ HOW IT WORKS

```
KB Files (YAML/MD)
    │
    ▼
Chunker (chunk_size=512, overlap=50)
    │
    ▼
Embedder (nomic-embed-text / text-embedding-3-small)
    │
    ▼
Vector Store (Pinecone / ChromaDB)
    │
    ▼ (at query time)
User Question → Embed → top-5 chunks retrieved
    │
    ▼
LLM (Groq/Gemini) + System Prompt + Retrieved Chunks
    │
    ▼
Chatbot Answer with Citations
```

**Retrieval Strategy:**
- Hybrid search: dense (cosine) + sparse (BM25) → RRF fusion
- Metadata filtering: `service_area`, `intent_type`, `persona`
- Reranking: cross-encoder reranker on top-20 → top-5

---

## 🚀 INSTALL

```bash
git clone https://github.com/hmzainjamil/digiminds-chatbot-kb
cd digiminds-chatbot-kb

pip install -r requirements.txt
# includes: chromadb, sentence-transformers, groq, ragas, watchdog, gradio

cp .env.example .env
# Fill: GROQ_API_KEY, PINECONE_API_KEY (optional), OPENAI_API_KEY (optional)

# Embed entire KB into local ChromaDB
python3 scripts/embed.py --source . --db ./chroma_db

# Test retrieval
python3 scripts/retrieve.py --query "What does DigiMinds charge for Google Ads management?"

# Launch chat UI
python3 ui/chat.py
```

---

## 📟 USAGE

```bash
# Embed all KB docs
python3 scripts/embed.py --source . --db ./chroma_db

# Query the KB
python3 scripts/retrieve.py --query "How long does SEO take to show results?"

# Run Ragas evaluation suite
python3 eval/run_eval.py --questions eval/test_questions.json

# Watch for KB changes and auto-re-embed
python3 scripts/sync_watch.py --source . --db ./chroma_db

# Export KB to JSON (for external chatbot platforms)
python3 scripts/export_kb.py --format json --output ~/Downloads/kb_export.json

# Generate FAQ from service catalog
python3 scripts/generate_faqs.py --service google-ads --count 20

# Chat UI
python3 ui/chat.py  # http://localhost:7860
```

---

## ⚙️ CONFIGURATION

| Variable | Default | Description |
|---|---|---|
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model (Ollama local or OpenAI) |
| `CHUNK_SIZE` | `512` | Token chunk size for KB splitting |
| `CHUNK_OVERLAP` | `50` | Overlap tokens between chunks |
| `TOP_K_RETRIEVAL` | `5` | Number of chunks to retrieve per query |
| `RERANK_TOP_N` | `5` | Final top-N after reranking |
| `LLM_MODEL` | `llama3.1:8b` | Generation model (Ollama/Groq) |
| `CHROMA_DB_PATH` | `./chroma_db` | Local vector store path |
| `GROQ_API_KEY` | — | Groq API key for fast inference |
| `SYSTEM_PROMPT_FILE` | `prompts/system.md` | Path to chatbot system prompt |
| `EVAL_QUESTIONS_FILE` | `eval/test_questions.json` | Ragas evaluation test set |

---

## 💡 TIPS AND TRICKS (12)

[RAG Quality](#tips-rag) · [KB Structure](#tips-kb) · [Sales Logic](#tips-sales) · [Deployment](#tips-deploy)

<a id="tips-rag"></a>■ **RAG Quality (3)**

| Tip | Source |
|---|---|
| Run `eval/run_eval.py` after any KB edit — Ragas faithfulness score should stay >0.85 | Ragas docs |
| Use `chunk_overlap=50` — prevents context loss at chunk boundaries | Chunking best practices |
| Hybrid search (dense+BM25) outperforms pure dense by 15-20% on FAQ retrieval | RAG benchmarks |

<a id="tips-kb"></a>■ **KB Structure (3)**

| Tip | Source |
|---|---|
| Front-load answers in each KB doc — first sentence should answer the question directly | RAG structure guide |
| Add `service_area:` metadata to every KB file — enables filtered retrieval | ChromaDB docs |
| Keep chunks under 400 tokens — longer chunks dilute embedding signal | Embedding best practices |

<a id="tips-sales"></a>■ **Sales Logic (3)**

| Tip | Source |
|---|---|
| Map each objection to a case study — credibility closes skeptics faster than feature lists | Objection handlers |
| Pricing logic should route by budget first, then service need — prevents sticker shock | Pricing logic doc |
| Use persona metadata to adjust chatbot tone — SMB vs enterprise language differs | Personas guide |

<a id="tips-deploy"></a>■ **Deployment (3)**

| Tip | Source |
|---|---|
| Use `sync_watch.py` in production — KB docs update daily, re-embedding takes <2 min | Sync watcher |
| Pinecone prod + ChromaDB dev — same embed/retrieve interface, swap via env var | Architecture guide |
| Set `TOP_K_RETRIEVAL=3` for pricing queries — fewer chunks = less hallucination risk | Retrieval tuning |

---

## 🔧 TROUBLESHOOTING

| Issue | Fix |
|---|---|
| Chatbot answers wrong pricing | Re-embed pricing/logic.md — likely stale chunks |
| Ragas faithfulness <0.7 | Reduce chunk size or improve KB answer quality |
| Slow retrieval | Switch from ChromaDB to Pinecone for >100k chunks |
| `nomic-embed-text` not found | `ollama pull nomic-embed-text` |
| Sync watcher misses changes | Check `watchdog` installed: `pip install watchdog` |
| Chat UI not loading | `pip install gradio>=4.0` |
| Export fails | Check output directory exists: `mkdir -p ~/Downloads` |

---

## 📊 ARCHITECTURE

```
digiminds-chatbot-kb/
├── catalog/
│   └── services.yaml           # Service catalog
├── pricing/
│   └── logic.md                # Pricing rules engine
├── faqs/
│   ├── general.md              # General FAQs
│   ├── google-ads.md           # Google Ads FAQs
│   ├── meta-ads.md             # Meta Ads FAQs
│   └── seo.md                  # SEO FAQs
├── objections/
│   └── handlers.md             # 50+ objection scripts
├── sops/
│   ├── onboarding.md           # Client onboarding SOP
│   ├── reporting.md            # Reporting SOP
│   └── escalation.md          # Issue escalation SOP
├── personas/
│   ├── smb_ecommerce.md        # SMB ecommerce persona
│   └── local_service.md        # Local service business persona
├── case_studies/
│   └── *.md                    # Anonymized case studies
├── scripts/
│   ├── embed.py                # KB embedding pipeline
│   ├── retrieve.py             # Query retrieval
│   ├── sync_watch.py           # Auto re-embed on change
│   ├── export_kb.py            # Export to JSON
│   └── generate_faqs.py        # AI-generated FAQ expansion
├── eval/
│   ├── run_eval.py             # Ragas evaluation runner
│   └── test_questions.json     # Evaluation test set
├── prompts/
│   └── system.md               # Chatbot system prompt
├── ui/
│   └── chat.py                 # Gradio chat interface
└── chroma_db/                  # Local vector store (gitignored)
```

---

## ☠️ STARTUPS / BUSINESSES

| This Repo / Feature | Replaced |
|---|---|
| RAG KB chatbot | Human rep answering same 50 questions 10x/day |
| Objection handlers | Lost deals due to slow or inconsistent responses |
| Pricing logic | Prospect confusion → no quote → lost deal |
| Sync watcher | Stale chatbot answers after price changes |
| Ragas eval suite | No way to know if chatbot was hallucinating |
| Case studies in KB | Generic chatbot with no social proof |
| SOP library | Tribal knowledge lost when staff churns |
| FAQ bank | Each rep inventing their own answers |

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hmzainjamil/digiminds-chatbot-kb&type=Date)](https://star-history.com/#hmzainjamil/digiminds-chatbot-kb&Date)

---
<div align="center">Built by <a href="https://github.com/hmzainjamil">HMZ</a> · Part of HMZ Claude AI System</div>

---

## 🔬 KB PERFORMANCE METRICS

| Metric | Target | Measurement |
|---|---|---|
| Ragas Faithfulness | >0.85 | `eval/run_eval.py` |
| Ragas Answer Relevancy | >0.80 | `eval/run_eval.py` |
| Context Recall | >0.75 | `eval/run_eval.py` |
| Response Latency | <2s | Gradio UI timing |
| Cache Hit Rate | >30% | Redis stats |
| Unanswered Rate | <10% | Chat logs review |

---

## 📋 KB CONTENT STANDARDS

Every KB document must follow this format:

```markdown
---
service_area: google-ads
intent_type: pricing | faq | objection | sop
persona: smb | enterprise | local
last_updated: 2025-01-15
---

# Question or Topic Title

**Answer:** Direct one-paragraph answer here.

**Details:** Supporting context, caveats, examples.

**Source:** Internal SOP v3.2 / Client results data
```

---

## 🔧 KB EXPANSION WORKFLOW

```bash
# Step 1: Write new KB doc following content standards
vim faqs/new_service_faqs.md

# Step 2: Validate format
python3 scripts/validate_kb.py --file faqs/new_service_faqs.md

# Step 3: Embed new doc
python3 scripts/embed.py --source faqs/new_service_faqs.md --db ./chroma_db

# Step 4: Test retrieval
python3 scripts/retrieve.py --query "question from new doc"

# Step 5: Run eval to check no regression
python3 eval/run_eval.py --questions eval/test_questions.json
```

---

## 🔄 CONTRIBUTING

Contributions welcome for:
- Additional service area FAQs
- More objection handlers
- New persona profiles
- Evaluation question sets
- Integration with Intercom / Tidio / Crisp APIs
