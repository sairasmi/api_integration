import requests
import logging, configparser
from dbHelper import mysqlController

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='debug.log', filemode='w', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('./config.ini')
mc = mysqlController()  ##initialize connection to db


def fetchUrlDataJson(url):
    response = requests.request("GET", url, verify=False)
    return response.json()

# get location 
def getLocation():
    try:
        table_name = config['tables']['location']
        url = config['fetchurls']['LOCATION_DATA_URL']
        response_json = fetchUrlDataJson(url)
        response_location = response_json['location']
        # write to db
        logging.info("Data insertion started for - {0}".format(table_name))
        for data in response_location:
            mc.insert_into_table(table_name, data)
        logging.info("Data insertion done for - {0}".format(table_name))
    except Exception as e:
        logging.error('Error in get location')
        logging.error(e)

getLocation()
