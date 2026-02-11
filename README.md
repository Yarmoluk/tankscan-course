# TankScan Intelligent Textbook

[![MkDocs](https://img.shields.io/badge/Built%20with-MkDocs%20Material-blue)](https://squidfunk.github.io/mkdocs-material/)
[![Chapters](https://img.shields.io/badge/Chapters-15-green)](https://github.com/Yarmoluk/tankscan-course)
[![Bloom's Taxonomy](https://img.shields.io/badge/Bloom's%20Taxonomy-Aligned-orange)](https://github.com/Yarmoluk/tankscan-course)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **Wireless Tank Monitoring Systems: From Sensors to Smart Decisions**

A comprehensive intelligent textbook covering TankScan's wireless tank monitoring technology, IoT architecture, data analytics, and AI-driven asset management. Built using an AI-powered educational content pipeline.

---

## About This Project

This intelligent textbook was created as a demonstration of AI-powered educational content generation. It takes TankScan's domain expertise in wireless tank monitoring and transforms it into structured, comprehensive educational material aligned with Bloom's Taxonomy.

**Dedicated to Craig Truempi**, owner of ITEK, LLC and TankScan, for his pioneering work in wireless tank monitoring and IIoT.

### The Pipeline

```
Site Research → Course Description → Bloom's Taxonomy → Learning Graph → Chapter Generation → Chatbot
```

1. **Research** - Domain analysis of TankScan technology, products, and market
2. **Course Description** - Structured curriculum with learning objectives
3. **Bloom's Taxonomy** - Learning outcomes aligned to 6 cognitive levels
4. **Learning Graph** - 90+ interconnected concepts with dependencies
5. **Chapter Generation** - 15 chapters of full educational content
6. **Chatbot** - AI assistant trained on the textbook content

---

## Contents

| Chapter | Title | Key Topics |
|---------|-------|------------|
| 1 | Introduction to Tank Monitoring | History, wireless revolution, TankScan overview |
| 2 | Wireless Sensor Technologies | Sensor types, accuracy, performance metrics |
| 3 | Radar and Ultrasonic Measurement | FMCW radar, time-of-flight, ultrasonic |
| 4 | IoT Architecture and Connectivity | Cellular, Wi-Fi, satellite, gateways |
| 5 | The Asset Intelligence Platform | Cloud dashboard, alerts, mapping, API |
| 6 | Tank Types and Applications | AST, UST, totes, IBCs, tank farms |
| 7 | Industry Solutions | Fuel, chemicals, lubricants, waste oil |
| 8 | Installation and Deployment | Site surveys, mounting, commissioning |
| 9 | Data Analytics and Optimization | Trends, forecasting, anomaly detection |
| 10 | Fleet Management and Routing | Route optimization, 30% efficiency gain |
| 11 | Safety and Compliance | C1D1/C1D2, ATEX, EPA regulations |
| 12 | Cloud Integration and APIs | REST API, ERP, cloud-to-cloud |
| 13 | Predictive Maintenance and AI | ML, digital twins, demand forecasting |
| 14 | Case Studies and ROI | Real-world deployments, cost-benefit |
| 15 | Future of Tank Monitoring | 5G, edge AI, autonomous delivery |

Plus: **Learning Graph**, **Glossary** (65+ terms), and **Interactive Chatbot**

---

## Quick Start

### View the Textbook

```bash
# Clone the repository
git clone https://github.com/Yarmoluk/tankscan-course.git
cd tankscan-course

# Install dependencies
pip install -r requirements.txt

# Serve locally
mkdocs serve
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

### Run the Chatbot

```bash
# Install chatbot dependencies
pip install -r chatbot/requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=your-key-here

# Build the knowledge base
python chatbot/build_knowledge_base.py

# Launch the chatbot
streamlit run chatbot/app.py
```

---

## Technology Stack

- **MkDocs Material** - Static site generator with Material Design theme
- **Mermaid** - Diagrams and flowcharts in markdown
- **MathJax** - Mathematical formula rendering
- **Streamlit** - Chatbot web interface
- **Anthropic Claude** - AI for content generation and chatbot responses
- **Python** - Knowledge base builder and analytics

---

## Project Structure

```
tankscan-course/
├── docs/
│   ├── index.md                    # Home page
│   ├── preface.md                  # Foreword to Craig Truempi
│   ├── course-description.md       # Curriculum with Bloom's Taxonomy
│   ├── chapters/
│   │   ├── 01-introduction/        # Chapter 1-15
│   │   ├── 02-wireless-sensors/
│   │   ├── ...
│   │   └── 15-future/
│   ├── learning-graph/             # Concept dependency map
│   └── glossary/                   # 65+ key terms
├── chatbot/
│   ├── app.py                      # Streamlit chatbot application
│   ├── build_knowledge_base.py     # Knowledge base compiler
│   └── requirements.txt            # Chatbot dependencies
├── mkdocs.yml                      # MkDocs configuration
├── requirements.txt                # MkDocs dependencies
└── README.md                       # This file
```

---

## About TankScan

[TankScan](https://tankscan.com) was founded in 2003 as a pioneer in wireless tank monitoring. Now part of the AquaPhoenix Scientific family, TankScan provides best-in-class hardware monitors and the cloud-based Asset Intelligence Platform (AIP) to help companies across industries maximize efficiency, improve operations, and make data-driven decisions.

**Key Products:** TSR Cellular Monitor, TSU Ultrasonic Monitor, TSP Pressure Monitor, TSC C-Store System, TSD Dial Gauge Reader, TSG BYOS Monitor

**Industries Served:** Fuel Distribution, C-Store Petroleum, Lubricants, Specialty Chemicals, Used Oil Collection, Oil Field Support

---

## License

This project is for educational and demonstration purposes.

---

*Built with Claude Code | February 2026*
