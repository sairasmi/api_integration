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
Cretaed By : Rasmi Ranjan Swain
Created on : 05 Oct 2023
"""
def fetachUrlJsonData(apiUrl):
    """
    Function to fetch api data    
     apiUrl: Api url to get the data    
    """
    app_responce = requests.request("GET",apiUrl,verify=False)
    return app_responce.json()
"""
Function to get districtwise bore well data
Created By : Rasmi Ranjan Swain
Created On :05 Oct 2023
"""
def getBlockBorewellData(fyear,schemename):
    """
    Function to get Block wise bore well data
    fyear : Finacial year
    schemename : Scheme name 
    """    
    select_query = 'SELECT vch_lgd_code FROM t_district_bore_well_data where deleted_at is NULL AND vch_finacial_year ="{0}" AND vch_scheme_name="{1}" '.format(fyear,schemename)
    #print(select_query)
    cur = mc.conn.cursor()
    cur.execute(select_query)
    dist_data=cur.fetchall()
    for lgd_code in dist_data:
        finalUrl = "{0}?appKey={1}&F_YEAR={2}&scheme={3}&distcode={4}".format('https://dbtmbdodisha.nic.in/dafp/getSpReportForAdapBlockWiseBWL','BVgd758hy4g5JUTi3589FR67', fyear,schemename,''.join(lgd_code))
        response_json = fetachUrlJsonData(finalUrl)
        for rdata in  response_json:
            slno                = rdata['Slno']
            block_name           = rdata['BlockName']
            lgd_code            = ''.join(lgd_code) 
            admin_target        = rdata['AdminTarget']
            valid_application   = rdata['ValidApplication']
            go_ahaed_generated  = rdata['GoAheadGenerated']
            project_competed    = rdata['ProjectCompleted']
            pyment_gec          = rdata['PymntGec']
            subsidy             = rdata['Subsidy']
            try:            
                insert_query = "INSERT IGNORE INTO t_block_bore_well_data (vch_block_name,vch_dist_lgd_code,vch_admin_target,vch_valid_application,vch_goahead_generated,vch_project_completed,vch_pymnt_gec,vch_subsidy,vch_finacial_year,vch_scheme_name) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
                valdata =(block_name,lgd_code,admin_target,valid_application,go_ahaed_generated,project_competed,pyment_gec,subsidy,fyear,schemename)
                cur = mc.conn.cursor()
                cur.execute(insert_query, valdata)
                mc.conn.commit()

            except Exception as e:
                mc.conn.rollback()
                logging.error("Error in insertion - t_block_bore_well_data")
                logging.error("Error in getting data for t_block_bore_well_data from API getSpReportForAdapBlockWiseBWL")
                logging.error(e)
            

print("District Bore well completed")


if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_block_bore_well_data"
    cur = mc.conn.cursor()
    cur.execute(stm)
    # Get the current financial year
    current_fy = mc.get_current_fy()
    f_year=''
    scheme_data =('RKVY','SP')
    for j in scheme_data:
        for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getBlockBorewellData(f_year,j)
    

    #getBlockBorewellData('2023-24','SP')