# Job Scout

**Job Scout** is a backend-focused, database engineer-oriented project for scraping and extracting job postings from online job boards (currently SEEK and Jora). It is designed as a foundation for ETL workflows, enabling scheduled data collection and further downstream processing for analytics, reporting, or personal research.

---

## Features

- **Modular Scraper**: Easily configurable selectors for different job boards via YAML.
- **ETL-Ready**: Designed for integration into scheduled ETL pipelines.
- **Async & Efficient**: Uses `httpx` and `asyncio` for fast, concurrent scraping.
- **Configurable**: All scraping parameters and selectors are managed in `src/config.yaml`.
- **Sample Data**: Includes sample JSON and TXT outputs for development and testing.

---

## Project Structure

```
job_scout/
│
├── main.py                # (Entry point, currently empty)
├── requirements.txt       # Python dependencies
└── src/
    ├── __init__.py
    ├── config.yaml        # Source-specific selectors and headers
    ├── fetch_jobs.py      # Async job search API fetcher (SEEK)
    ├── scraper.py         # HTML job detail scraper (SEEK)
    ├── seek_sample.json   # Example job data (JSON)
    └── seek_sample.txt    # Example job data (TXT)
```

---

## Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure selectors and headers

Edit `src/config.yaml` to adjust scraping targets, selectors, and HTTP headers for each job board.

### 3. Run a job search (SEEK example)

```bash
python src/fetch_jobs.py
```

### 4. Scrape job details from a URL

```bash
python src/scraper.py
```
_Edit the script to set your target job URL._

---

## ETL & Scheduling

This project is designed to be integrated into larger ETL workflows. You can schedule the scripts using cron, Airflow, or any workflow orchestrator to periodically fetch and store job data for further processing.

---

## Dependencies

- `httpx`
- `beautifulsoup4`
- `PyYAML`
- `asyncio`
- (see `requirements.txt` for full list)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Disclaimer

**This project is for personal, educational, and research purposes only.**  
Web scraping may violate the terms of service of the target websites.  
The author is not responsible for any misuse or illegal use of this code.  
Use at your own risk and always respect the robots.txt and terms of the sites you scrape. 