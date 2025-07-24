import json
import logging
import httpx
import asyncio
import yaml
import time

logger = logging.getLogger(__name__)

def safe_get(d, path, default=None):
    """
    Safely get a nested value from a dict/list structure.
    path: list of keys/indices, e.g. ['classifications', 0, 'subclassification', 'description']
    """
    for key in path:
        if isinstance(d, dict):
            d = d.get(key)
        elif isinstance(d, list) and isinstance(key, int):
            if len(d) > key:
                d = d[key]
            else:
                return default
        else:
            return default
        if d is None:
            return default
    return d

with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)



async def fetch_seek_jobs(custom_params:dict=None, job_ids:set=None, limit:int=20) -> list:
    """
    Scrape jobs from seek.com.au
    Args:
        custom_params: dict, custom parameters for the seek api. 
            If not provided, the default parameters will be used in config.yaml
        job_ids: set, set of job ids to filter out.
        limit: int, limit the number of jobs to scrape.
    Returns:
        list, list of jobs
    """
    seek_headers = config["job_sources"]["seek"]["headers_api"]
    if custom_params:
        params = custom_params
    else:
        params = config["job_sources"]["seek"]["api_params"]
        
    params = {
        "page": 1,
        "where": "Melbourne VIC 3000",
        "keywords": "BUSINESS DEVELOPMENT MANAGER", # space separated keywords
        "daterange": "7", # how recent: 1 = 24h, 3 = 3 days, 7 = 7d, 14 = 14d, 31 = 31d
        "worktype": "242", # 242 = full-time, 243 = part-time, 244 = casual, 245 = contract, 246 = internship
        "workarrangement": "1", # 1 = remote, 2 = hybrid, 3 = on-site
        "salarytype": "annual", # annual, hourly
        "salaryrange": "80000-200000", # salary range
    }
    job_list = []
    error_count = 0
    success_count = 0
    start_time = time.time()

    logger.info("=== SEEK API Scraper Run Started ===")
    async with httpx.AsyncClient(headers=seek_headers) as client:
        while True:
            try:
                res = await client.get("https://www.seek.com.au/api/jobsearch/v5/search", params=params, timeout=10.0)
                logger.info(f"Status: {res.status_code}")
                data = res.json()
                jobs = data.get("data", [])
                if not jobs:
                    logger.error("No jobs found")
                    return
                
                for job in jobs:
                    if job.get("id") in job_ids:
                        logger.info(f"Skipping job: {job.get('id')} (duplicated)")
                        continue
                    job_dict = {}
                    try:
                        job_dict["job_id"] = job.get("id")
                        job_dict["title"] = job.get("title")
                        job_dict["company"] = safe_get(job, ["advertiser", "description"])
                        job_dict["location"] = safe_get(job, ["locations", 0, "label"])
                        job_dict["description"] = job.get("bulletPoints") # list of strings
                        job_dict["url"] = f"https://www.seek.com.au/job/{job.get('id')}"
                        job_dict["date_posted"] = job.get("listingDate")
                        job_dict["category"] = safe_get(job, ["classifications", 0, "subclassification", "description"])
                        job_dict["work_type"] = safe_get(job, ["workTypes", 0])
                        job_dict["work_mode"] = safe_get(job, ["workArrangements", "displayText"])
                        job_dict["salary"] = job.get("salaryLabel")
                        job_dict["salary_currency"] = safe_get(job, ["salary", "salaryCurrency"])
                        job_dict["source"] = "seek"
                        job_list.append(job_dict)
                        success_count += 1
                        logger.info(f"Added job: {job_dict['title']}")

                    except Exception as e:
                        logger.error(f"Failed to parse job:", exc_info=True)
                        logger.error(f"Raw job: {job}")
                        error_count += 1
                        continue
                    if len(job_list) == limit:
                        break
                if len(job_list) == limit:
                    break

                params["page"] += 1
                logger.info(f"Page: {params['page']}")
                await asyncio.sleep(1)
        
            except Exception as e:
                logger.error("Failed to parse response", exc_info=True)
                logger.error(f"Raw response: {res.text[:300]}")
                error_count += 1
                continue
                
        return job_list
                
    duration = time.time() - start_time
    logger.info(f"=== SEEK API Scraper Run Finished: {success_count} success, {error_count} errors, duration: {duration:.2f} seconds ===")