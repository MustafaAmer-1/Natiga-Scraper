import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

key_file_name = 'client_key.json'

creds = ServiceAccountCredentials.from_json_keyfile_name('client_key.json',scope)
client = gspread.authorize(creds)
sheet = client.open('khadiga').sheet1

row = [0, 0, 0]
sheet.insert_row(row, 1)
row = [1, 1, 1]
sheet.insert_row(row, 2)
row = [2, 2, 2]
sheet.insert_row(row, 3)
