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
Function to get districtwise bore well pending data
Created By : Ranjit Kumar Sahu
Created On :11-10-2023
"""
def getBlockSTWData(fyear):
    """
    Function to get districtwise bore well data
    fyear : Finacial year
    schemename : Scheme name 
    """
    select_query = 'SELECT vch_lgd_code FROM t_district_stw_data where deleted_at is NULL AND vch_finacial_year ="{0}"'.format(fyear)
    cur = mc.conn.cursor()
    cur.execute(select_query)
    dist_data=cur.fetchall()
    for lgd_code in dist_data:
        finalUrl = "{0}?appKey={1}&F_YEAR={2}&distcode={3}".format('https://dbtmbdodisha.nic.in/dafp/getSpReportForAdapBlockWiseSTW','HGyu758hy4g5JUTi3589FR67', fyear,''.join(lgd_code))
    
        response_json = mc.fetachUrlJsonData("GET",finalUrl)
        for rdata in  response_json:
            block_name            = rdata['block_name']
            lgd_code              = ''.join(lgd_code) 
            admin_target          = rdata['AdminTarget']
            valid_application     = rdata['ValidApplication']
            goahead_generated     = rdata['GoAheadGenerated']
            project_completed     = rdata['ProjectCompleted']
            pymnt_gec             = rdata['PymntGec']
            subsidy               = rdata['Subsidy']
            current_datetime      = datetime.datetime.now()
            try:            
                insert_query = "INSERT IGNORE INTO t_block_stw_data (vch_dist_lgd_code,vch_block_name,vch_admin_target,vch_valid_application,vch_goahead_generated,vch_project_completed,vch_pymnt_gec,vch_subsidy,vch_finacial_year,created_at,updated_at) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
                valdata =(lgd_code,block_name,admin_target,valid_application,goahead_generated,project_completed,pymnt_gec,subsidy,fyear,current_datetime,current_datetime)
                cur = mc.conn.cursor()
                cur.execute(insert_query, valdata)
                mc.conn.commit()
        
            except Exception as e:
                    mc.conn.rollback()
                    logging.error("Error in insertion - t_block_stw_data")
                    logging.error("Error in getting data for t_block_stw_data from API getSpReportForAdapBlockWiseSTW")
                    logging.error(e)
print("Block STW data completed")
if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_block_stw_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    # Get the current financial year
    current_fy = mc.get_current_fy()
    f_year=''
    # scheme_data =('RKVY','SP')
    # for j in scheme_data:
    for i in range(2017, int(current_fy[:4]) + 1):
        f_year = str(i) + "-" + str(i + 1)[-2:]
        getBlockSTWData(f_year)
    #getBlockSTWData()