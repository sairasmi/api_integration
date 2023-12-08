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
"""
Function to get districtwise  STW AAE Pending Report
Created By : Ranjit Kumar Sahu
Created On :10-10-2023
"""
def getDistrictSTWPendingAAEReport(fyear):
    """
    Function to get districtwise  STW AAE Pending Report
    fyear : Finacial year
    schemename : Scheme name 
    """
    finalUrl = "{0}?appKey={1}&Fyr={2}".format('https://dbtmbdodisha.nic.in/dafp/getspSTWReportForAdapForPendingWithAAEDistWise','HGyu758hy4g5JUTi3589FR67', fyear)
    response_json = mc.fetachUrlJsonData("GET",finalUrl)
    for rdata in  response_json:
        lgd_code            = rdata['LGdCode'] 
        district_name       = rdata['DistName']
        aae_initialpending  = rdata['AAEInitialPending']
        aae_billingpending  = rdata['AAEBillingPending']
        current_datetime    = datetime.datetime.now()
        try:            
            insert_query = "INSERT IGNORE INTO t_district_stw_pending_aae_data (vch_lgd_code,vch_district_name,vch_aae_initialpending,vch_aae_billingpending,vch_finacial_year,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s, %s)"
            valdata =(lgd_code,district_name,aae_initialpending,aae_billingpending,fyear,current_datetime,current_datetime)
            cur = mc.conn.cursor()
            cur.execute(insert_query, valdata)
            mc.conn.commit()

        except Exception as e:
            mc.conn.rollback()
            logging.error("Error in insertion -t_district_stw_pending_aae_data")
            logging.error(e)
            
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_district_stw_pending_aae_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    current_fy = mc.get_current_fy()
    f_year=''
    for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getDistrictSTWPendingAAEReport(f_year)

    #getDistrictSTWPendingAAEReport()