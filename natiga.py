import requests, csv, subprocess, time
from bs4 import BeautifulSoup
from json import loads

# multithreading
from queue import Queue
from threading import Thread, Lock

# google spreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

start_seating = 1339993 # set the start_seating 
end_seating = 10000000 # set the end_seating
THREADS_NUM = 10

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

creds = ServiceAccountCredentials.from_json_keyfile_name('client_key.json', scope) # put your credentials in a json file named client_key.json
client = gspread.authorize(creds)

SHEET_ID = '1PYewJ4oMt7-DoijLhseMGttaAxypJXa32ddIBDzxFJ4' # put your sheet id here

url = 'https://natega.cairo24.com/Home/Result'

csv_file = open('grades.csv', 'a')
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
        while self.ss < end_seating:
            row = get_data(self.ss)
            self.ss += THREADS_NUM
            if(row):
                addToQueue(row)

def is_threads_alive():
    for thread in threads:
        if thread.is_alive():
            return True
    return False

threads = []
for i in range(THREADS_NUM):
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
    
    if(index % 10000 == 0):
        csv_file.flush()
        res = subprocess.check_output('curl -F "file=@grades.csv" https://file.io', shell=True)
        link = loads(res)['link']
        print("The file uploaded at "  + link)
        r_f = open('grades.csv', 'r')
        client.import_csv(SHEET_ID, r_f.read().encode('utf-8'))        
        r_f.close()

csv_file.close()
print('\n---------------------------------------------Done!!---------------------------------------------\n')

res = subprocess.check_output('curl -F "file=@grades.csv" https://file.io', shell=True)

csv_file = open('grades.csv', 'r')
client.import_csv(SHEET_ID, csv_file.read().encode('utf-8'))
csv_file.close()

while(1):
    print("The file uploaded at "  + link)
    time.sleep(10)
