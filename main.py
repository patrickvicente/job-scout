import logging

# Central logging configuration for the whole project
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('job_scout.log'),
        logging.StreamHandler()
    ]
)

# You can import and run your ETL or scraping scripts here
# Example:
# from src import fetch_jobs, scraper
# ...
