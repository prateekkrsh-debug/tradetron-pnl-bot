import os
import json
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


# =========================
# GOOGLE SHEETS CONNECTION
# =========================

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    creds_dict,
    scopes=scopes
)

client = gspread.authorize(credentials)


# =========================
# OPEN GOOGLE SHEET
# =========================

sheet = client.open("Tradetron Auto Tracker").worksheet("Daily P&L")


# =========================
# SAMPLE DATA
# =========================

today = datetime.now().strftime("%d-%b-%Y")

strategy_data = {
    "Strategy 1": 2500,
    "Strategy 2": -700,
    "Strategy 3": 1200
}

total = sum(strategy_data.values())


# =========================
# CREATE HEADERS
# =========================

headers = ["Date"] + list(strategy_data.keys()) + ["Total"]

existing_headers = sheet.row_values(1)

if existing_headers != headers:
    sheet.clear()
    sheet.append_row(headers)


# =========================
# APPEND DATA
# =========================

row = [today]

for value in strategy_data.values():
    row.append(value)

row.append(total)

sheet.append_row(row)

print("Google Sheet Updated Successfully")
