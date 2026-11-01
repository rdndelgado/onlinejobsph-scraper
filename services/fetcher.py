import time

import requests

from core import constants
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_page(url):
    # robots.txt: Crawl-delay: 5 — applies to every request, list-page or job-detail-page alike
    time.sleep(constants.CRAWL_DELAY_SECONDS)
    try:
        response = requests.get(
            url,
            headers={"User-Agent": constants.USER_AGENT},
            timeout=constants.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("request failed url=%s error=%s", url, exc)
        raise
    logger.info("request ok url=%s status=%s", url, response.status_code)
    return response.text
