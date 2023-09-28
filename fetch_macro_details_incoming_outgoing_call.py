import requests
import sys
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta
import json

import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    filename="debug.log",
    filemode="w",
    level=logging.DEBUG,
)
config = configparser.ConfigParser()
config.read("./config.ini")
MC = mysqlController()  ##initialize connection to db


def fetchUrlDataJson(date):
    url = config["fetchurls"]["MACRO_DETAILS_INCOMING_OUTGOING_CALL_URL"]
    finalUrl = f"{url}{date}"
    response = requests.request("GET", finalUrl)
    response_data = response.text
    response_json = json.loads(response_data)
    data = response_json["data"]
    return data


def insertIntoTable(table_name, response_json, date):
    logging.info(f"Data load started - {table_name} - {date}")
    for data in response_json:
        data = {key.replace(" ","_"): value for key, value in data.items()}
        MC.insert_into_table(table_name, data)
    logging.info(
        f"Data insertion/updation done for - {table_name} - date - {date}"
    )


def getAPIData(date):
    try:
        main_table_name = config["tables"]["macro_details_incoming_outgoing_call"]
        response_json = fetchUrlDataJson(date)
        if response_json:
            # insert into main table
            insertIntoTable(main_table_name, response_json, date)
        else:
            logging.info("Empty data")
    except Exception as e:
        logging.error("Error in getting data from API")
        logging.error(e)


if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count > 1:
        input_date = sys.argv[1]
        input_date_formatted = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()
        getAPIData(input_date_formatted)
    else:
        # by default calling the API for previous day
        input_date_formatted = datetime.date.today() - timedelta(days = 1)
        getAPIData(input_date_formatted)
