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
# sheet = client.open('all').sheet1

url = 'https://natega.cairo24.com/Home/Result'
start_seating = 1336490
current_seating = start_seating

csv_file = open('all_thread.csv', 'a')
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

def addToQueue(row):
    lock.acquire()
    queue.put(row)
    lock.release()

class ProcessThread(Thread):
    def __init__(self,ss):
        Thread.__init__(self)
        self.ss = ss
    
    def run(self):
        while self.ss < 10000000:
            row = get_data(self.ss)
            self.ss += 10
            if(row):
                addToQueue(row)

def is_threads_alive():
    for thread in threads:
        if thread.is_alive():
            return True
    return False

threads = []
for i in range(10):
    threads.append(ProcessThread(start_seating+i))

for thread in threads:
    thread.start()

lock = Lock()
queue = Queue()

index = 1
while(is_threads_alive()):
    if(queue.empty()):
        continue
    lock.acquire()
    row = queue.get()
    lock.release()
    
    csv_writer.writerow(row)
    index += 1
    
    if(index % 2000 == 0):
        csv_file.flush()
        os.system('curl -F "file=@all_thread.csv" https://file.io')

csv_file.close()
print('\n---------------------------------------------Done!!---------------------------------------------\n')

res = os.system('curl -F "file=@all_thread.csv" https://file.io')

csv_file = open('all_thread.csv', 'r')
client.import_csv('1PYewJ4oMt7-DoijLhseMGttaAxypJXa32ddIBDzxFJ4', csv_file.read().encode('utf-8'))

while(1):
    print(res)
    time.sleep(10)
