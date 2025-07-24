import os
import logging
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

notion_client = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def safe_str(val):
    return str(val) if val else ""

def safe_select(val):
    return {"name": val} if val else None

def safe_multi_select(val):
    if not val:
        return []
    if isinstance(val, str):
        return [{"name": v.strip()} for v in val.split(",") if v.strip()]
    if isinstance(val, list):
        return [{"name": v} for v in val if v]
    return []

def push_job_to_notion(job: dict):
    """
    Push job to Notion
    Args:
        job: dict, job data
    Returns:
        bool, True if job was pushed to Notion, False otherwise
    """
    try:
        
        properties = {
            "Title": {"title": [{"text": {"content": str(job.get("title", ""))}}]},
            "job_id": {"rich_text": [{"text": {"content": safe_str(job.get("job_id"))}}]},
            "Company": {"rich_text": [{"text": {"content": safe_str(job.get("company"))}}]},
            "Location": {"rich_text": [{"text": {"content": safe_str(job.get("location"))}}]},
            "Notes": {"rich_text": [{"text": {"content": safe_str(job.get("description"))}}]},
            "Category": {"rich_text": [{"text": {"content": safe_str(job.get("category"))}}]},
            "Work Mode": {"select": {"name": safe_str(job.get("work_mode"))}},
            "Salary": {"rich_text": [{"text": {"content": safe_str(job.get("salary"))}}]},
            "Link": {"url": safe_str(job.get("url"))},
            "Tech Stack": {"multi_select": safe_multi_select(job.get("tech_stack"))},
            "Work Type": {"select": {"name": safe_str(job.get("work_type"))}},
            "Source": {"select": {"name": safe_str(job.get("source"))}},
            "Experience Level": {"select": {"name": safe_str(job.get("experience_level"))}},
            "Method": {"select": {"name": "Job Scout"}},
        }
        
        if job.get("date_posted"):
            properties["Date Posted"] = {
                "date": {"start": safe_str(job["date_posted"])}
            }

        # Remove keys where value is None (like select fields that are missing)
        filtered_properties = {k: v for k, v in properties.items() if v is not None}
        response = notion_client.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=filtered_properties
        )
        if response:
            logger.info(f"Successfully pushed job to Notion: {job.get('title')}")
            return True
        else:
            logger.error("Failed to push job to Notion")
            return False
    except Exception as e:
        logger.error("Failed to push job to Notion", exc_info=True)
        return False

def get_job_ids_from_notion() -> list:
    """
    Get job ids from notion
    Returns:
        list, list of job ids
    """
    notion_job_ids = []
    try:
        response = notion_client.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Source",
                "select": {"equals": "seek"}
            }
        )
    except Exception as e:
        logger.error("Failed to get jobs from notion", exc_info=True)
        return []

test_job = {
    "job_id": "12345672",
    "title": "Senior Data Engineer",
    "company": "Tech Innovators Inc.",
    "location": "Sydney NSW",
    "description": "Lead data engineering projects, mentor junior staff, and design scalable data pipelines.",
    "category": "Engineering - Data",
    "work_type": "Full time",
    "work_mode": "Hybrid",
    "salary": 150000,
    "salary_currency": "AUD",
    "source": "seek",
    "url": "https://www.seek.com.au/job/12345678",
    # "Notes" and "Method" are handled in the Notion integration, but you can add them if you want:
    # "Notes": "This is a test job for Notion integration.",
    # "Method": "Job Scout"
}

if __name__ == "__main__":
    print(push_job_to_notion(test_job))