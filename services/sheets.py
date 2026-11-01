import json

import gspread
from google.oauth2.service_account import Credentials

from core import constants

SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _sheets_client():
    creds_dict = json.loads(constants.GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SHEETS_SCOPES)
    return gspread.authorize(creds)


def read_keywords():
    sheet = _sheets_client().open_by_key(constants.KEYWORDS_SPREADSHEET_ID).worksheet(
        constants.KEYWORDS_SHEET_NAME
    )
    return [v.strip() for v in sheet.col_values(1) if v.strip()]
