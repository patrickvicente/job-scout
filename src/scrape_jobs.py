import logging
import httpx
import yaml
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

with open("src/config.yaml") as f:
    config = yaml.safe_load(f)

def get_seek_job_details_bs4(job: dict) -> dict:
    headers = config["job_sources"]["seek"]["headers_scrape"]
    try:
        response = httpx.get(job_url, headers=headers, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch page: {e}")
        return {"error": f"Failed to fetch page: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("[data-automation='job-detail-title']")
    company = soup.select_one("[data-automation='advertiser-name']")
    location = soup.select_one("[data-automation='job-detail-location']")
    description = soup.select_one("[data-automation='jobAdDetails']")

    job_data = {
        "title": title.get_text(strip=True) if title else None,
        "company": company.get_text(strip=True) if company else None,
        "location": location.get_text(strip=True) if location else None,
        "description": description.get_text(strip=True) if description else None,
        "source": job_url,
    }
    logger.info(f"Scraped job: {job_data['title']} at {job_data['company']}")
    return job_data

if __name__ == "__main__":
    start_time = time.time()
    logger.info("=== Job Scraper Run Started ===")
    url = "https://www.seek.com.au/job/2561585"
    job = get_seek_job_details_bs4(url)
    error_count = 0
    success_count = 0
    if "error" in job:
        logger.error(job["error"])
        error_count += 1
    else:
        logger.info(f"Job details: {job}")
        success_count += 1
    duration = time.time() - start_time
    logger.info(f"=== Job Scraper Run Finished: {success_count} success, {error_count} errors, duration: {duration:.2f} seconds ===")

    properties = job_id {
        'id': 'title', 
        'type': 'title', 
        'title': [
            {'type': 'text', 
            'text': {'content': 'Senior Data Engineer', 'link': None}, 
            'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 
            'plain_text': 'Senior Data Engineer', 'href': None}]}