# 🌍 Mental Health Atlas

> **A Comprehensive Study & Interactive Exploration of Global Mental Health Trends (1990–2019)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-2f5d46.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-b5683a.svg?style=flat-square)](LICENSE)
[![Zero Framework Dependencies](https://img.shields.io/badge/web-built--in%20http.server-a9b8a0.svg?style=flat-square)](https://docs.python.org/3/library/http.server.html)
[![Data Source: Our World in Data / IHME](https://img.shields.io/badge/data-Our%20World%20in%20Data%20%2F%20IHME-2b2d2a.svg?style=flat-square)](https://ourworldindata.org/mental-health)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Architecture](#-project-architecture)
- [Repository Structure](#-repository-structure)
- [Datasets](#-datasets)
- [Installation & Quickstart](#-installation--quickstart)
- [Usage Guide](#-usage-guide)
  - [Web Application (`app.py`)](#web-application-apppy)
  - [Data Science Lab (`mental_health_analysis.ipynb`)](#data-science-lab-mental_health_analysisipynb)
- [Technical Implementation](#-technical-implementation)
- [Key Epidemiological Insights](#-key-epidemiological-insights)
- [Limitations & Disclaimer](#-limitations--disclaimer)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🔭 Overview

**Mental Health Atlas** is an end-to-end data analysis and web exploration project investigating global mental health patterns over three decades (1990–2019). Utilizing data originally collected by the **Institute for Health Metrics and Evaluation (IHME) Global Burden of Disease (GBD)** study and curated by **Our World in Data** (via Kaggle), this project examines:

1. **Prevalence**: What percentage of populations live with depression, anxiety, bipolar disorder, schizophrenia, and eating disorders?
2. **Disease Burden (DALYs)**: How many years of healthy life are lost per 100,000 individuals due to illness and disability?
3. **Longitudinal Trends**: How have average disorder rates evolved from 1990 to 2019 across nations?
4. **Disparity & Treatment Gaps**: What fraction of affected individuals receive adequate care vs. remaining untreated?
5. **Data Coverage & Scarcity**: Which parts of the globe actually have primary empirical measurements versus statistical estimations?

The project uniquely pairs an interactive **Jupyter research notebook** (for step-by-step EDA and modeling) with a **production web atlas** engineered entirely with Python's built-in standard library server (`http.server`) and core data libraries (`pandas`, `numpy`, `matplotlib`), requiring **zero heavy web frameworks** (like Flask or Django).

---

## ✨ Key Features

### 🌐 1. Interactive Web Application (`app.py`)
- **Dashboard (`/`)**: Displays high-level macro statistics, total dataset rows, years spanned, and 2019 global prevalence benchmarks.
- **Dataset Explorer (`/explore`)**: A searchable, filterable tabular viewer for all seven CSV files with keyword search, country/entity dropdowns, year filters, and pagination.
- **Trends Analysis (`/trends`)**: Longitudinal visualizations tracking cross-country averages, percentage changes from 1990 to 2019, and 10-year cohort snapshots.
- **Country Comparison (`/countries`)**: Multi-country selector allowing direct comparative analysis of up to 3 nations across specific disorders, alongside grouped bar charts of 2019 disease burdens (DALYs).
- **Conditions Deep Dive (`/conditions`)**: Disorder rankings by prevalence and burden, top 10 most affected nations, horizontal stacked bar charts of the anxiety treatment gap, and US depressive symptom frequency breakdowns.
- **About & Methodology (`/about`)**: Complete project documentation, syllabus concepts applied, data coverage visualizations, and methodological limitations.

### 🔬 2. Data Science Lab (`mental_health_analysis.ipynb`)
- Reproducible, documented Jupyter Notebook with Markdown commentary.
- Step-by-step data ingestion, schema harmonization, missing value diagnostics, and regional filtering.
- Grouped statistical aggregations and high-resolution chart generation.

### 🎨 3. Editorial Design System
- Custom, distraction-free aesthetic with an earthy, publication-grade color scheme (`#faf6ee` warm paper, `#2f5d46` forest green, `#a9b8a0` sage, and `#b5683a` terracotta accent).
- Responsive grid and card layout built in pure Vanilla CSS (`static/css/style.css`).
- Headless chart generation via Matplotlib's `Agg` backend with consistent palettes, typography, and clean spine formatting.

---

## 🏛 Project Architecture

```
                       ┌───────────────────────────────┐
                       │     Raw CSV Datasets (7)      │
                       │   (Kaggle / OWID / IHME GBD)   │
                       └──────────────┬────────────────┘
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
     ┌───────────────────────────┐         ┌───────────────────────────┐
     │   Data Science Lab        │         │   Web Presentation Layer  │
     │ mental_health_analysis    │         │          (app.py)         │
     │          .ipynb           │         └─────────────┬─────────────┘
     └───────────────────────────┘                       │
                                           ┌─────────────┴─────────────┐
                                           ▼                           ▼
                              ┌────────────────────────┐  ┌────────────────────────┐
                              │  Built-in HTTP Server  │  │ Dynamic Matplotlib Gen │
                              │     (port 8000)        │  │     (charts/*.png)     │
                              └────────────┬───────────┘  └────────────────────────┘
                                           ▼
                              ┌────────────────────────┐
                              │ HTML & CSS Templates   │
                              │ (templates/layout.html │
                              │  static/css/style.css) │
                              └────────────────────────┘
```

---

## 📂 Repository Structure

```
mental_health_atlas/
├── app.py                         # Main web application & built-in HTTP server
├── mental_health_analysis.ipynb   # Jupyter Notebook for exploratory data analysis
├── requirements.txt               # Python package dependencies
├── README.md                      # Project documentation
├── data/                          # 7 Primary CSV datasets
│   ├── 1_prevalence.csv           # Disorder prevalence by country & year (1990-2019)
│   ├── 2_burden_dalys.csv         # Disability-Adjusted Life Years (DALYs) per 100k
│   ├── 3_coverage_depression.csv  # Major depression regional data coverage (2008)
│   ├── 4_coverage_all.csv         # Coverage across 6 disorders by region (2008)
│   ├── 5_treatment_gap.csv        # Anxiety treatment distribution survey data
│   ├── 6_symptoms_us.csv          # US adult depressive symptom survey frequencies (2014)
│   └── 7_countries_with_data.csv  # Number of countries with primary prevalence data (2019)
├── templates/
│   └── layout.html                # Base HTML5 layout template
├── static/
│   └── css/
│       └── style.css              # Custom editorial stylesheet
└── charts/                        # Auto-generated visualization PNG files
```

---

## 📊 Datasets

The project utilizes seven datasets covering epidemiological, geographic, and survey dimensions:

| # | File Name | Title | Rows | Description |
|---|---|---|:---:|---|
| **1** | `1_prevalence.csv` | **Prevalence of Mental Disorders** | 6,468 | Share of population (%) diagnosed with depression, anxiety, bipolar, schizophrenia, and eating disorders (1990–2019). |
| **2** | `2_burden_dalys.csv` | **Disease Burden (DALYs)** | 6,468 | Disability-Adjusted Life Years lost per 100,000 individuals across the five conditions. |
| **3** | `3_coverage_depression.csv` | **Data Coverage: Depression** | 29 | Percentage of regional adult populations covered by primary data on major depression (2008). |
| **4** | `4_coverage_all.csv` | **Data Coverage: All Disorders** | 29 | Regional primary data coverage across 6 psychiatric disorders (2008). |
| **5** | `5_treatment_gap.csv` | **Anxiety Treatment Gap** | 27 | Share of individuals receiving adequate treatment, other treatment, or remaining untreated. |
| **6** | `6_symptoms_us.csv` | **US Depressive Symptoms** | 9 | Reported frequency of core depressive symptoms among US adults (2014). |
| **7** | `7_countries_with_data.csv` | **Primary Data Availability** | 5 | Count of nations with empirical primary data for each disorder (2019). |

---

## ⚙️ Installation & Quickstart

### Prerequisites
- Python **3.8** or higher
- `pip` (Python package installer)

### 1. Clone or Download the Repository
```bash
git clone https://github.com/your-username/mental_health_atlas.git
cd mental_health_atlas
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Contents: `pandas`, `numpy`, `matplotlib`)*

---

## 🚀 Usage Guide

### Web Application (`app.py`)

To run the interactive web application:

```bash
python app.py
```

Once started, open your web browser and navigate to:
```
http://localhost:8000
```

*Press `Ctrl+C` in your terminal to shut down the server.*

#### Available URL Endpoints:
- `http://localhost:8000/` — Main dashboard with summary metrics.
- `http://localhost:8000/explore` — Full dataset explorer with search, filtering, and pagination.
- `http://localhost:8000/trends` — 30-year trend analyses and percentage change statistics.
- `http://localhost:8000/countries` — Custom comparative analysis between up to 3 countries.
- `http://localhost:8000/conditions` — Breakdown of individual conditions, top 10 rankings, and treatment gap.
- `http://localhost:8000/about` — Research methodology, academic syllabus topics, and data limitations.

---

### Data Science Lab (`mental_health_analysis.ipynb`)

To run and explore the Jupyter Notebook:

```bash
# If jupyter is not installed:
pip install jupyter

# Launch the notebook environment:
jupyter notebook mental_health_analysis.ipynb
```

The notebook guides you through data cleaning, regional vs. sovereign state filtering, summary statistics generation, and visualization generation with inline plots.

---

## 🛠 Technical Implementation

### 1. Data Cleaning & Normalization
- **Column Shortening**: Standardizes verbose IHME GBD column names (e.g., `"Prevalence - Depressive disorders - Sex: Both - Age: Age-standardized (Percent)"` $\rightarrow$ `"Depressive disorders"`).
- **Regional Disaggregation**: Isolates sovereign countries by filtering out regional aggregates (entities without country codes or with `OWID_*` regional codes) to avoid double-counting in national averages.
- **Type Coercion**: Cleans numeric fields containing string anomalies using `pd.to_numeric(..., errors="coerce")`.

### 2. Zero-Dependency Web Architecture
Rather than relying on third-party frameworks like Flask, FastAPI, or Django, `app.py` leverages:
- `http.server.HTTPServer` and `http.server.BaseHTTPRequestHandler` for request processing.
- `urllib.parse` for query string parsing (`parse_qs`) and URL reconstruction (`urlencode`).
- Reusable HTML string templates and pagination math (`numpy.ceil`).

### 3. Automated Headless Visualization
- Matplotlib uses the headless `Agg` backend (`matplotlib.use("Agg")`), allowing charts to render as PNG assets without requiring a GUI window server.
- Figures automatically save into `charts/` with custom aspect ratios, consistent serif typography, hidden spines, and uniform palettes before being referenced dynamically by the web pages.

---

## 💡 Key Epidemiological Insights

1. **Prevalence Disparity**: Depression and anxiety disorders affect significantly larger shares of populations (~3.5% to 4.5% global cross-country averages) compared to bipolar disorder (~0.7%), schizophrenia (~0.25%), and eating disorders (~0.2%).
2. **Age-Standardized Stability**: Global averages across the 30-year span (1990–2019) exhibit gradual changes because figures are age-standardized, neutralizing the confounding effects of aging populations.
3. **The Treatment Gap**: In survey datasets, an average of over **50% of individuals diagnosed with anxiety disorders received no treatment**, highlighting critical disparities in global mental healthcare infrastructure.
4. **The Measurement Void**: A significant portion of reported figures for developing regions are model-based statistical estimates. As shown in coverage files, multiple global regions had zero primary empirical data coverage for major depression in baseline surveys.

---

## ⚠️ Limitations & Disclaimer

> [!IMPORTANT]
> **Educational & Analytical Use Only**: This project was developed as an educational data analysis project. It is strictly intended for statistical research and data science demonstration. It is **not** a clinical diagnostic tool and should not be used as medical advice. If you or someone you know is struggling with mental health, please reach out to licensed healthcare professionals or your local crisis helpline.

- **Modelled Estimates**: Figures in files 1 and 2 derive from IHME GBD Bayesian statistical modeling rather than exhaustive global health censuses.
- **Reporting Disparities**: Variations in prevalence between countries often reflect differences in diagnostic capacity, cultural stigma, screening practices, and healthcare accessibility rather than biological incidence alone.
- **Temporal Inconsistencies**: Survey datasets (files 5 and 6) represent single-year point estimates from specific cohorts and should not be over-generalized to modern national populations.

---

## 📜 License & Acknowledgments

- **Data Attribution**: Institute for Health Metrics and Evaluation (IHME), Global Burden of Disease (GBD), and [Our World in Data](https://ourworldindata.org/mental-health).
- **License**: Released under the [MIT License](LICENSE) for open educational and academic use.
