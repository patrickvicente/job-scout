import logging
import httpx
import asyncio
import yaml
import time

logger = logging.getLogger(__name__)

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

seek_headers = config["job_sources"]["seek"]["headers_api"]

async def scrape_seek():
    params = {
        "where": "Melbourne VIC 3000",
        "keywords": "data engineer", # space separated keywords
        "daterange": "3", # how recent: 1 = 24h, 3 = 3 days, 7 = 7d, 14 = 14d, 31 = 31d
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
        try:
            res = await client.get("https://www.seek.com.au/api/jobsearch/v5/search", params=params)
            logger.info(f"Status: {res.status_code}")
            data = res.json()
            jobs = data.get("data", [])
            if jobs:
                for job in jobs:
                    job["id"] = job.get("id")
                    job["title"] = job.get("title")
                    job["company"] = job.get("advertiser", {}).get("description")
                    job["location"] = job["locations"][0]["label"] if job.get("locations") and isinstance(job["locations"], list) and job["locations"] else None
                    job["description"] = job.get("bulletpoints")
                    job["url"] = f"https://www.seek.com.au/job/{job.get('id')}"
                    job["date_posted"] = job.get("listingDate")
                    job["category"] = job.get("classifications", {}).get("subclassification", {}).get("description")
                    job["work_type"] = job["workTypes"][0] if job.get("workTypes") and isinstance(job["workTypes"], list) and job["workTypes"] else None
                    job["work_mode"] = job.get("workArrangements", {}).get("displayText")
                    job["salary"] = job.get("salary", {}).get("displayText")
                    job["salary_type"] = job.get("salary", {}).get("salaryType")
                    job["salary_range"] = job.get("salary", {}).get("salaryRange")
                    job["salary_unit"] = job.get("salary", {}).get("salaryUnit")
                    job["salary_currency"] = job.get("salary", {}).get("salaryCurrency")
                    job["source"] = "seek"
                    job_list.append(job)
                    success_count += 1
        except Exception as e:
            logger.error("Failed to parse response", exc_info=True)
            logger.error(f"Raw response: {res.text[:300]}")
            error_count += 1

    duration = time.time() - start_time
    logger.info(f"=== SEEK API Scraper Run Finished: {success_count} success, {error_count} errors, duration: {duration:.2f} seconds ===")

if __name__ == "__main__":
    asyncio.run(scrape_seek())