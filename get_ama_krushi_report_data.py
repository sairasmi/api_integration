import sys
import json
import requests
import datetime
import logging, configparser
from dbHelper import mysqlController
from datetime import timedelta
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='debug.log', filemode='w', level=logging.DEBUG)
config = configparser.ConfigParser()
config.read('./config.ini')
mc = mysqlController()

def null_str_to_none(items):
    result = {}
    for key, value in items:
        if value == 'null':
            value = None
        result[key] = value
    return result

# get report daily
def get_specific_date_report(date=None):
    if date is None:
        # set yesterday's date if no date is passed
        date = datetime.date.today() - timedelta(days = 1)
    table_name = config['tables']['ama_krushi_daily_reports']
    try:
        logging.info(f"Trying to get the {table_name} data for {date}")
        url = config['fetchurls']['GET_AMA_KRUSHI_REPORTS_DAILY_URL']
        final_url = "{0}{1}".format(url, date)

        response = requests.request("GET", final_url, verify=False)
        response_json = response.json()
        if response_json:
            dict_str = json.dumps(response_json)
            updated_dict = json.loads(dict_str, object_pairs_hook=null_str_to_none)
            ivr_df = pd.DataFrame.from_dict(
                updated_dict["Advisory send"]["District wise ivr send"].items())
            ivr_df.columns = ['district_name', 'ivr_send_district_wise']
            onboarded_df = pd.DataFrame.from_dict(
                updated_dict["Farmer onboarded"]["Farmer Onboarded District Wise "].items())
            onboarded_df.columns = ['district_name', 'farmer_onboarded_district_wise']
            unique_farmer_df = pd.DataFrame.from_dict(
                updated_dict["Number of unique farmers getting advisory"]["District wise unique farmer"].items())
            unique_farmer_df.columns = ['district_name', 'unique_farmer_district_wise']
            intermediate = ivr_df.merge(onboarded_df, on='district_name', how='outer')
            final_df = intermediate.merge(unique_farmer_df, on='district_name', how='outer')
            final_df['advisory_calls_picked_up'] = updated_dict["Advisory calls picked up"]
            final_df['date'] = updated_dict["Advisory send"]["Active Date"]
            final_df['advisory_send'] = updated_dict["Advisory send"]["Advisory send"]
            final_df['avg_call_duration'] = updated_dict["Avg call duration"]
            final_df['farmer_onboarded'] = updated_dict["Farmer onboarded"]["Farmer Onboarded"]
            final_df['incoming_calls_on_LCC'] = updated_dict["Incoming calls on LCC"]
            final_df['no_unique_farmers_getting_advisory'] = updated_dict["Number of unique farmers getting advisory"]["Number of unique farmers getting advisory"]
            final_df['survey_calls_attempted'] = updated_dict["Survey calls attempted"]
            final_df['survey_calls_completed'] = updated_dict["Survey calls completed"]
            final_df['unique_advisories_sent'] = updated_dict["Unique advisories sent"]
            final_df['unique_advisories_sent'] = updated_dict["Unique advisories sent"]
            # write to db
            logging.info("Data insertion started for - {0}".format(table_name))
            final_df.to_sql(con=mc.engine, name='ama_krushi_daily_reports', if_exists='append', index=False)
            logging.info("Data insertion done for - {0}".format(table_name))
        else:
            logging.info('No data - {0}'.format(response_json))
    except Exception as e:
        logging.error('Error in get - {0}'.format(table_name))
        logging.error(e)

if __name__ == "__main__":
    cmd_arg_count = len(sys.argv)
    if cmd_arg_count > 1:
            input_date = sys.argv[1]
            input_date_formatted = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()
            get_specific_date_report(input_date_formatted)
    else:
        get_specific_date_report()
