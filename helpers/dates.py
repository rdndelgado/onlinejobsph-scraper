from datetime import datetime, timezone

from utils.logger import get_logger

logger = get_logger(__name__)


def parse_date_updated(raw_text):
    """Site gives a date-only string like 'Oct 19, 2026', no time component."""
    if not raw_text:
        return None
    try:
        parsed = datetime.strptime(raw_text.strip(), "%b %d, %Y")
        return parsed.replace(tzinfo=timezone.utc).isoformat()
    except ValueError:
        logger.warning("unparseable date_updated value=%r", raw_text)
        return None
