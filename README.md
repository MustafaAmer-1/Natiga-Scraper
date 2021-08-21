# Natiga-Scraper

web scraper program to get all the grades of the high school students.

## Overview

This program was created to run as Heroku [worker](https://devcenter.heroku.com/articles/background-jobs-queueing) app to fetch the grades of all the high school students "_Thanawya 3ama_" in Egypt. 

The script saves the fetched data in a local CSV file in addition to google spread sheet on your google drive.

## Requirements
The modules used are in [requirements.txt](https://github.com/MustafaAmer-1/Natiga-Scraper/blob/main/requirements.txt) file.
```bash
pip install -r requirements.txt
```
In order to save your fetched data on the Google cloud spreadsheet you need to make [Google Drive API](https://developers.google.com/drive) and [Google Sheets API](https://developers.google.com/sheets/api) credential. after enable these APIs save the Google drive credential key as json file named **client_key.json**, then you have to share the spreadsheet with the client email in the json file.

And finally replace your sheet ID with the one in the code.
 
However, you can only use the local CSV file to save these data which is uploaded to [file.io](https://file.io) every 10000 record fetched.

## Usage
you can set the start seating and end seating to be the range of seatings to be fetched in the code, then start the script.

It's simple as that:
```bash
python natiga.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
