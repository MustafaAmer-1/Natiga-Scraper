import requests, csv, os
from bs4 import BeautifulSoup

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

# creds = ServiceAccountCredentials.from_json_keyfile_name('client_key.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open('all').sheet1

url = 'https://natega.cairo24.com/Home/Result'
start_seating = 1025940
current_seating = start_seating

csv_file = open('all.csv', 'w')
print("File created at: " + os.path.dirname(os.path.realpath('all.csv')))
csv_writer = csv.writer(csv_file)

def get_data(seating):
    data = {'seating_no': seating}
    row = []
    try:
        response = requests.post(url, data=data)
        print("seating " + str(seating))
        soup = BeautifulSoup(response.text, 'html.parser')
        site_seating = soup.select('#pills-tab > li:nth-child(1) > h1')[0].text
        if(site_seating != str(seating)):
            return []
        row.append(site_seating)
        edara = soup.select('#pills-tab > li:nth-child(3) > span:nth-child(2)')[0].text
        row.append(edara)
        school = soup.select('#pills-tab > li:nth-child(2) > span:nth-child(2)')[0].text
        row.append(school)
        name = soup.select('#pills-tab > li:nth-child(1) > span:nth-child(2)')[0].text
        row.append(name)
        grades = soup.select('#pills-tab > li:nth-child(2) > h1')[0].text
        row.append(grades)
        shoaba = soup.select('#pills-tab > li:nth-child(6) > span:nth-child(2)')[0].text
        row.append(shoaba)
        row.append(float(grades)*100/410)
        return row
    except:
        return row

index = 1
while(1):
    data = get_data(start_seating)
    if(data):
        csv_writer.writerow(data)

        csv_file.close()
        csv_file = open('all.csv', 'w')
        csv_writer = csv.writer(csv_file)

        # sheet.insert_row(data, index)
        index += 1
    elif(start_seating > 10000000):
        break
    start_seating += 1

csv_file.close()
print('Done!!')

'''
dir = 1
failed = 0
while(1):
    data = get_data(current_seating)
    time.sleep(0.1)
    if(data):
        writer.writerow(data)
    elif(failed < 100):
        failed += 1
    elif(dir == 1):
        current_seating = start_seating
        failed = 0
        dir = -1
    else:
        break
    current_seating += dir
'''

