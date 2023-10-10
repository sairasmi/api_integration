import logging
import mysql.connector as MysqlConnector
import logging, configparser
from sqlalchemy import create_engine
import pymysql
import urllib.parse
import datetime
from datetime import timedelta
config = configparser.ConfigParser()
config.read("./config.ini")


class mysqlController:
    def __init__(self):
        self.conn = self.__dbConnect()
        self.engine = create_engine(
            f"mysql+pymysql://{urllib.parse.quote(config['mysql']['user'])}:{urllib.parse.quote(config['mysql']['password'])}@{config['mysql']['host']}/{config['mysql']['db']}"
        )

    def __dbConnect(self):
        self.conn = None
        try:
            logging.info("Connecting to the database ...")
            self.conn = MysqlConnector.connect(
                user=config["mysql"]["user"],
                password=config["mysql"]["password"],
                host=config["mysql"]["host"],
                database=config["mysql"]["db"],
                auth_plugin="mysql_native_password",
            )
            if self.conn.is_connected():
                logging.info("Connected to the database")
                return self.conn
            else:
                logging.error("Error in connection")
        except Exception as e:
            logging.error("Error in connection")
            logging.error(e)

    def insert_into_table(self, table_name, data):
        try:
            if table_name == config["tables"]["location"]:
                params = (
                    data["id"],
                    data["name"],
                    data["state"],
                    data["district"],
                    data["latitude"],
                    data["longitude"],
                    data["imei_no"],
                )
                insert_query = (
                    " INSERT IGNORE INTO "
                    + config["tables"]["location"]
                    + " (id, name, state, district, latitude, longitude, imei_no) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )

            elif table_name == config["tables"]["location_raw_data_half_hour"]:
                insert_query = (
                    "INSERT IGNORE INTO  "
                    + config["tables"]["location_raw_data_half_hour"]
                    + "  (response_id, district, location, date, time, TMax, TMin, HMax, HMin, Rain, ExternalPowerSupply, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                params = (
                    data["id"],
                    data["district"],
                    data["location"],
                    data["date"],
                    data["time"],
                    data["TMax"],
                    data["TMin"],
                    data["HMax"],
                    data["HMin"],
                    data["Rain"],
                    data["ExternalPowerSupply"],
                    data["location_id"],
                )

            elif table_name == config["tables"]["location_raw_data_daily"]:
                insert_query = (
                    "INSERT IGNORE INTO  "
                    + config["tables"]["location_raw_data_daily"]
                    + "  (response_id, district, location, date, TMax, TMin, HMax, HMin, Rain, location_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                params = (
                    data["id"],
                    data["district"],
                    data["location"],
                    data["date"],
                    data["TMax"],
                    data["TMin"],
                    data["HMax"],
                    data["HMin"],
                    data["Rain"],
                    data["location_id"],
                )

            elif table_name == config["tables"]["dealer_main"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["dealer_main"]
                    + "  (district_name, valid_till, licence_no, licence_type, mail, phone, dealer_name) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE district_name=%s, valid_till=%s, mail=%s, phone=%s, dealer_name=%s"
                )

                params = (
                    data["districtName"],
                    data["validTill"],
                    data["licenceNo"],
                    data["licenceType"],
                    data["mail"],
                    data["phone"],
                    data["dealerName"],
                    data["districtName"],
                    data["validTill"],
                    data["mail"],
                    data["phone"],
                    data["dealerName"],
                )

            elif table_name == config["tables"]["insecticide_main"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["insecticide_main"]
                    + "  (technical_name, percentage) VALUES (%s, %s) ON DUPLICATE KEY UPDATE percentage=%s"
                )

                params = (data["technicalName"], data["percentage"], data["percentage"])

            elif table_name == config["tables"]["dealer_insectiside_transactions"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["dealer_insectiside_transactions"]
                    + "  (licenceNo, dealer_id, technical_name, insectiside_id, available, received, intransit, sold, month, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )

                params = (
                    data["licenceNo"],
                    data["dealerId"],
                    data["technicalName"],
                    data["insectisideId"],
                    data["available"],
                    data["received"],
                    data["intransit"],
                    data["sold"],
                    data["month"],
                    data["year"],
                )

            elif table_name == config["tables"]["farm_mech_PDI_data_table"]:

                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["farm_mech_PDI_data_table"]
                    + "  (block_name, TotalToBeVerify, TotVrfied, PendingVrfy, ContactNumber, UserName) VALUES (%s, %s, %s, %s, %s, %s)"
                )

                params = (
                    data["block_name"],
                    data["TotalToBeVerify"],
                    data["TotVrfied"],
                    data["PendingVrfy"],
                    data["ContactNumber"],
                    data["UserName"],
                )

            elif table_name == config["tables"]["farm_mech_subsidy_payment_table"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["farm_mech_subsidy_payment_table"]
                    + "  (F_YEAR, FARMER_ID, VCHMOBILENO, VCHFARMERNAME, VCHFATHERNAME, Category_Value, vch_DistrictName, vch_BlockName, vch_GPNameOr, vch_VillageNameOr, Implement, SubImpl, PaymentTransDt, Bill_Crt_Dt, mfgapprovedDt, eeAppdt, BankReqDt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE F_YEAR=%s, VCHMOBILENO=%s, VCHFARMERNAME=%s, VCHFATHERNAME=%s, Category_Value=%s, vch_DistrictName=%s, vch_BlockName=%s, vch_GPNameOr=%s, vch_VillageNameOr=%s, Implement=%s, SubImpl=%s, Bill_Crt_Dt=%s, mfgapprovedDt=%s, eeAppdt=%s, BankReqDt=%s"
                )

                params = (
                    data["F_YEAR"],
                    data["FARMER_ID"],
                    data["VCHMOBILENO"],
                    data["VCHFARMERNAME"],
                    data["VCHFATHERNAME"],
                    data["Category_Value"],
                    data["vch_DistrictName"],
                    data["vch_BlockName"],
                    data["vch_GPNameOr"],
                    data["vch_VillageNameOr"],
                    data["Implement"],
                    data["SubImpl"],
                    data["PaymentTransDt"],
                    data["Bill_Crt_Dt"],
                    data["mfgapprovedDt"],
                    data["eeAppdt"],
                    data["BankReqDt"],
                    data["F_YEAR"],
                    data["VCHMOBILENO"],
                    data["VCHFARMERNAME"],
                    data["VCHFATHERNAME"],
                    data["Category_Value"],
                    data["vch_DistrictName"],
                    data["vch_BlockName"],
                    data["vch_GPNameOr"],
                    data["vch_VillageNameOr"],
                    data["Implement"],
                    data["SubImpl"],
                    data["Bill_Crt_Dt"],
                    data["mfgapprovedDt"],
                    data["eeAppdt"],
                    data["BankReqDt"],
                )

            elif table_name == config["tables"]["achivement_report_data"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["achivement_report_data"]
                    + "  (srno, finyear, DistrictName, target, assistance, NormalAdminCost, SCPAdminCost, TASPAdminCost, noappsubmotted, nocancelapplication, totalappsubmitted, initialverificationcompleted, dlcapproved, nogoagead, rejnogoagead, seedmoneybao, phasebbao, secondphasebao, thirdphasemoneybao, total1stphasefilerealsed, total1stphasepymntrealsed, total2ndphasefilerealsed, total2ndphasepymntrealsed, total3rdphasefilerealsed, total3rdphasepymntrealsed, total4thphasefilerealsed, total4thphasepymntrealsed, trainingexp, adminstrativeexp, wshg, totalexpenses, grandtotal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE srno=%s, target=%s, assistance=%s, NormalAdminCost=%s, SCPAdminCost=%s, TASPAdminCost=%s, noappsubmotted=%s, nocancelapplication=%s, totalappsubmitted=%s, initialverificationcompleted=%s, dlcapproved=%s, nogoagead=%s, rejnogoagead=%s, seedmoneybao=%s, phasebbao=%s, secondphasebao=%s, thirdphasemoneybao=%s, total1stphasefilerealsed=%s, total1stphasepymntrealsed=%s, total2ndphasefilerealsed=%s, total2ndphasepymntrealsed=%s, total3rdphasefilerealsed=%s, total3rdphasepymntrealsed=%s, total4thphasefilerealsed=%s, total4thphasepymntrealsed=%s, trainingexp=%s, adminstrativeexp=%s, wshg=%s, totalexpenses=%s, grandtotal=%s"
                )
                params = (
                    data["srno"],
                    data["finyear"],
                    data["DistrictName"],
                    data["target"],
                    data["assistance"],
                    data["NormalAdminCost"],
                    data["SCPAdminCost"],
                    data["TASPAdminCost"],
                    data["noappsubmotted"],
                    data["nocancelapplication"],
                    data["totalappsubmitted"],
                    data["initialverificationcompleted"],
                    data["dlcapproved"],
                    data["nogoagead"],
                    data["rejnogoagead"],
                    data["seedmoneybao"],
                    data["phasebbao"],
                    data["secondphasebao"],
                    data["thirdphasemoneybao"],
                    data["total1stphasefilerealsed"],
                    data["total1stphasepymntrealsed"],
                    data["total2ndphasefilerealsed"],
                    data["total2ndphasepymntrealsed"],
                    data["total3rdphasefilerealsed"],
                    data["total3rdphasepymntrealsed"],
                    data["total4thphasefilerealsed"],
                    data["total4thphasepymntrealsed"],
                    data["trainingexp"],
                    data["adminstrativeexp"],
                    data["wshg"],
                    data["totalexpenses"],
                    data["grandtotal"],
                    data["srno"],
                    data["target"],
                    data["assistance"],
                    data["NormalAdminCost"],
                    data["SCPAdminCost"],
                    data["TASPAdminCost"],
                    data["noappsubmotted"],
                    data["nocancelapplication"],
                    data["totalappsubmitted"],
                    data["initialverificationcompleted"],
                    data["dlcapproved"],
                    data["nogoagead"],
                    data["rejnogoagead"],
                    data["seedmoneybao"],
                    data["phasebbao"],
                    data["secondphasebao"],
                    data["thirdphasemoneybao"],
                    data["total1stphasefilerealsed"],
                    data["total1stphasepymntrealsed"],
                    data["total2ndphasefilerealsed"],
                    data["total2ndphasepymntrealsed"],
                    data["total3rdphasefilerealsed"],
                    data["total3rdphasepymntrealsed"],
                    data["total4thphasefilerealsed"],
                    data["total4thphasepymntrealsed"],
                    data["trainingexp"],
                    data["adminstrativeexp"],
                    data["wshg"],
                    data["totalexpenses"],
                    data["grandtotal"],
                )
            elif table_name == config["tables"]["micro_details_incoming_call"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["micro_details_incoming_call"]
                    + "  (date, time, farmer_name, farmer_ph_no, district, block, gp, domain, tag1, tag2, callstatus, operator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE farmer_name=%s, district=%s, block=%s, gp=%s, domain=%s, tag1=%s, tag2=%s, callstatus=%s, operator=%s"
                )
                params = (
                    data["date"],
                    data["time"],
                    data["farmer_name"],
                    data["farmer_no"],
                    data["district"],
                    data["block"],
                    data["gp"],
                    data["domain"],
                    data["tag1"],
                    data["tag2"],
                    data["callstatus"],
                    data["operator"],
                    data["farmer_name"],
                    data["district"],
                    data["block"],
                    data["gp"],
                    data["domain"],
                    data["tag1"],
                    data["tag2"],
                    data["callstatus"],
                    data["operator"]
                )
            elif table_name == config["tables"]["farmers_onboarded"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["farmers_onboarded"]
                    + "  (active_date, crop_domain, fisheries_domain, livestock_domain, forest_domain, null_domain, district_name, farmer_onboarded_district_wise) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE crop_domain=%s, fisheries_domain=%s, livestock_domain=%s, forest_domain=%s, null_domain=%s, farmer_onboarded_district_wise=%s"
                )
                params = (
                    data["active_date"],
                    data["crop_domain"],
                    data["fisheries_domain"],
                    data["livestock_domain"],
                    data["forest_domain"],
                    data["null_domain"],
                    data["district_name"],
                    data["farmer_onboarded_district_wise"],
                    data["crop_domain"],
                    data["fisheries_domain"],
                    data["livestock_domain"],
                    data["forest_domain"],
                    data["null_domain"],
                    data["farmer_onboarded_district_wise"]
                )
            elif table_name == config["tables"]["macro_details_incoming_outgoing_call"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["macro_details_incoming_outgoing_call"]
                    + "  (uid, date, district, workinghrs_miss_count, non_workinghrs_count, total_inbound, total_inbound_duration_avg, total_out_completed, total_out_completed_duration_avg, total_outbound) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE uid=%s, workinghrs_miss_count=%s, non_workinghrs_count=%s, total_inbound=%s, total_inbound_duration_avg=%s, total_out_completed=%s, total_out_completed_duration_avg=%s, total_outbound=%s"
                )
                params = (
                    data["uid"],
                    data["date"],
                    data["district"],
                    data["workinghrs_miss_count"],
                    data["non_workinghrs_count"],
                    data["total_inbound"],
                    data["total_inbound_duration_avg"],
                    data["total_out_completed"],
                    data["total_out_completed_duration_avg"],
                    data["total_outbound"],
                    data["uid"],
                    data["workinghrs_miss_count"],
                    data["non_workinghrs_count"],
                    data["total_inbound"],
                    data["total_inbound_duration_avg"],
                    data["total_out_completed"],
                    data["total_out_completed_duration_avg"],
                    data["total_outbound"]
                )
            elif table_name == config["tables"]["outgoing_ivrs_advisory"]:
                insert_query = (
                    "INSERT INTO  "
                    + config["tables"]["outgoing_ivrs_advisory"]
                    + "  (date, advisories_pickup, average_advisory_duration, average_listening_duration, district, crop_domain, fish_domain, livestock_domain, farmer_reached, total_advisory_sent, unique_advisories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE advisories_pickup=%s, average_advisory_duration=%s, average_listening_duration=%s, crop_domain=%s, fish_domain=%s, livestock_domain=%s, farmer_reached=%s, total_advisory_sent=%s, unique_advisories=%s"
                )
                params = (
                    data["date"],
                    data["advisories_pickup"],
                    data["average_advisory_duration"],
                    data["average_listening_duration"],
                    data["district"],
                    data["crop_domain"],
                    data["fish_domain"],
                    data["livestock_domain"],
                    data["farmer_reached"],
                    data["total_advisory_sent"],
                    data["unique_advisories"],
                    data["advisories_pickup"],
                    data["average_advisory_duration"],
                    data["average_listening_duration"],
                    data["crop_domain"],
                    data["fish_domain"],
                    data["livestock_domain"],
                    data["farmer_reached"],
                    data["total_advisory_sent"],
                    data["unique_advisories"]
                )

            cur = self.conn.cursor()
            cur.execute(insert_query, params)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            logging.error("Error in insertion - {0}".format(table_name))
            logging.error(e)
            logging.error("Data not inserted - {0}".format(table_name))

    def fetch_from_table(self, table_name, limit=100, page=1):
        try:
            if table_name == config["tables"]["location"]:
                select_query = "SELECT id FROM {0}".format(config["tables"]["location"])
            elif table_name == config["tables"]["location_raw_data_hourly"]:
                pass
            elif table_name == config["tables"]["location_raw_data_daily"]:
                pass

            cur = self.conn.cursor()
            cur.execute(select_query)
            return cur.fetchall()
        except Exception as e:
            logging.error("Error in selection - {0}".format(table_name))
            logging.error(e)

    def truncate_table(self, table_name):
        try:
            stm = "TRUNCATE TABLE {0}".format(table_name)
            cur = self.conn.cursor()
            cur.execute(stm)
        except Exception as e:
            logging.error("Error in TRUNCATE table - {0}".format(table_name))
            logging.error(e)

    def delete_data_on_dealer_by_licence_type(self, licence_type):
        try:
            select_query = "DELETE FROM {0} WHERE licence_type='{1}'".format(
                config["tables"]["dealer_main"], licence_type
            )

            cur = self.conn.cursor()
            cur.execute(select_query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error("Error in delete_data_on_dealer_by_licence_type")
            logging.error(e)

    def delete_data_on_dit_by_year_month(self, year, month):
        try:
            select_query = "DELETE FROM {0} WHERE year={1} and month={2}".format(
                config["tables"]["dealer_insectiside_transactions"], year, month
            )

            cur = self.conn.cursor()
            cur.execute(select_query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error("Error in delete_data_on_dit_by_year_month")
            logging.error(e)

    def get_dealer_by_licence_no(self, licence_no):
        try:
            select_query = "SELECT id FROM {0} where licence_no='{1}'".format(
                config["tables"]["dealer_main"], licence_no
            )

            cur = self.conn.cursor()
            cur.execute(select_query)
            return cur.fetchone()
        except Exception as e:
            logging.error("Error in get_dealer_by_licence_no")
            logging.error(e)

    def get_insectisides_by_technical_name(self, technical_name):
        try:
            select_query = 'SELECT id FROM {0} where technical_name="{1}"'.format(
                config["tables"]["insecticide_main"], technical_name
            )

            cur = self.conn.cursor()
            cur.execute(select_query)
            return cur.fetchone()
        except Exception as e:
            logging.error("Error in get_insectisides_by_technical_name")
            logging.error(e)
    # Define a function to get the current financial year
    def get_current_fy(self):
        # Get the current date
        today = datetime.date.today()
        # Get the current year and month
        year = today.year
        month = today.month
        # If the month is before April, subtract one from the year
        if month < 4:
            year -= 1
        # Return the current financial year as a string
        return str(year) + "-" + str(year + 1)
