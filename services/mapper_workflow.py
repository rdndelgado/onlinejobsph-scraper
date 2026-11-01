from core import constants
from services import db, sheets
from services.search import search_keyword
from utils.logger import get_logger

logger = get_logger(__name__)


def run_mapper():
    keywords = sheets.read_keywords()
    logger.info("mapper start keywords=%s", len(keywords))

    keyword_links = {}
    all_links = set()
    for keyword in keywords:
        links = search_keyword(keyword, max_pages=constants.MAX_PAGE_PER_KEYWORD)
        keyword_links[keyword] = links
        all_links.update(links)
        logger.info("keyword=%s links_found=%s", keyword, len(links))

    new_links = db.filter_new_urls(all_links)
    logger.info("mapper new_links=%s of total_links=%s", len(new_links), len(all_links))

    rows = []
    seen = set()
    for keyword, links in keyword_links.items():
        for link in links:
            if link in new_links and link not in seen:
                rows.append({"url": link, "keyword": keyword})
                seen.add(link)

    db.insert_pending(rows)
    logger.info("mapper done inserted=%s", len(rows))

    return {"keywords_processed": len(keywords), "links_found": len(all_links), "inserted": len(rows)}
