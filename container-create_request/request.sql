-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `order`
--
CREATE DATABASE IF NOT EXISTS `request` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `request`;

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `requst`;
CREATE TABLE IF NOT EXISTS `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `requestor_id` int(11) NOT NULL,
  `provider_id` int(11),
  `status` varchar(32) NOT NULL DEFAULT 'UNACCEPTED',
  `document_link` varchar(100),
  `create_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `coordinates` varchar(100) NOT NULL ,
  `location_name` varchar(100) NOT NULL,
  PRIMARY KEY (`request_id`),
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `data`
--

INSERT INTO `request` (`request_id`, `requestor_id`, `provider_id`, `status`, `document_link`, 'create_datetime', 'coordinates', 'location_name') VALUES
(1, 2, 3, "status test", "xxxxxx", '2020-06-12 02:14:55', "coordinates", "toa payoh");

-- --------------------------------------------------------