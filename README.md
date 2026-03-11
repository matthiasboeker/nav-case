# nav-case

Exploratory analysis of case data from NAV.

## Setup

Requires [uv](https://github.com/astral-sh/uv) to be installed.

```bash
git clone https://github.com/matthiasboeker/nav-case.git
cd nav-case
uv sync
```

## Data

Place the file `aap_saker.csv` in the `data/` folder:

```
nav-case/
└── data/
    └── aap_saker.csv
```

## Run

```bash
uv run eksplorativ_analyse.py
```

Figures are saved to the `figures/` folder automatically.

## Project structure

```
nav-case/
├── data/                   # Input data (not tracked by git)
├── figures/                # Output plots
├── utils/
│   ├── transformations.py  # Data loading and cleaning functions
│   └── make_plots.py       # Plotting functions
├── main.py                 # Entry point
├── pyproject.toml
└── README.md
```

## Analysis

The script produces the following outputs:

- **cases_per_year.png** — Number of cases received per year
- **case_time_histogram.png** — Distribution of processing time (mottatt → vedtak)
- **reason_closed_antall.png** — Count of cases by closure reason
- **reason_closed_pie_diagram.png** — Share of cases by closure reason
- **case_time_by_status.png** — Processing time broken down by case status
- **case_time_by_fylke.png** — Processing time broken down by county
- **case_time_by_saksbehandler.png** — Processing time broken down by caseworker
- **case_time_by_aarsak.png** — Processing time broken down by closure reason