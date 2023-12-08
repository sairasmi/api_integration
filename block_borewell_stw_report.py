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
Function to get districtwise bore well and STW Report
Created By : Ranjit Kumar Sahu
Created On :10-10-2023
"""
def getBlockBorewellAndSTWReport(fyear,schemename,plip,chk):
    """
    Function to get districtwise bore well and STW Report
    fyear : Finacial year
    schemename : Scheme name 
    """
    select_query = 'SELECT vch_lgd_code FROM t_district_borewell_stw_report where deleted_at is NULL AND vch_finacial_year ="{0}" AND vch_scheme_name="{1}" AND vch_plip="{2}" AND int_chk="{3}"'.format(fyear,schemename,plip,chk)
    # select_query = 'SELECT vch_lgd_code FROM t_district_borewell_stw_report where deleted_at is NULL GROUP BY vch_lgd_code'
    cur = mc.conn.cursor()
    cur.execute(select_query)
    dist_data=cur.fetchall()
    for lgd_code in dist_data:
        finalUrl = "{0}?appKey={1}&F_YEAR={2}&scheme={3}&PLIP={4}&Chk={5}&distcode={6}".format('https://dbtmbdodisha.nic.in/dafp/getReportForAdapBlockWiseBWLAndSTW','HGyu758hy4g5JUTi3589FR67', fyear,schemename,plip,chk ,''.join(lgd_code))
       
        response_json = mc.fetachUrlJsonData("GET",finalUrl)
        
        
        for rdata in  response_json:
            if chk==0:
               lgd_code = rdata['LGD_code'] 
               block_data_name= rdata['block_name']
            else:
               lgd_code = rdata['LGD_code'] 
               block_data_name = rdata['block_name']
            admin_target             = rdata['AdminTarget']
            validapplication         = rdata['ValidApplication']
            aao_inspection           = rdata['AAOInspection']
            aao_pending              = rdata['AAOPending']
            gohead_issued            = rdata['GoAheadIssued']
            goahead_pending          = rdata['GoAheadPending']
            aao_complition           = rdata['AAOComplition']
            aao_completion_pending   = rdata['AAoCompletionPending']
            no_deactivate            = rdata['NoDeactivate']
            aae_inspectionok         = rdata['AAEInspectionOk']
            aae_reject               = rdata['AAEReject']
            aae_tobe_inspected       = rdata['AAEToBeInspected']
            aae_billing              = rdata['AAEBilling']
            aae_billing_pending      = rdata['AAEBillingPending']
            physical                 = rdata['Physical']
            financial                = rdata['Financial']

            current_datetime = datetime.datetime.now()
            try:            
                insert_query = "INSERT IGNORE INTO t_block_borewell_stw_report (vch_dist_lgd_code,vch_block_name,vch_admin_target,vch_validapplication,vch_aao_inspection,vch_aao_pending,vch_gohead_issued,vch_goahead_pending,vch_aao_complition,vch_aao_completion_pending,vch_no_deactivate,vch_aae_inspectionok,vch_aae_reject,vch_aae_tobe_inspected,vch_aae_billing,vch_aae_billing_pending,vch_physical,vch_financial,vch_finacial_year,vch_scheme_name,vch_plip,int_chk,created_at,updated_at) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
                valdata =(lgd_code,block_data_name,admin_target,validapplication,aao_inspection,aao_pending,gohead_issued,goahead_pending,aao_complition,aao_completion_pending,no_deactivate,aae_inspectionok,aae_reject,aae_tobe_inspected,aae_billing,aae_billing_pending,physical,financial,fyear,schemename,plip,chk,current_datetime,current_datetime)
                cur = mc.conn.cursor()
                cur.execute(insert_query, valdata)
                mc.conn.commit()

            except Exception as e:
                mc.conn.rollback()
                logging.error("Error in insertion -t_block_borewell_stw_report")
                logging.error(e)
                logging.error("Error in getting data for t_block_borewell_stw_report from API getReportForAdapBlockWiseBWLAndSTW")
                logging.error(e)
print("Block Bore well And  STW  data completed")
    

if __name__ == "__main__":
    stm = "TRUNCATE TABLE t_block_borewell_stw_report"
    cur = mc.conn.cursor()
    cur.execute(stm)
    current_fy = mc.get_current_fy()
    f_year=''
    scheme_data =('RKVY','SP')
    plip_data=('Bore Well','STW')
    chk_data=('0','1')
    for c in chk_data:
     for p in plip_data:
      for j in scheme_data:
        for i in range(2017, int(current_fy[:4]) + 1):
            f_year = str(i) + "-" + str(i + 1)[-2:]
            getBlockBorewellAndSTWReport(f_year,j,p,c)

    #getBlockBorewellAndSTWReport()