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

