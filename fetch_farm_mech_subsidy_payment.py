import sys
import requests
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='debug.log', filemode='w', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('./config.ini')
mc = mysqlController()  ##initialize connection to db


def fetchUrlDataJson(url):
    response = requests.request("GET", url, verify=False)
    return response.json()

def get_subsidy_payment_data():
    try:
        # Get the required Variables
        table_name = config['tables']['farm_mech_subsidy_payment_table']
        url = config['fetchurls']['FARM_MECH_SUBSIDY_PAYMENT_URL']
        # Extract data from API
        finalUrl = "{0}?apiKey={1}".format(url, config['secretKeys']['FARM_MECH_SUBSIDY_PAYMENT_API_KEY'])
        logging.info(f"Final API URL: {finalUrl}")
        response_json = fetchUrlDataJson(finalUrl)
        
        # Perform Transformation if required
        if response_json:
            logging.info(f"Data insertion started for Table {table_name}")
            for data in response_json:
                # Load data into target database table
                if data["PaymentTransDt"]:
                    data["PaymentTransDt"] = datetime.strptime(data["PaymentTransDt"], '%Y-%m-%dT%H:%M:%S.%f%z')
                if data["Bill_Crt_Dt"]:
                    data["Bill_Crt_Dt"] = datetime.strptime(data["Bill_Crt_Dt"], '%Y-%m-%dT%H:%M:%S.%f%z')
                if data["mfgapprovedDt"]:
                    data["mfgapprovedDt"] = datetime.strptime(data["mfgapprovedDt"], '%Y-%m-%dT%H:%M:%S.%f%z')
                if data["eeAppdt"]:
                    data["eeAppdt"] = datetime.strptime(data["eeAppdt"], '%Y-%m-%dT%H:%M:%S.%f%z')
                if data["BankReqDt"]:
                    data["BankReqDt"] = datetime.strptime(data["BankReqDt"], '%Y-%m-%dT%H:%M:%S.%f%z')
                mc.insert_into_table(table_name, data)
            logging.info("Data insertion done for - {0}".format(table_name))
        else:
            logging.info(f"Empty data for {table_name}")
    except Exception as e:
        logging.error(f"Error in getting data for {table_name} from API {finalUrl}")
        logging.error(e)

if __name__ == "__main__":
    get_subsidy_payment_data()
