import logging
from src import fetch_jobs
from src.scrape_jobs import get_seek_job_details_bs4

logger = logging.getLogger(__name__)

async def extract_jobs(params: dict) -> list:
    """
    Extract jobs from job list
    Args:
        params: dict, parameters for the job list
    Returns:
        list, list of jobs
    """
    try:
        jobs_list = await fetch_jobs(params)

        # if jobs_list and len(jobs_list) > 0:
        #     for job in jobs_list:
        #         enrich job with details
        #         job_details = get_seek_job_details_bs4(job)
        #         jobs_list.append(job_details)
                

    except Exception as e:
        logger.error("Failed to extract jobs", exc_info=True)
        return []

    return jobs_list