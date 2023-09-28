import requests
import sys
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta

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


def convertStringDatetimeToDatetimeObj(datetimeStr):
    return datetime.datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S.%fz")


def fetchUrlDataJson(fin_year):
    url = config["fetchurls"]["GET_ACHIEVEMENT_REPORT_DATA_URL"]
    finalUrl = "{0}?finYear={1}".format(url, fin_year)
    response = requests.request("GET", finalUrl)
    return response.json()


def insertIntoTable(table_name, response_json, fin_year):
    # # write to db
    logging.info(
        "Data insertion/updation started for - {0} - fin_year - {1}".format(
            table_name, fin_year
        )
    )
    
    for data in response_json:
        data["target"] = str(data["target"])
        data["finyear"] = fin_year
        MC.insert_into_table(table_name, data)
    logging.info(
        "Data insertion/updation done for - {0} - fin_year - {1}".format(
            table_name, fin_year
        )
    )


def getAchievementReportData(fin_year):
    try:
        main_table_name = config["tables"]["achivement_report_data"]
        response_json = fetchUrlDataJson(fin_year)
        if response_json:
            # insert into main table
            insertIntoTable(main_table_name, response_json, fin_year)
        else:
            logging.info("Empty data")
    except Exception as e:
        logging.error("Error in getAchievementReportData")
        logging.error(e)


if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count == 2:
        fin_year = sys.argv[1]
        getAchievementReportData(fin_year)
    else:
        # by default
        fin_year = "2021-22"
        getAchievementReportData(fin_year)
