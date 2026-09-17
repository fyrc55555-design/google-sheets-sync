import os
import csv
import json
import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1MVubq3_rUpj_KVD4QUyxZ8cv2YrlxzugrP8kOltjto4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

service_account_info = json.loads(
    os.environ["GOOGLE_CREDENTIALS_JSON"]
)

credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)

client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(SPREADSHEET_ID)

os.makedirs("data", exist_ok=True)

for worksheet in spreadsheet.worksheets():
    rows = worksheet.get_all_values()

    filename = worksheet.title.replace("/", "_").replace("\\", "_")
    filepath = os.path.join("data", f"{filename}.csv")

    with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Exported: {worksheet.title} -> {filepath}")
