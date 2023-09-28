import sys
import requests
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='debug.log', filemode='w', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('./config.ini')
mc = mysqlController()  ##initialize connection to db


def fetchUrlDataJson(url):
    response = requests.request("GET", url, verify=False)
    return response.json()

def get_PDI_data():
    try:
        # Get the required Variables
        table_name = config['tables']['farm_mech_PDI_data_table']
        url = config['fetchurls']['FARM_MECH_PDI_DATA_URL']
        # Extract data from API
        finalUrl = "{0}?apiKey={1}".format(url, config['secretKeys']['FARM_MECH_PDI_DATA_API_KEY'])
        logging.info(f"Final API URL: {finalUrl}")
        response_json = fetchUrlDataJson(finalUrl)
        
        # Perform Transformation if required
        if response_json:
            logging.info(f"Data insertion started for Table {table_name}")
            for data in response_json:
                data["block_name"] = data["UserName"].split("_")[1]
                # Load data into target database table
                mc.insert_into_table(table_name, data)
            logging.info("Data insertion done for - {0}".format(table_name))
        else:
            logging.info(f"Empty data for {table_name}")
    except Exception as e:
        logging.error(f"Error in getting data for {table_name} from API {finalUrl}")
        logging.error(e)

if __name__ == "__main__":
    get_PDI_data()
