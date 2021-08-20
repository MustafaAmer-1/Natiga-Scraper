import requests, csv, os, time
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread, Lock

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

creds = ServiceAccountCredentials.from_json_keyfile_name('client_key.json', scope)
client = gspread.authorize(creds)

url = 'https://natega.cairo24.com/Home/Result'
start_seating = 1334174
current_seating = start_seating

csv_file = open('test.csv', 'a')
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

lock = Lock()

def addToQueue(row):
    lock.acquire()
    queue.put(row)
    lock.release()

class ProcessThread(Thread):
    def __init__(self,ss, ee):
        Thread.__init__(self)
        self.ss = ss
        self.ee = ee
    
    def run(self):
        while self.ss <= self.ee:
            row = get_data(self.ss)
            self.ss += 1
            if(row):
                addToQueue(row)

queue = Queue()

t1 = ProcessThread(1334174, 1334184)
t2 = ProcessThread(1334185, 1334195)
t3 = ProcessThread(1334196, 1334206)

t1.start()
t2.start()
t3.start()

while t1.is_alive() or t2.is_alive() or t3.is_alive():
    if(queue.empty()):
        continue
    lock.acquire()
    row = queue.get()
    lock.release()
    csv_writer.writerow(row)

csv_file.close()
csv_file = open('test.csv', 'r')
client.import_csv('1BxzLrU3bIs-obEHOk8NGOJlDXOgHUy8Se2jAHvOuG6g', csv_file.read().encode('utf-8'))

print('\n---------------------------------------------Done!!---------------------------------------------\n')

# res = os.system('curl -F "file=@all_again.csv" https://file.io')

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

