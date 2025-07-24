from dotenv.main import logger

from src.notion.notion_integration import push_job_to_notion


def load_jobs_to_notion(jobs: list) -> int: # return number of jobs loaded
    """
    Load jobs to Notion
    Args:
        jobs: list, list of jobs
    Returns:
        int, number of jobs loaded
    """
    logger.info(f"Loading {len(jobs)} jobs to Notion")
    success_count = 0
    error_count = 0
    
    for job in jobs:
        is_success = push_job_to_notion(job)
        if is_success: 
            success_count += 1
        else:
            error_count += 1

    logger.info(f"Successfully loaded {success_count} jobs to Notion")
    logger.info(f"Failed to load {error_count} jobs to Notion")
    return success_count