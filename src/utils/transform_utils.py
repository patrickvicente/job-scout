from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_date(value, job_title):
    try:
        if value:
            return datetime.strptime(value.strip(), "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        else:
            return ""
    except Exception:
        logger.error(f"Failed to parse date: {value} for job: {job_title}")
        return ""

def parse_salary(value, job_title):
    try:
        if value and isinstance(value, int):
            return value
        else:
            salary = value.split(" ")[0].replace("$", "").replace(",", "").strip()
            if "k" in salary.lower():
                return int(salary.replace("k", "").split("-")[0].strip()) * 1000
            if "-" in salary:
                return int(salary.split("-")[0].strip())
            if "." in salary:
                return int(float(salary))
            if salary.isdigit():
                return int(salary)
            else:
                logger.error(f"Failed to parse salary: {value} for job: {job_title}")
                return None

    except Exception:
        logger.error(f"Failed to parse salary: {value} for job: {job_title}")
        return ""