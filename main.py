import logging
import asyncio
from src.etl.transform import transform_jobs
from src.fetch_jobs import scrape_seek

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('job_scout.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    sample_jobs = asyncio.run(scrape_seek())
    transform_jobs(sample_jobs)