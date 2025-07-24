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
            "job_id": {"title": [{"text": {"content": job.get("job_id", "")}}]},
            "Title": {"rich_text": [{"text": {"content": safe_str(job.get("title", ""))}}]},
            "Company": {"rich_text": [{"text": {"content": safe_str(job.get("company"))}}]},
            "Location": {"rich_text": [{"text": {"content": safe_str(job.get("location"))}}]},
            "Notes": {"rich_text": [{"text": {"content": safe_str(job.get("description"))}}]},
            "Category": {"rich_text": [{"text": {"content": safe_str(job.get("category"))}}]},
            "Work Mode": {"select": {"name": job.get("work_mode")}} if job.get("work_mode") else None,
            "Salary": {"rich_text": [{"text": {"content": safe_str(job.get("salary"))}}]},
            "Link": {"url": safe_str(job.get("url"))},
            "Tech Stack": {"multi_select": safe_multi_select(job.get("tech_stack"))},
            "Work Type": {"select": {"name": safe_str(job.get("work_type"))}},
            "Source": {"select": {"name": safe_str(job.get("source"))}},
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

def get_job_ids_from_notion(source: str="seek") -> list:
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
                "select": {"equals": source}
            }
        )
        for result in response.get("results", []):
            job_id = result["properties"].get("job_id", {}).get("title", [{}])[0].get("plain_text", "")
            notion_job_ids.append(job_id)
        return notion_job_ids
        
    except Exception as e:
        logger.error("Failed to get jobs from notion", exc_info=True)
        return []