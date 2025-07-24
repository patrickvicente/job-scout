import logging
import asyncio
from src.fetch_jobs import fetch_seek_jobs
from src.etl.load import load_jobs_to_notion
from src.etl.transform import transform_jobs
from src.notion.notion_integration import get_job_ids_from_notion

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('job_scout.log'),
        logging.StreamHandler()
    ]
)

async def etl_pipeline():
    """
    ETL pipeline
    """

    # filter out jobs that already exist in notion
    existing_job_ids = set(get_job_ids_from_notion(source="seek"))

    # extract jobs
    jobs = await fetch_seek_jobs(job_ids=existing_job_ids) # will pass args in the future from here

    # transform jobs
    clean_jobs = transform_jobs(jobs)

    # load jobs to notion
    load_jobs_to_notion(clean_jobs)

if __name__ == "__main__":
    asyncio.run(etl_pipeline())