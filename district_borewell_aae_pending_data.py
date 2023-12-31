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
Function to get districtwise bore well AAE pending data
Created By : Ranjit Kumar Sahu
Created On :06-10-2023
"""
def getDistrictBorewellAEEPendingData(fyear,schemename):
    """
    Function to get districtwise bore well AAE pending data
    fyear : Finacial year
    schemename : Scheme name 
    """
    finalUrl = "{0}?appKey={1}&Fyr={2}&scheme={3}".format('https://dbtmbdodisha.nic.in/dafp/getspBWLReportForAdapForPendingWithAAEDistWise','LKyu758hy4g5JUTi3589FR67', fyear,schemename)
    response_json = mc.fetachUrlJsonData("GET",finalUrl)
    for rdata in  response_json:
        dist_name           = rdata['DistName']
        lgd_code            = rdata['LGdCode'] 
        aae_initialpending  = rdata['AAEInitialPending']
        aae_billingpending  = rdata['AAEBillingPending']
        current_datetime = datetime.datetime.now()
        try:            
            insert_query = "INSERT IGNORE INTO t_district_borewell_aae_pendingapplication_data (vch_lgd_code,vch_district_name,vch_aae_initialpending,vch_aae_billingpending,vch_finacial_year,vch_scheme_name,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
            valdata =(lgd_code,dist_name,aae_initialpending,aae_billingpending,fyear,schemename,current_datetime,current_datetime)
            cur = mc.conn.cursor()
            cur.execute(insert_query, valdata)
            mc.conn.commit()

        except Exception as e:
            mc.conn.rollback()
            logging.error("Error in insertion -t_district_borewell_aae_pendingapplication_data")
            logging.error(e)
 
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_district_borewell_aae_pendingapplication_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    current_fy = mc.get_current_fy()
    f_year=''
    scheme_data =('RKVY','SP')
    for j in scheme_data:
        for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getDistrictBorewellAEEPendingData(f_year,j)

    #getDistrictBorewellAEEPendingData()