import requests

from core import constants
from helpers.dates import parse_date_updated
from services import db
from services.fetcher import fetch_page
from services.parser import parse_job
from utils.logger import get_logger

logger = get_logger(__name__)


def run_parser():
    rows = db.fetch_unparsed(limit=constants.MAX_PARSE_PER_RUN)
    logger.info("parser start rows=%s", len(rows))

    done_count = 0
    failed_count = 0

    for row in rows:
        row_id = row["id"]
        url = row["url"]

        try:
            html = fetch_page(url)
            job = parse_job(html, url)
            db.update_job(
                row_id,
                {
                    "status": constants.STATUS_DONE,
                    "html_content": html,
                    "job_id": job["job_id"],
                    "title": job["title"],
                    "description": job["description"],
                    "rate": job["rate"],
                    "job_type": job["job_type"],
                    "date_updated": parse_date_updated(job["date_updated"]),
                    "skills": job["skills"],
                    "employer_name": job["employer_name"],
                    "error_message": None,
                },
            )
            done_count += 1
            logger.info("parsed url=%s job_id=%s", url, job["job_id"])
        except requests.RequestException as exc:
            db.update_job(row_id, {"status": constants.STATUS_FAILED, "error_message": str(exc)})
            failed_count += 1
            logger.error("failed url=%s error=%s", url, exc)
        except Exception as exc:
            db.update_job(row_id, {"status": constants.STATUS_FAILED, "error_message": str(exc)})
            failed_count += 1
            logger.error("failed url=%s error=%s", url, exc)

    logger.info("parser done done=%s failed=%s", done_count, failed_count)

    return {"rows_processed": len(rows), "done": done_count, "failed": failed_count}
