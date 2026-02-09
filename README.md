---

# GarimpoBot (Project Prospector)

An Open-Architecture Web Platform enabling the Circular Economy through AI-driven local market efficiency.

## 📌 Table of Contents

1. [Quick Start (Development)](#quick-start)
2. [Project Vision & The Market Problem](#vision)
3. [Market Potential & The Ecosystem](#market)
4. [Architecture & Business Roadmap](#architecture)
5. [Repository Structure](#structure)
6. [References & Market Validation](#references)

---

## <a id="quick-start"></a>🚀 Quick Start (Development)

This repository contains the core API engine and the Flet Web UI.

### Prerequisites

* Python 3.10+
* Playwright (Chromium)

### Installation

1. **Clone the repo and configure environment variables (.env):**

```env
GEMINI_API_KEY=your-gemini-api-key
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
playwright install chromium

```

3. **Run the Web Application:**

```bash
python run.py --mode api

```

The Web UI will be available at http://localhost:8000.

---

## <a id="vision"></a>📌 Project Vision & The Market Problem

GarimpoBot is a fully responsive AI-driven Web Platform (SaaS) designed to democratize access to the second-hand market.

Currently, local marketplaces (OLX, Facebook Marketplace, Craigslist) are fragmented. Micro-entrepreneurs and resellers face a high barrier to entry, spending hours manually tracking inventory. GarimpoBot automates "digital mining" (Garimpo) through an intuitive Web Interface, allowing users to define parameters (e.g., "PlayStation 5 up to $400 in NY") and receive instant alerts via Web Hooks.

### 🌍 Social Impact (UN SDGs)

This project is technically aligned with the United Nations Sustainable Development Goals, backed by real market data:

* **SDG 12 (Responsible Consumption):** By accelerating the transaction speed of used goods among **176 million potential consumers**, we extend product lifecycles and actively drive the Circular Economy, reducing e-waste.
* **SDG 8 (Decent Work & Economic Growth):** We lower the technological barrier for **4.5 million active sellers and 6.4 million SMEs**, providing them with enterprise-grade sourcing tools.

---

## <a id="market"></a>📊 Market Potential & The Ecosystem

Brazil is a nation seeking financial efficiency. We identified a massive, underserved ecosystem where practically every active citizen and business needs to buy or sell better.

| Market Metric | Scale | Definition & Narrative |
| --- | --- | --- |
| **TAM (The Dream)** | **~186 Million** Touchpoints | **176M Consumers + 4.5M Sellers + 6.4M SMEs.** Validated by the 2024 Gamer Census and E-commerce growth metrics. The total potential market seeking efficiency. |
| **SAM (Digital Demand)** | **~35.7 Million** Monthly Leads | **29.9M Deal Seekers + 4.5M Active Sellers + 1.3M Food Service Businesses.** This is the audience *already* actively searching for deals or suppliers online right now, validated by Abrasel and National Data. |
| **SOM (Year 1 Goal)** | **~310,000** Paying Users | **290k Snipers + 4.5k Stockers + 13.7k B2B Prospectors.** A conservative goal of capturing <1% of the active demand, driven by viral Gamer adoption and the influx of ~10 Million higher education students seeking extra income. |

---

## <a id="architecture"></a>🏗️ Architecture & Business Roadmap

GarimpoBot is designed for high-concurrency to support our Year 1 user goals.

### Phase 1: PoC & Market Validation (Current MVP)

To validate the "Sniper" user behavior (fast, local purchases) with zero friction, the current v0.1 utilizes:

* **The Web App (Flet/Flutter):** A seamless, cross-platform UI for rapid user onboarding.
* **Headless Browser Agents:** Temporary DOM scraping for un-federated platforms.
* **Aggressive Rate Limiting:** Hard limits to respect robots.txt, maintain 1GB RAM server constraints, and prevent IP blacklisting.
* **JSON Persistence:** Frictionless local storage for rapid prototyping.

### Phase 2: B2B Partnerships & The Affiliate Flywheel

GarimpoBot is not a scraping company; it is a lead generation ecosystem for our 35.7M monthly leads.
The production roadmap (v1.0) pivots from scraping to Official API/OAuth Integrations with the marketplaces. With the Brazilian second-hand and refurbished market growing over 150%, feeding millions of qualified buyers directly into partner platforms sustains the project via **Affiliate Partnerships** (projected to be 78.8% of revenue), ensuring low server overhead and 100% legal compliance.

---

## <a id="structure"></a>📂 Repository Structure

```text
src/prospector_bot/
├── agents/              # Connectors (Craigslist RSS, eBay Finding API, FB Scraper)
├── api/                 # FastAPI REST Endpoints & Flet Web Handlers
├── i18n.py              # Internationalization Engine (EN, ES, FR, DE, PT-BR)
└── ai_client.py         # Google Gemini LLM Integration (Hyper-compressed parameters)

```

## 🤝 Contributing

We are actively looking for contributors to help scale the Circular Economy!
If you are a developer, we welcome PRs for:

* **Front-end:** Enhancements for our Flet/Flutter Web UI.
* **Connectors:** Official API integrations (replacing legacy scrapers).
* **Databases:** Migrating the local JSON storage to PostgreSQL & Redis for the v1.0 release.

---

## <a id="references"></a>📑 References & Market Validation

The architecture decisions and market scoping for this product are backed by official 2023/2024 sector data:

1. **Meio e Mensagem / PGB 2024:** *Cresce o número de brasileiros que jogam, afirma PGB 2024*. Validates the 176M+ consumer baseline. [Link](https://meioemensagem.com.br/marketing/cresce-o-numero-de-brasileiros-que-jogam-afirma-pgb-2024)
2. **Estadão / Abrasel:** *O tamanho do setor de Bares e Restaurantes*. Validates the 1.3M+ B2B SAM. [Link](https://especiais.estadao.com.br/abrasel/diagnostico-e-iniciativas/o-tamanho-do-setor/)
3. **Exame:** *Compra de produtos recondicionados cresce mais de 150% no Brasil*. Validates second-hand/circular economy growth. [Link](https://exame.com/bussola/compra-de-produtos-recondicionados-cresce-mais-de-150-no-brasil/)
4. **Camargo e Associados:** *Porcentagem de Pequenas e Médias Empresas no Brasil*. Validates the 6.4M SMEs ecosystem. [Link](https://www.camargoeassociados.com.br/CamargoOnLine/Artigo20240629.aspx)
5. **Gov.br / INEP:** *Inep divulga resultado do Censo Superior 2024 (Quase 10 milhões de universitários)*. Validates the Reseller persona growth potential. [Link](https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/censo-da-educacao-superior/inep-divulga-resultado-do-censo-superior-2024)

---

**Legal Disclaimer & Compliance:** This codebase is a Proof of Concept (PoC). It operates statelessly and collects no sensitive user data (GDPR/LGPD compliant). Contributors and users are strictly responsible for ensuring their configurations comply with the Terms of Service (TOS) and privacy guidelines of any monitored platform.

---
