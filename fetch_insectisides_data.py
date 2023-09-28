import requests
import sys
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='debug.log', filemode='w', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('./config.ini')
MC = mysqlController()  ##initialize connection to db


def fetchUrlDataJson():
    url = config['fetchurls']['GET_INSECTICIDE_DATA_URL']
    finalUrl = "{0}?appKey={1}".format(url, config['secretKeys']['APP_KEY'])
    response = requests.request("GET", finalUrl)
    return response.json()

def insertIntoTable(table_name, response_json):
    # # write to db
    logging.info("Data insertion started for - {0}".format(table_name))
    for data in response_json:
        if 'percentage' not in data.keys():
            data["percentage"] = None
        MC.insert_into_table(table_name, data)
    logging.info("Data insertion done for - {0}".format(table_name))

def getInsectisideData():
    try:
        main_table_name = config['tables']['insecticide_main']
        response_json = fetchUrlDataJson()
        if response_json:
            #insert into main table
            insertIntoTable(main_table_name, response_json)
            
        else:
            logging.info("Empty data")
       
    except Exception as e:
        logging.error('Error in get insectiside data')
        logging.error(e)


if __name__ == "__main__":
    getInsectisideData()
    