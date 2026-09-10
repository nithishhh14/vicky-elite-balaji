import gspread

SHEET_ID = "10-5n2epVeVhn9_ecRGd9xHpvmHkJ5qdwlGoHdMumwKg"
HEADERS = [
    "Contractor Name",
    "Phone Number",
    "City Hub",
    "Source Platform",
    "Source Website",
    "Client Details",
    "Custom Pitch Summary",
    "Sourced At",
]
ws = gspread.service_account(filename="google_creds.json").open_by_key(SHEET_ID).sheet1
ws.clear()
ws.update(values=[HEADERS], range_name="A1:H1")
print("sheet cleared to headers only")
