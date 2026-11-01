from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from core import constants
from services.fetcher import fetch_page
from utils.logger import get_logger

logger = get_logger(__name__)


def build_search_url(keyword, offset):
    query = urlencode({"jobkeyword": keyword})
    if offset:
        return f"{constants.BASE_URL}/{offset}?{query}"
    return f"{constants.BASE_URL}?{query}"


def parse_search_result_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(constants.JOB_LINK_PREFIX):
            links.add(constants.SITE_ROOT + href)
    return links


def search_keyword(keyword, max_pages):
    all_links = set()
    for page in range(max_pages):
        offset = page * constants.PAGE_SIZE
        url = build_search_url(keyword, offset)

        try:
            html = fetch_page(url)
        except requests.RequestException:
            logger.error("keyword=%s stopped early at offset=%s due to request failure", keyword, offset)
            break

        page_links = parse_search_result_links(html)
        logger.info("keyword=%s offset=%s links_found=%s", keyword, offset, len(page_links))

        if not page_links:
            break

        all_links.update(page_links)

    return all_links
