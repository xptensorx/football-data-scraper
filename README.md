## football-data-scraper

Project layout:

```
/football-data-scraper
  scraper/
  config/
  output/
  logs/
  requirements.txt
  run_scraper.py
  run_historical.py
```

### Quick start (Windows PowerShell)

```bash
cd football-data-scraper
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_historical.py
python run_scraper.py
```

- **Sample CSV**: `output/sample.csv`
- **Default config**: `config/default.json`

Note: the `scraper/current_season.py` and `scraper/historical.py` modules are currently stubs that write placeholder rows. Next step is wiring real public sources per league.

### Config notes

- **`leagues[].football_data_code`**: used by `run_historical.py` to download from football-data.co.uk (e.g. `E0`, `E1`, `SP1`, `I1`, `D1`).
- **`seasons`**: can be either:
  - a dict like `{"mode":"current_and_previous","count":2}` (auto-computes `2324` style IDs), or
  - an explicit list like `["2324","2223","2122","2021","1920"]`.

