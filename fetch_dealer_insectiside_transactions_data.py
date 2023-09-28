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


def fetchUrlDataJson(year, month):
    url = config['fetchurls']['GET_DEALER_INSECTISIDES_TRANSACTIONS_DATA_URL']
    finalUrl = "{0}?appKey={1}&year={2}&month={3}".format(url, config['secretKeys']['APP_KEY'], year, month)
    response = requests.request("GET", finalUrl)
    return response.json()

def getDealerByLicenceNo(licence_no):
    results = MC.get_dealer_by_licence_no(licence_no)
    if results:
        for data in results:
            return data
    else:
        return None

def getInsectisidesByTechnicalName(technical_name):
    results = MC.get_insectisides_by_technical_name(technical_name)
    if results:
        for data in results:
            return data
    else:
        return None

def insertIntoTable(table_name, response_json, year, month):
    # # write to db
    logging.info("Data insertion started for - {0}".format(table_name))
    for data in response_json:
        data["year"] = year
        data["month"] = month
        # print('licenceNo --> ', data['licenceNo'])
        # print(getDealerByLicenceNo(data['licenceNo']))
        # print('technicalName --> ', data['technicalName'])
        # print(getInsectisidesByTechnicalName(data['technicalName']))
        data["dealerId"] = getDealerByLicenceNo(data['licenceNo'])
        data["insectisideId"] = getInsectisidesByTechnicalName(data['technicalName'])
        MC.insert_into_table(table_name, data)
    logging.info("Data insertion done for - {0}".format(table_name))
    

def deleteDataByMonthYear(table_name, year, month):
    MC.delete_data_on_dit_by_year_month(year, month)
    logging.info("Data deleted from table Done - {0} - for month - {1} - year - {2}".format(table_name, year, month))


def getCurrentYearMonth():
    currentDate = datetime.datetime.now()
    year = currentDate.year
    month = currentDate.month
    return [year, month]


def getDealerInsectisidesTransactionsData(year=None, month=None):
    try:
        print(year, month)
        if not year and month:
            # get current month and year
            [year, month] = getCurrentYearMonth()
            print(year, month)

        dit_table_name = config['tables']['dealer_insectiside_transactions']
        response_json = fetchUrlDataJson(year, month)
        if response_json:
            #delete data
            deleteDataByMonthYear(dit_table_name, year, month)

            #insert into main table
            insertIntoTable(dit_table_name, response_json, year, month)
            
        else:
            logging.info("Empty data")
       
    except Exception as e:
        logging.error('Error in get dealer insectisides transaction data')
        logging.error(e)


if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count == 3:
        year = sys.argv[1]
        month = sys.argv[2]
        getDealerInsectisidesTransactionsData(year, month)
    else:
        getDealerInsectisidesTransactionsData()