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
Function to fetch api data
Cretaed By : Ranjit Kumar Sahu
Created on : 09-10-2023
"""
def fetachUrlJsonData(apiUrl):
    """
    Function to fetch api data    
     apiUrl: Api url to get the data    
    """
    app_responce = requests.request("GET",apiUrl,verify=False)
    return app_responce.json()
"""
Function to get districtwise  STW Report
Created By : Ranjit Kumar Sahu
Created On :09-10-2023
"""
def getDistrictSTWReport(fyear):
    """
    Function to get districtwise bore well and STW Report
    fyear : Finacial year
    schemename : Scheme name 
    """
    finalUrl = "{0}?appKey={1}&F_YEAR={2}".format('https://dbtmbdodisha.nic.in/dafp/getSpReportForAdapSTW','HGyu758hy4g5JUTi3589FR67', fyear)
    response_json = fetachUrlJsonData(finalUrl)
    for rdata in  response_json:
        lgd_code            = rdata['LGD_code'] 
        district_name       = rdata['DistName']
        admin_target        = rdata['AdminTarget']
        valid_application   = rdata['ValidApplication']
        goahead_generated   = rdata['GoAheadGenerated']
        project_completed   = rdata['ProjectCompleted']
        pymnt_gec           = rdata['PymntGec']
        subsidy             = rdata['Subsidy']

        current_datetime = datetime.datetime.now()
        try:            
            insert_query = "INSERT IGNORE INTO t_district_stw_data (vch_lgd_code,vch_district_name,vch_admin_target,vch_valid_application,vch_goahead_generated,vch_project_completed,vch_pymnt_gec,vch_subsidy,vch_finacial_year,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
            valdata =(lgd_code,district_name,admin_target,valid_application,goahead_generated,project_completed,pymnt_gec,subsidy,fyear,current_datetime,current_datetime)
            cur = mc.conn.cursor()
            cur.execute(insert_query, valdata)
            mc.conn.commit()

        except Exception as e:
            mc.conn.rollback()
            logging.error("Error in insertion -t_district_stw_data")
            logging.error(e)
            
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_district_stw_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    current_fy = mc.get_current_fy()
    f_year=''
    for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getDistrictSTWReport(f_year)

    #getDistrictSTWReport()