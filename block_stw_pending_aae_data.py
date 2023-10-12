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
Created on : 10-10-2023
"""
def fetachUrlJsonData(apiUrl):
    """
    Function to fetch api data    
     apiUrl: Api url to get the data    
    """
    app_responce = requests.request("GET",apiUrl,verify=False)
    return app_responce.json()
"""
Function to get districtwise bore well pending data
Created By : Ranjit Kumar Sahu
Created On :11-10-2023
"""
def getBlockSTWAAEPendingData(fyear):
    """
    Function to get districtwise bore well data
    fyear : Finacial year
    schemename : Scheme name 
    """
    select_query = 'SELECT vch_lgd_code FROM t_district_stw_pending_aae_data where deleted_at is NULL group by vch_lgd_code'
    cur = mc.conn.cursor()
    cur.execute(select_query)
    dist_data=cur.fetchall()
    for lgd_code in dist_data:
        finalUrl = "{0}?appKey={1}&Fyr={2}&distcode={3}".format('https://dbtmbdodisha.nic.in/dafp/getspSTWReportForAdapForPendingWithAAEBlockWise','HGyu758hy4g5JUTi3589FR67', fyear,''.join(lgd_code))
        
        response_json = fetachUrlJsonData(finalUrl)
        for rdata in  response_json:
            block_name                   = rdata['BlockName']
            lgd_code                     = ''.join(lgd_code) 
            aae_name                     = rdata['AAEInitialPending']
            aae_mobileno                 = rdata['AAEInitialPending']
            aae_initialpending           = rdata['AAEInitialPending']
            aae_billingpending           = rdata['AAEBillingPending']
            current_datetime             = datetime.datetime.now()
            try:            
                insert_query = "INSERT IGNORE INTO t_block_stw_pending_aae_data (vch_dist_lgd_code,vch_block_name,vch_aae_name,vch_aae_mobileno,vch_aae_initialpending,vch_aae_billingpending,vch_finacial_year,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)"
                valdata =(lgd_code,block_name,aae_name,aae_mobileno,aae_initialpending,aae_billingpending,fyear,current_datetime,current_datetime)
                cur = mc.conn.cursor()
                cur.execute(insert_query, valdata)
                mc.conn.commit()
        
            except Exception as e:
                    mc.conn.rollback()
                    logging.error("Error in insertion - t_block_stw_pending_aae_data")
                    logging.error("Error in getting data for t_block_stw_pending_aae_data from API getSTWReportForAdapForPendingWithAAOBlockWise")
                    logging.error(e)
        print("Block STW AAE pending data completed")
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_block_stw_pending_aae_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    # Get the current financial year
    current_fy = mc.get_current_fy()
    f_year=''
    for i in range(2017, int(current_fy[:4]) + 1):
        f_year = str(i) + "-" + str(i + 1)[-2:]
        getBlockSTWAAEPendingData(f_year)
    #getBlockSTWAAEPendingData()