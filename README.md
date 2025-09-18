# SEO Tracker Agent

SEO Tracker Agent is a multi-agent SEO assistant built with Google's Agent Development Kit (ADK) for the Google Agentic Hackathon. It audits any public web page, explains how the page scores against SEO best practices, and can immediately rewrite copy or generate visuals to improve the result.

## What the agent delivers
- **Automated page audits.** The root agent delegates every URL to a dedicated evaluator that extracts the page structure, measures compliance with SEO rules, and stores the findings for follow-up actions.【F:app/agent.py†L27-L45】【F:app/sub_agents/seo_content_evaluator_agent/agent.py†L17-L53】
- **Actionable, end-to-end reports.** Prompting enforces a three-stage workflow—crawl, score, and recommend—so responses always contain keyword density, pass/fail checks, prioritized fixes, and next steps.【F:app/prompt.py†L32-L170】
- **Hands-on optimization.** An editing orchestrator can rewrite titles, headings, paragraphs, and image alt text, or pass requests to an image generator for fresh creative with SEO-friendly descriptions.【F:app/sub_agents/edit_content_agent/agent.py†L12-L36】【F:app/sub_agents/edit_content_agent/prompt.py†L6-L198】

## Agent architecture
1. **`seo_tracker` root agent** – Receives every user request, chooses between evaluation and editing flows, and keeps shared state through the `memorize` tool.【F:app/agent.py†L27-L45】【F:app/tools/memory.py†L39-L53】
2. **Evaluation pipeline** – `seo_content_evaluator_agent` runs `html_content_extractor_agent` to inventory tags and text, then `content_seo_ruler_agent` to compute scores, capture keyword density, and log recommendations.【F:app/sub_agents/seo_content_evaluator_agent/agent.py†L17-L53】【F:app/tools/html_parser.py†L11-L155】【F:app/tools/seo_analyze.py†L9-L75】
3. **Optimization pipeline** – `edit_content_agent` routes copy requests to `edit_text_content_agent` (title/meta/heading/paragraph tools) and visual requests to `image_generator_agent`, returning a unified response.【F:app/sub_agents/edit_content_agent/agent.py†L12-L36】【F:app/tools/recreate_page.py†L7-L177】【F:app/tools/recreate_image.py†L12-L69】

## Core tools
| Tool | Purpose |
| --- | --- |
| `extract_html_content`, `extract_specific_tags` | Crawl pages and build a structured inventory of headings, paragraphs, and divs with counts and metadata.【F:app/tools/html_parser.py†L11-L156】 |
| `analyze_webpage_seo`, `extract_page_keywords` | Score technical SEO checks, capture keyword statistics, and persist the detailed report for downstream steps.【F:app/tools/seo_analyze.py†L9-L137】 |
| `optimize_title_tag`, `optimize_meta_description`, `optimize_headings`, `optimize_paragraph_content`, `generate_image_alt_texts` | Produce SEO-compliant rewrites guided by length limits, keyword strategy, and readability safeguards.【F:app/tools/recreate_page.py†L7-L240】 |
| `generate_image_with_alt_text` | Create on-brand images with Gemini and return SEO-optimized alt text while saving artifacts to Vertex AI storage.【F:app/tools/recreate_image.py†L12-L69】 |
| `memorize` | Share intermediate results across agents during a session, enabling edits to build on previous audits.【F:app/tools/memory.py†L39-L53】 |

## Prerequisites and configuration
- **uv package manager** for dependency management (`make install`).【F:Makefile†L2-L4】
- **Google Cloud SDK & Terraform** for provisioning development or production environments (`make setup-dev-env`).【F:Makefile†L22-L25】
- **make** to run the provided automation targets.【F:Makefile†L2-L37】
- **Vertex AI project configuration.** Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` so deployment, tracing, and image generation can authenticate against your GCP project.【F:app/agent_engine_app.py†L36-L76】【F:app/tools/recreate_image.py†L12-L41】

## Run locally
1. **Install dependencies**
   ```bash
   make install
   ```
   This installs uv (if missing) and syncs project dependencies.【F:Makefile†L2-L4】
2. **Launch the playground**
   ```bash
   make playground
   ```
   Starts the ADK web playground on port 8501 with hot-reloading for your agents.【F:Makefile†L6-L14】

## Quality checks
- **Unit and integration tests**
  ```bash
  make test
  ```
  Runs the pytest suites under `tests/unit` and `tests/integration`.【F:Makefile†L27-L29】
- **Lint and type checks**
  ```bash
  make lint
  ```
  Executes codespell, Ruff lint/format in check mode, and mypy type checking.【F:Makefile†L31-L37】

## Deploy to Vertex AI Agent Builder
1. Export dependencies and trigger deployment with the provided make target:
   ```bash
   make backend
   ```
   The target writes `.requirements.txt` with uv and calls `app/agent_engine_app.py` to push the agent to Vertex AI Agent Engine.【F:Makefile†L16-L21】
2. Alternatively, run the deployment script directly for more control (custom project, region, env vars, or service account):
   ```bash
   uv run app/agent_engine_app.py --project <project-id> --location <region> --agent-name <name> \
     --requirements-file .requirements.txt --extra-packages ./app
   ```
   The script provisions staging and artifact buckets, registers tracing, and creates or updates the remote agent before saving metadata to `deployment_metadata.json`.【F:app/agent_engine_app.py†L59-L194】

## Customizing the agent
- **Adjust audit depth or messaging** by editing the SEO tracker prompt, which enforces the crawl → score → recommend workflow and the reporting template.【F:app/prompt.py†L32-L170】
- **Tune editing behavior** by updating the orchestrator and optimization prompts that control routing, tone, and output format for rewritten content and generated imagery.【F:app/sub_agents/edit_content_agent/prompt.py†L6-L240】
- **Extend tooling** by adding new tools or utilities in `app/tools/` and registering them with the relevant sub-agent definitions.【F:app/sub_agents/seo_content_evaluator_agent/agent.py†L17-L52】【F:app/sub_agents/edit_content_agent/agent.py†L12-L36】

Bring a URL to the playground, and the agent will return a full SEO health report along with the option to rewrite or visually refresh the page in a single session.
