# Konnect APIs Integration Repository

## List of APIs:

### Weather APIs

#### Get Location (One time execution)
```
https://krushipanipaga.gov.in/api/get_location.php
```

#### Get weather data in every half an hour
```
https://krushipanipaga.gov.in/api/get_rawdata.php?loc_id=116&from=2022-11-18&to=2022-11-18
```

#### Get daily weather data
```
https://krushipanipaga.gov.in/api/get_dailydata.php?loc_id=116&from=18-11-2022&to=18-11-2022
```

### Ama Krushi APIs

#### Get Ama Krushi Daily reports
```
https://dss.amakrushi.in/dailyreport/2022-10-01
```

### Dealer, Insecticide and transaction APIs

#### Get Dealer Data
```
https://odishaagrilicense.nic.in/districtDealerDetail?appKey=<appKey>&licenceType=i

licenceType- i (for Insecticide)
licenceType- f (for Fertilizer)
licenceType- s (for Seed)
```

#### Get Insectisides Data
```
https://odishaagrilicense.nic.in/insecticideDetail?appKey=<appKey>
```

#### Get Dealer Insectisides Transactions Data
```
https://odishaagrilicense.nic.in/insecticideEnteredDetails?appKey=<appKey>&year=<year>&month=<month>

e.g
month=11
year=2022

month=1
year=2023
```

### Farm Mech PDI (Post Delivery Inspection) API

```
https://dbtmbdodisha.nic.in/dafp/getPDIDATAConsolidated?apiKey=<appKey>
```

### Farm Mech Subsidy Payment API

```
https://dbtmbdodisha.nic.in/dafp/getFmndbtTransactionDtl?apiKey=<appKey>
```

### Achivement Report API
```
https://ifsodisha.nic.in/admin/achivementReport?finYear=2021-22
https://ifsodisha.nic.in/admin/achivementReport?finYear=2022-23
https://ifsodisha.nic.in/admin/achivementReport?finYear=2023-24
```

### Micro Details of all incoming calls API
```
https://crm.amakrushi.in/api/gov/mdic/2023-07-03
```

### Details of farmers onboarded API
```
https://crmapi.amakrushi.in/farmer_onboarded/2023-06-30
```

### Macro Details of Incoming & Outgoing calls
```
https://crm.amakrushi.in/api/gov/mdioc/2023-07-03
```

### Details of outgoing IVRS advisory
```
https://crmapi.amakrushi.in/advisory_details?date=2023-07-01
```


## Prerequisites
* Python 3.8.10
* mysql/MariaDB 15.1.0
* mysql-connector-python 8.0.31

## Project Setup

- Copy `config.ini.sample` to `config.ini`
- Replace the db credentials in the `config.ini` file.
- import db_schema.sql file into your mysql database - to create tables
- Create virtual env and activate it.
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
* Install the python dependencies
    ```
    pip install -r requirements.txt
    ```

## To run

- Run below command for Various APIs

### Weather APIs Execution
    ```
    # only one time
    python weather_get_location_data.py
    ```

    ```
    python weather_data_fetch_hourly.py
    # or pass from date and to date
    python weather_data_fetch_hourly.py 20-12-2022 23-12-2022
    ```

    ```
    python weather_data_fetch_daily.py # for yesterday's data
    # or pass from date and to date
    python weather_data_fetch_daily.py 20-12-2022 23-12-2022
    ```
### Dealers, Insecticides and transaction APIs Execution

    ```
    python fetch_dealer_data.py i # to get dealer data based on licenseType(check above)
    ```

    ```
    python fetch_insectisides_data.py # to get insectisides data
    ```
 
    ```
    # to get dealer insectisides transaction data
    python fetch_dealer_insectiside_transactions_data.py # for current year and month
    # or pass year and month
    python fetch_dealer_insectiside_transactions_data.py 2022 11
    ```

### Ama Krushi APIs Execution
- Run below command for ama_krushi data
    ```
    python get_ama_krushi_report_data.py
    # or pass the specific date in below format
    python get_ama_krushi_report_data.py 2022-12-18
    ```

### Farm Mech PDI (Post Delivery Inspection) API Execution

- Run the below command for farm mech PDI data
    ```
    python fetch_farm_mech_PDI_data.py
    ```

### Farm Mech Subsidy Payment API Execution

- Run the below command for farm mech subsidy Payment
    ```
    python fetch_farm_mech_subsidy_payment.py
    ```

### Achievement Report API Execution

- Run the below command for farm mech subsidy Payment
    ```
    python fetch_achievement_report.py 2021-22
    python fetch_achievement_report.py 2022-23
    python fetch_achievement_report.py 2023-24
    ```

### Micro Details of all incoming calls API Execution

- Run the below command for Micro Details of all incoming calls
    ```
    # Below command will get data for previous day
    python fetch_micro_details_incoming_calls.py
    # or 
    # Below command will get data for the specific day
    python fetch_micro_details_incoming_calls.py 2023-07-03
    ```

### Farmers Onboarded API Execution

- Run the below command for farmers onboarded API
    ```
    # Below command will get data for previous day
    python fetch_farmer_onboarded_data.py
    # or 
    # Below command will get data for the specific day
    python fetch_farmer_onboarded_data.py 2023-07-03
    ```

### Macro Details of Incoming & Outgoing calls API Execution

- Run the below command for Macro Details of Incoming & Outgoing calls API
    ```
    # Below command will get data for previous day
    python fetch_macro_details_incoming_outgoing_call.py
    # or 
    # Below command will get data for the specific day
    python fetch_macro_details_incoming_outgoing_call.py 2023-07-03
    ```

### Details of outgoing IVRS advisory

- Run the below command for outgoing IVRS advisory API
    ```
    # Below command will get data for previous day
    python fetch_outgoing_ivrs_advisory.py
    # or 
    # Below command will get data for the specific day
    python fetch_outgoing_ivrs_advisory.py 2023-07-01
    ```
