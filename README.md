# Crime Data Analysis — Los Angeles

Exploratory data analysis of crime incidents in Los Angeles using pandas, seaborn, and matplotlib. The script answers questions like which demographics and areas are most affected, when crimes occur, what percentage are unresolved, and how weapon usage breaks down.

## Dataset

The data is **not included** in this repository (standard practice is to keep datasets out of source control).

Download `crimes.csv` from Kaggle:
**https://www.kaggle.com/datasets/beshoyatefadel/analyzing-crime-in-los-angeles**

After downloading, place the file at:

```
Crime Data Analysis/
└── data/
    └── crimes.csv
```

## Setup

Clone the repo and install dependencies (Python 3.9+ recommended):

```bash
git clone <your-repo-url>
cd "Crime Data Analysis"

# Create a virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
python crimes_analysis.py
```

The script will:
- Print column types, resolution rates, and weapon-usage stats to the console.
- Open a series of matplotlib windows with plots covering victim demographics, area hotspots, time-of-day patterns, monthly trends, and crime-type breakdowns.

## Key Findings

- **~82%** of crimes in the dataset are still unresolved.
- **~60%** of recorded crimes involved a weapon.
- At least **40%** of crimes in each area occur at night (18:00–03:59).
- Crime distribution shows clear hourly patterns and area-level hotspots.

## Project Structure

```
Crime Data Analysis/
├── crimes_analysis.py     # Main analysis script
├── requirements.txt       # Python dependencies
├── .gitignore             # Excludes data, venvs, caches
├── README.md              # This file
└── data/                  # (gitignored) Place crimes.csv here
```

## Dependencies

- pandas
- numpy
- seaborn
- matplotlib

See `requirements.txt` for version specifiers.
