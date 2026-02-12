# TankScan Intelligent Textbook

[![Live Site](https://img.shields.io/badge/📖_Read_Online-yarmoluk.github.io-1E88E5?style=for-the-badge)](https://yarmoluk.github.io/tankscan-course/)
[![Chapters](https://img.shields.io/badge/Chapters-15-success?style=for-the-badge)](https://yarmoluk.github.io/tankscan-course/)
[![Bloom's Taxonomy](https://img.shields.io/badge/Bloom's_Taxonomy-Aligned-orange?style=for-the-badge)](https://yarmoluk.github.io/tankscan-course/course-description/)

> ### Wireless Tank Monitoring Systems: From Sensors to Smart Decisions
> A comprehensive intelligent textbook on wireless tank monitoring technology, IoT architecture, data analytics, and AI-driven asset management.

---

### For Craig Truempi

This intelligent textbook is dedicated to **Craig Truempi** and the TankScan team for their pioneering work in wireless tank monitoring since 2003. It demonstrates the power of AI-driven educational content: taking a company's domain expertise and transforming it into a structured, interactive learning resource.

---

## The AI-Powered Pipeline

This entire textbook was generated through a systematic process:

```
  Research  →  Course Description  →  Bloom's Taxonomy  →  Learning Graph  →  15 Chapters  →  Chatbot
```

| Step | What It Does |
|------|-------------|
| **1. Research** | Domain analysis of TankScan technology, products, and market |
| **2. Course Description** | Structured curriculum with learning objectives |
| **3. Bloom's Taxonomy** | Outcomes aligned across all 6 cognitive levels |
| **4. Learning Graph** | 90+ interconnected concepts with dependencies |
| **5. Chapter Generation** | 15 chapters of educational content with diagrams and formulas |
| **6. Chatbot** | AI assistant that answers any question about the material |

---

## Textbook Contents

| Ch. | Title | Key Topics |
|:---:|-------|------------|
| 1 | **Introduction to Tank Monitoring** | History, wireless revolution, TankScan overview |
| 2 | **Wireless Sensor Technologies** | Sensor types, accuracy, performance metrics |
| 3 | **Radar and Ultrasonic Measurement** | FMCW radar, time-of-flight, ultrasonic principles |
| 4 | **IoT Architecture and Connectivity** | Cellular, Wi-Fi, satellite, gateways |
| 5 | **The Asset Intelligence Platform** | Cloud dashboard, alerts, mapping, open API |
| 6 | **Tank Types and Applications** | AST, UST, totes, IBCs, tank farms |
| 7 | **Industry Solutions** | Fuel, chemicals, lubricants, waste oil, c-stores |
| 8 | **Installation and Deployment** | Site surveys, mounting, commissioning, scaling |
| 9 | **Data Analytics and Optimization** | Trends, forecasting, anomaly detection |
| 10 | **Fleet Management and Routing** | Route optimization, 30% efficiency gains |
| 11 | **Safety and Compliance** | C1D1/C1D2, ATEX, EPA regulations |
| 12 | **Cloud Integration and APIs** | REST API, ERP, cloud-to-cloud integration |
| 13 | **Predictive Maintenance and AI** | ML, digital twins, demand forecasting |
| 14 | **Case Studies and ROI** | Real-world deployments, cost-benefit analysis |
| 15 | **Future of Tank Monitoring** | 5G, edge AI, autonomous delivery |

**Plus:** Learning Graph (90+ concepts) &bull; Glossary (65+ terms) &bull; Interactive Chatbot

---

## Quick Start

### Read the Textbook Online

**[yarmoluk.github.io/tankscan-course](https://yarmoluk.github.io/tankscan-course/)**

### Run Locally

```bash
git clone https://github.com/Yarmoluk/tankscan-course.git
cd tankscan-course
pip install -r requirements.txt
mkdocs serve
```

### Launch the Chatbot

```bash
pip install -r chatbot/requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python chatbot/build_knowledge_base.py
streamlit run chatbot/app.py
```

---

## Project Structure

```
tankscan-course/
├── docs/
│   ├── index.md                  # Home page
│   ├── preface.md                # Foreword dedicated to Craig Truempi
│   ├── course-description.md     # Curriculum with Bloom's Taxonomy
│   ├── chapters/                 # 15 complete chapters
│   ├── learning-graph/           # 90+ concept dependency map
│   └── glossary/                 # 65+ key terms
├── chatbot/
│   ├── app.py                    # Streamlit chatbot application
│   ├── build_knowledge_base.py   # Knowledge base compiler
│   └── knowledge_base.txt        # 102K+ word knowledge base
├── .github/workflows/            # Auto-deploy to GitHub Pages
├── mkdocs.yml                    # Site configuration
└── requirements.txt              # Dependencies
```

---

## About TankScan

[TankScan](https://tankscan.com) was founded in 2003 as a pioneer in wireless tank monitoring when manual checks were the industry norm. TankScan provides best-in-class hardware monitors and the cloud-based **Asset Intelligence Platform (AIP)** to help companies across industries maximize efficiency and make data-driven decisions.

**Products:** TSR Cellular Monitor &bull; TSU Ultrasonic Monitor &bull; TSP Pressure Monitor &bull; TSC C-Store System &bull; TSD Dial Gauge Reader &bull; TSG BYOS Monitor

**Industries:** Fuel Distribution &bull; C-Store Petroleum &bull; Lubricants &bull; Specialty Chemicals &bull; Used Oil Collection &bull; Oil Field Support

---

<p align="center">
<em>Built with Claude Code &bull; February 2026 &bull; Daniel Yarmoluk</em>
</p>
