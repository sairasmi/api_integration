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


def convertStringDatetimeToDatetimeObj(datetimeStr):
    return datetime.datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%S.%fz')

def fetchUrlDataJson(licence_type):
    url = config['fetchurls']['GET_DEALER_DATA_URL']
    finalUrl = "{0}?appKey={1}&licenceType={2}".format(url, config['secretKeys']['APP_KEY'], licence_type)
    response = requests.request("GET", finalUrl)
    return response.json()

def insertIntoTable(table_name, response_json, licence_type):
    # # write to db
    logging.info("Data insertion/updation started for - {0} - licence_type - {1}".format(table_name, licence_type))
    for data in response_json:
        if 'districtName' not in data:
            data["districtName"] = None
        data["validTill"] = convertStringDatetimeToDatetimeObj(data["validTill"])
        data["licenceType"] = licence_type
        MC.insert_into_table(table_name, data)
    logging.info("Data insertion/updation done for - {0} - licence_type - {1}".format(table_name, licence_type))


def getDealerData(licence_type):
    try:
        main_table_name = config['tables']['dealer_main']
        response_json = fetchUrlDataJson(licence_type)
        if response_json:
            # insert into main table
            insertIntoTable(main_table_name, response_json, licence_type)
        else:
            logging.info("Empty data")
       
    except Exception as e:
        logging.error('Error in get dealer data')
        logging.error(e)


if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count == 2:
        licence_type = sys.argv[1]
        getDealerData(licence_type)
    else:
        print("Licence Type argument is missing")