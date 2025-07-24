import json
import logging
from src.utils.transform_utils import parse_date, parse_salary

logger = logging.getLogger(__name__)

def transform_jobs(jobs_list: list) -> list:
    """
    Transform jobs list to a list of dictionaries
    Args:
        jobs_list: list, list of jobs
    Returns:
        list, list of dictionaries
    """
    if not jobs_list or len(jobs_list) == 0:
        logger.error("No jobs to transform")
        return []
    
    if not isinstance(jobs_list, list):
        logger.error(f"This is not a list: {jobs_list}")
        return []

    cleaned_jobs_list = []
    try:
        for job in jobs_list:
            job_dict = {}
            for key, value in job.items():
                if value is None:
                    job_dict[key] = ""
                elif isinstance(value, list):
                    job_dict[key] = ", ".join(str(v) for v in value).strip()
                elif isinstance(value, dict):
                    job_dict[key] = json.dumps(value).strip()
                elif isinstance(value, str):
                    job_dict[key] = value.strip()
                else:
                    job_dict[key] = value
                    
                if key == "date_posted":
                    job_dict[key] = parse_date(value, job_dict.get("title", ""))
                if key == "salary" and value:
                    job_dict[key] = parse_salary(value, job_dict.get("title", ""))

            cleaned_jobs_list.append(job_dict)

    except Exception as e:
        logger.error("Failed to transform jobs", exc_info=True)
        return []
    return cleaned_jobs_list