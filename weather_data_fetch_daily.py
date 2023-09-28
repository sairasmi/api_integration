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

# to restrict duplicate entry composite PK set - (id and date)
def getLocationDataDaily(from_date=None, to_date=None):
    if from_date is None or to_date is None:
        # yesterday's from and to date.
        # Getting date for last 2 days, sometimes system doesn't provide data for all the location and get it after 2 days.
        from_date = datetime.date.today() - timedelta(days = 2)
        to_date = datetime.date.today() - timedelta(days = 1)
    elif from_date > to_date:
        logging.error(f"From date can't be greater than to date.")
        sys.exit()
    try:
        table_name = config['tables']['location_raw_data_daily']
        url = config['fetchurls']['LOCATION_DATA_DAILY_URL']
        location_table_name = config['tables']['location']
        # fetch location data
        location_rows = mc.fetch_from_table(location_table_name)
        # for each row fetch location data daily basis
        for row in location_rows:
            loc_id = row[0]
            finalUrl = "{0}?loc_id={1}&from={2}&to={3}".format(url, loc_id, from_date, to_date)
            print(finalUrl)
            response_json = fetchUrlDataJson(finalUrl)
            response_dailydata = response_json['dailydata']
            # # write to db
            if response_dailydata:
                logging.info("Data insertion started for - {0} - Loc_id:{1}".format(table_name, loc_id))
                for data in response_dailydata:
                    data["location_id"] = loc_id # set location id
                    data["date"] = datetime.datetime.strptime(data["date"], "%d-%m-%Y").date()  #date parse
                    mc.insert_into_table(table_name, data)
                logging.info("Data insertion done for - {0}".format(table_name))
            else:
                logging.info("Empty data for location - Loc_id:{0}".format(loc_id))
    except Exception as e:
        logging.error('Error in get location daily basis')
        logging.error(e)

if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count > 1:
        from_date = sys.argv[1]
        to_date = sys.argv[2]
        from_date_formatted = datetime.datetime.strptime(from_date, '%d-%m-%Y').date()
        to_date_formatted = datetime.datetime.strptime(to_date, '%d-%m-%Y').date()
        getLocationDataDaily(from_date,to_date)
    else:
        getLocationDataDaily()
