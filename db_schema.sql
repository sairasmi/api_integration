-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 06, 2023 at 05:20 AM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `weatherpiyush`
--

-- --------------------------------------------------------
CREATE TABLE `location` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `state` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  `imei_no` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------
--
-- Table structure for table `location_raw_data_daily`
--
CREATE TABLE `location_raw_data_daily` (
  `id` int NOT NULL AUTO_INCREMENT,
  `response_id` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `date` date NOT NULL,
  `TMax` float NOT NULL,
  `TMin` float NOT NULL,
  `HMax` float NOT NULL,
  `HMin` float NOT NULL,
  `Rain` float NOT NULL,
  `location_id` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`location_id`,`date`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------
--
-- Table structure for table `location_raw_data_hourly`
--
CREATE TABLE `location_raw_data_hourly` (
  `id` int NOT NULL AUTO_INCREMENT,
  `response_id` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL,
  `TMax` float NOT NULL,
  `TMin` float NOT NULL,
  `HMax` float NOT NULL,
  `HMin` float NOT NULL,
  `Rain` float NOT NULL,
  `ExternalPowerSupply` float NOT NULL,
  `location_id` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`time`, `date`, `location_id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- --------------------------------------------------------
--
-- Table structure for table `ama_krushi_reports`
--
CREATE TABLE `ama_krushi_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `advisories_sent` int DEFAULT NULL,
  `number_of_unique_farmers_getting_advisory` int DEFAULT NULL,
  `advisory_calls_picked_up` float DEFAULT NULL,
  `average_call_duration_sec` float DEFAULT NULL,
  `unique_advisories_sent` int DEFAULT NULL,
  `survey_calls_attempted` int DEFAULT NULL,
  `survey_calls_completed` int DEFAULT NULL,
  `incoming_calls_on_LCC` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `ama_krushi_daily_reports` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `advisory_calls_picked_up` FLOAT NULL,
  `date` DATE NULL,
  `advisory_send` INT NULL,
  `avg_call_duration` FLOAT NULL,
  `farmer_onboarded` INT NULL,
  `incoming_calls_on_LCC` INT NULL,
  `no_unique_farmers_getting_advisory` INT NULL,
  `survey_calls_attempted` INT NULL,
  `survey_calls_completed` INT NULL,
  `unique_advisories_sent` INT NULL,
  `district_name` VARCHAR(255) NULL,
  `ivr_send_district_wise` INT NULL,
  `farmer_onboarded_district_wise` INT NULL,
  `unique_farmer_district_wise` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`));
-- --------------------------------------------------------

--
-- Table structure for table `dealer_main`
--

CREATE TABLE `dealer_main` (
  `id` int NOT NULL AUTO_INCREMENT,
  `district_name` varchar(255) DEFAULT NULL,
  `valid_till` datetime NOT NULL,
  `licence_no` varchar(255) NOT NULL,
  `licence_type` varchar(255) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `dealer_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `licence_no` (`licence_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `insecticide_main`
--
CREATE TABLE `insecticide_main` (
  `id` int NOT NULL AUTO_INCREMENT,
  `technical_name` varchar(255) NOT NULL,
  `percentage` float DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `technical_name` (`technical_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
--
-- Table structure for table `dealer_insectiside_transactions`
--
CREATE TABLE `dealer_insectiside_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `licenceNo` varchar(255) NOT NULL,
  `dealer_id` int NOT NULL,
  `technical_name` varchar(255) NOT NULL,
  `insectiside_id` int DEFAULT NULL,
  `available` int NOT NULL DEFAULT '0',
  `received` int NOT NULL DEFAULT '0',
  `intransit` int NOT NULL DEFAULT '0',
  `sold` int NOT NULL DEFAULT '0',
  `month` varchar(2) NOT NULL,
  `year` varchar(4) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `dealer_FK` (`dealer_id`),
  KEY `insectiside_FK` (`insectiside_id`),
  CONSTRAINT `dealer_FK` FOREIGN KEY (`dealer_id`) REFERENCES `dealer_main` (`id`),
  CONSTRAINT `insectiside_FK` FOREIGN KEY (`insectiside_id`) REFERENCES `insecticide_main` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

CREATE TABLE `farm_mech_PDI_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `block_name` VARCHAR(45) NULL,
  `TotalToBeVerify` INT NULL,
  `TotVrfied` INT NULL,
  `PendingVrfy` INT NULL,
  `ContactNumber` VARCHAR(45) NULL,
  `UserName` VARCHAR(45) NULL,
  `DB_LOAD_TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);


CREATE TABLE `farm_mech_subsidy_payment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `F_YEAR` VARCHAR(255) NULL,
  `FARMER_ID` VARCHAR(255) NOT NULL,
  `VCHMOBILENO` VARCHAR(255) NULL,
  `VCHFARMERNAME` VARCHAR(255) NULL,
  `VCHFATHERNAME` VARCHAR(255) NULL,
  `Category_Value` VARCHAR(255) NULL,
  `vch_DistrictName` VARCHAR(255) NULL,
  `vch_BlockName` VARCHAR(255) NULL,
  `vch_GPNameOr` VARCHAR(255) NULL,
  `vch_VillageNameOr` VARCHAR(255) NULL,
  `Implement` VARCHAR(255) NULL,
  `SubImpl` VARCHAR(255) NULL,
  `PaymentTransDt` DATETIME NULL,
  `Bill_Crt_Dt` DATETIME NULL,
  `mfgapprovedDt` DATETIME NULL,
  `eeAppdt` DATETIME NULL,
  `BankReqDt` DATETIME NULL,
  `DB_LOAD_TS` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`FARMER_ID`));

--
-- Table structure for table `achivement_report_data`
--
CREATE TABLE `achivement_report_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `srno` VARCHAR(255) NULL,
  `finyear` VARCHAR(255) NOT NULL,
  `DistrictName` VARCHAR(255) NOT NULL,
  `target` VARCHAR(255) NULL,
  `noappsubmotted` VARCHAR(255) NULL,
  `nocancelapplication` varchar(255) NULL,
  `totalappsubmitted` varchar(255) NULL,
  `initialverificationcompleted` VARCHAR(255) NULL,
  `dlcapproved` VARCHAR(255) NULL,
  `nogoagead` VARCHAR(255) NULL,
  `rejnogoagead` VARCHAR(255) NULL,
  `seedmoneybao` VARCHAR(255) NULL,
  `phasebbao` VARCHAR(255) NULL,
  `secondphasebao` VARCHAR(255) NULL,
  `thirdphasemoneybao` VARCHAR(255) NULL,
  `total1stphasefilerealsed` VARCHAR(255) NULL,
  `total1stphasepymntrealsed` VARCHAR(255) NULL,
  `total2ndphasefilerealsed` VARCHAR(255) NULL,
  `total2ndphasepymntrealsed` VARCHAR(255) NULL,
  `total3rdphasefilerealsed` VARCHAR(255) NULL,
  `total3rdphasepymntrealsed` VARCHAR(255) NULL,
  `total4thphasefilerealsed` VARCHAR(255) NULL,
  `total4thphasepymntrealsed` VARCHAR(255) NULL,
  `trainingexp` VARCHAR(255) NULL,
  `adminstrativeexp` VARCHAR(255) NULL,
  `wshg` VARCHAR(255) NULL,
  `totalexpenses` VARCHAR(255) NULL,
  `grandtotal` VARCHAR(255) NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  PRIMARY KEY (`finyear`, `DistrictName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
COMMIT;

--
-- Table structure for table `micro_details_incoming_call`
--

CREATE TABLE `api_integration`.`micro_details_incoming_call` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `time` VARCHAR(255) NOT NULL,
  `farmer_name` VARCHAR(255) NULL,
  `farmer_ph_no` VARCHAR(255) NOT NULL,
  `district` VARCHAR(255) NULL,
  `block` VARCHAR(255) NULL,
  `gp` VARCHAR(255) NULL,
  `domain` VARCHAR(255) NULL,
  `tag1` VARCHAR(255) NULL,
  `tag2` VARCHAR(255) NULL,
  `callstatus` VARCHAR(255) NULL,
  `operator` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`date`, `time`, `farmer_ph_no`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

CREATE TABLE `api_integration`.`farmers_onboarded` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `active_date` DATE NOT NULL,
  `crop_domain` INT NULL,
  `fisheries_domain` INT NULL,
  `livestock_domain` INT NULL,
  `district_name` VARCHAR(255) NOT NULL,
  `farmer_onboarded_district_wise` INT NULL,
  `total_farmer_onboarded` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`active_date`, `district_name`));

CREATE TABLE `api_integration`.`macro_details_incoming_outgoing_call` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(255) NULL,
  `date` DATE NOT NULL,
  `district` VARCHAR(255) NOT NULL,
  `workinghrs_miss_count` FLOAT NULL,
  `non_workinghrs_count` FLOAT NULL,
  `total_inbound` FLOAT NULL,
  `total_inbound_duration_avg` FLOAT NULL,
  `total_out_completed` FLOAT NULL,
  `total_out_completed_duration_avg` FLOAT NULL,
  `total_outbound` FLOAT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX `idmacro_details_incoming_outgoing_call_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`date`, `district`));

CREATE TABLE `api_integration`.`outgoing_ivrs_advisory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `advisories_pickup` INT NULL,
  `average_advisory_duration` FLOAT NULL,
  `average_listening_duration` FLOAT NULL,
  `district` VARCHAR(255) NOT NULL,
  `crop_domain` FLOAT NULL,
  `fish_domain` FLOAT NULL,
  `livestock_domain` FLOAT NULL,
  `farmer_reached` INT NULL,
  `total_advisory_sent` INT NULL,
  `unique_advisories` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  PRIMARY KEY (`date`, `district`));

ALTER TABLE `api_integration`.`achivement_report_data` 
ADD COLUMN `assistance` VARCHAR(255) NULL AFTER `target`,
ADD COLUMN `NormalAdminCost` VARCHAR(255) NULL AFTER `assistance`,
ADD COLUMN `SCPAdminCost` VARCHAR(255) NULL AFTER `NormalAdminCost`,
ADD COLUMN `TASPAdminCost` VARCHAR(255) NULL AFTER `SCPAdminCost`;


ALTER TABLE `farmers_onboarded` 
CHANGE COLUMN `district_name` `district_name` VARCHAR(255) NOT NULL AFTER `active_date`,
CHANGE COLUMN `total_farmer_onboarded` `null_domain` INT NULL DEFAULT NULL AFTER `livestock_domain`;
ALTER TABLE `api_integration`.`farmers_onboarded` 
ADD COLUMN `forest_domain` INT NULL DEFAULT NULL AFTER `livestock_domain`;
