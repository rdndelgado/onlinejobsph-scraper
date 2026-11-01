from decouple import config

BASE_URL = "https://www.onlinejobs.ph/jobseekers/jobsearch"
SITE_ROOT = "https://www.onlinejobs.ph"
JOB_LINK_PREFIX = "/jobseekers/job/"
PAGE_SIZE = 30
CRAWL_DELAY_SECONDS = 5  # robots.txt: Crawl-delay: 5 — applies to every request this service makes
REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; onlinejobsph-scraper/1.0)"

# Render cron service — this run's own inputs, hardcoded here (per-run input comes
# from the Keywords sheet only; this is the "remaining input")
MAX_PAGE_PER_KEYWORD = 1
MAX_PARSE_PER_RUN = 50

# Google Sheets (keywords input)
GOOGLE_SERVICE_ACCOUNT_JSON = config("GOOGLE_SERVICE_ACCOUNT_JSON", default="")
KEYWORDS_SPREADSHEET_ID = config("KEYWORDS_SPREADSHEET_ID", default="")
KEYWORDS_SHEET_NAME = config("KEYWORDS_SHEET_NAME", default="Keywords")

# Supabase (jobs datastore)
SUPABASE_URL = config("SUPABASE_URL", default="")
SUPABASE_KEY = config("SUPABASE_KEY", default="")
JOBS_TABLE_NAME = config("JOBS_TABLE_NAME", default="jobs")

STATUS_PENDING = "pending"
STATUS_DONE = "done"
STATUS_FAILED = "failed"
