# onlinejobsph-scraper

Scheduled job that searches [onlinejobs.ph](https://www.onlinejobs.ph) for a set of keywords and stores parsed job details in Supabase.

Runs as a scheduled GitHub Actions workflow, every 12 hours. No web server, no public API — see `architecture.md` for details.

## How it works

Each run does two phases, sequentially, in one process:

1. **Mapper** — reads search keywords from a Google Sheet, searches onlinejobs.ph for each, dedupes the found job URLs against what's already in Supabase, inserts the new ones as `status = pending`.
2. **Parser** — reads rows where `status != done`, fetches each job's detail page live, parses it, writes the result back to the same row (`status = done`, or `status = failed` with `error_message` if something broke — failed rows retry on the next run).

All requests to onlinejobs.ph wait 5s first (its `robots.txt` sets `Crawl-delay: 5`).

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in the values below
```

### Environment variables

| var | purpose |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google service-account credentials (single-line JSON), shared with the Keywords spreadsheet |
| `KEYWORDS_SPREADSHEET_ID` | Google Sheet ID holding the keywords list |
| `KEYWORDS_SHEET_NAME` | tab name in that sheet (default `Keywords`) |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase secret/service key (server-side, bypasses RLS) |
| `JOBS_TABLE_NAME` | table name (default `jobs`) |

The Keywords sheet is a single column of search terms — edit it directly to change what gets searched, no deploy needed.

`core/constants.py` holds the rest of this run's inputs that aren't meant to be edited per-run (`MAX_PAGE_PER_KEYWORD`, `MAX_PARSE_PER_RUN`, crawl-delay, etc).

### Database

Run this once in Supabase's SQL editor:

```sql
create table if not exists jobs (
  id bigint generated always as identity primary key,
  url text not null unique,
  keyword text,
  status text not null default 'pending',  -- pending | done | failed
  html_content text,
  job_id text,
  title text,
  description text,
  rate text,
  job_type text,
  date_updated timestamptz,
  skills jsonb,
  employer_name text,
  error_message text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists jobs_status_idx on jobs (status);
```

## Run it

```
python3 main.py
```

## Deploy

`.github/workflows/scrape.yml` defines the schedule (`cron: "0 */12 * * *"`, every 12 hours) plus a manual `workflow_dispatch` trigger. Push this repo to GitHub, then set each environment variable above as a repo secret (Settings → Secrets and variables → Actions) under the same names — the workflow reads them from `secrets.*`.
