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
Function to get districtwise  STW Report
Created By : Ranjit Kumar Sahu
Created On :09-10-2023
"""
def getDistrictSTWPendingReport(fyear):
    """
    Function to get districtwise bore well and STW Pending Report
    fyear : Finacial year
    schemename : Scheme name 
    """
    finalUrl = "{0}?appKey={1}&Fyr={2}".format('https://dbtmbdodisha.nic.in/dafp/getSTWReportForAdapForPendingApplication','HGyu758hy4g5JUTi3589FR67', fyear)
    response_json = mc.fetachUrlJsonData("GET",finalUrl)
    for rdata in  response_json:
        lgd_code            = rdata['Lgd_code'] 
        district_name       = rdata['DistName']
        aao_initialpending  = rdata['AAOInitialPending']
        goahead_pending     = rdata['GoaheadPending']
        current_datetime = datetime.datetime.now()
        try:            
            insert_query = "INSERT IGNORE INTO t_district_stw_pending_data (vch_lgd_code,vch_district_name,vch_aao_initialpending,vch_goahead_pending,vch_finacial_year,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s, %s)"
            valdata =(lgd_code,district_name,aao_initialpending,goahead_pending,fyear,current_datetime,current_datetime)
            cur = mc.conn.cursor()
            cur.execute(insert_query, valdata)
            mc.conn.commit()

        except Exception as e:
            mc.conn.rollback()
            logging.error("Error in insertion -t_district_stw_pending_data")
            logging.error(e)
            
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_district_stw_pending_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    current_fy = mc.get_current_fy()
    f_year=''
    for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getDistrictSTWPendingReport(f_year)

    #getDistrictSTWPendingReport()