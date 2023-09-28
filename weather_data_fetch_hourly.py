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
mc = mysqlController()  ##initialize connection to db


def fetchUrlDataJson(url):
    response = requests.request("GET", url, verify=False)
    return response.json()

# get location half-an-hour basis
# to restrict duplicate entry composite PK set - (date, time and location_id)
def getLocationDataHourly(from_date=None, to_date=None):
    if from_date is None or to_date is None:
        # today's date and yesterday's date. Trying to get the data from yesterday to today. As sometimes we don't get immediately for all the locations.
        from_date = datetime.datetime.now().date() - timedelta(days = 1)
        to_date = datetime.datetime.now().date()
    elif from_date > to_date:
        logging.error(f"From date can't be greater than to date.")
        sys.exit()
    try:
        table_name = config['tables']['location_raw_data_half_hour']
        url = config['fetchurls']['LOCATION_DATA_HALF_AN_HOUR_URL']
        location_table_name = config['tables']['location']
        # fetch location data
        location_rows = mc.fetch_from_table(location_table_name)
        # for each row fetch location data half an hour basis
        for row in location_rows:
            loc_id = row[0]
            finalUrl = "{0}?loc_id={1}&from={2}&to={3}".format(url, loc_id, from_date, to_date)
            response_json = fetchUrlDataJson(finalUrl)
            response_rawdata = response_json['rawdata']
            # # write to db
            logging.info("Data insertion started for - {0} - Loc_id:{1}".format(table_name, loc_id))
            for data in response_rawdata:
                data["location_id"] = loc_id # set location id
                data["date"] = datetime.datetime.strptime(data["date"], "%d-%m-%Y").date()  #date parse
                mc.insert_into_table(table_name, data)
            logging.info("Data insertion done for - {0}".format(table_name))
    except Exception as e:
        logging.error('Error in get location half-an-hour basis')
        logging.error(e)

if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count > 1:
        from_date = sys.argv[1]
        to_date = sys.argv[2]
        from_date_formatted = datetime.datetime.strptime(from_date, '%d-%m-%Y').date()
        to_date_formatted = datetime.datetime.strptime(to_date, '%d-%m-%Y').date()
        getLocationDataHourly(from_date,to_date)
    else:
        getLocationDataHourly()
