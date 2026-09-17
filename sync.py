import os
import csv
import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1MVubq3_rUpj_KVD4QUyxZ8cv2YrlxzugrP8kOltjto4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

credentials = Credentials.from_service_account_info(
    {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_PROJECT_ID"],
        "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "token_uri": "https://oauth2.googleapis.com/token",
    },
    scopes=SCOPES,
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
