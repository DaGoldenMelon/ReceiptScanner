import gspread
import datetime
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

#Getting the workbook
sheet_id = "1I0SFtIBl-CbtIdgWOTmG026qdfksmDRHaBd8Cz_K8YQ"
workbook = client.open_by_key(sheet_id)

#Getting the current month for the worksheet name
date = datetime.datetime.now()
date_transaction = date.strftime("%B") + " Transactions"
sheet = workbook.worksheet(date_transaction)

#Findin the next available cell
existing = sheet.col_values(2)
current = len(existing) + 1
expense_range = f"B{current}:E{current}"

#Collecting data (temporary)
data = ["02.04.2026", "6,00", "KFC", "Eating Out"]

#Updating the current cell
sheet.update(range_name=expense_range, values=[data], value_input_option="USER_ENTERED")


#1. Find the current month and then match that month to the right worksheet
#2. Collect the data that wants to be added into the system
#3. Find the next free row of cells
#4. Update the cells to contain new data
