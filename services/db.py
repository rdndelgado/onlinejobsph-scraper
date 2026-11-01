from supabase import create_client

from core import constants

_client = None


def get_client():
    global _client
    if _client is None:
        _client = create_client(constants.SUPABASE_URL, constants.SUPABASE_KEY)
    return _client


def filter_new_urls(urls):
    """Of the given urls, return the ones not already in the jobs table."""
    if not urls:
        return set()

    urls = list(urls)
    response = (
        get_client()
        .table(constants.JOBS_TABLE_NAME)
        .select("url")
        .in_("url", urls)
        .execute()
    )
    existing = {row["url"] for row in response.data}
    return set(urls) - existing


def insert_pending(rows):
    """rows: list of {"url": ..., "keyword": ...}"""
    if not rows:
        return
    payload = [{**row, "status": constants.STATUS_PENDING} for row in rows]
    get_client().table(constants.JOBS_TABLE_NAME).insert(payload).execute()


def fetch_unparsed(limit):
    response = (
        get_client()
        .table(constants.JOBS_TABLE_NAME)
        .select("id,url")
        .neq("status", constants.STATUS_DONE)
        .limit(limit)
        .execute()
    )
    return response.data


def update_job(row_id, fields):
    get_client().table(constants.JOBS_TABLE_NAME).update(fields).eq("id", row_id).execute()
