-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306

-- Generation Time: Jan 14, 2019 at 06:42 AM
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
-- Database: `book`
--
CREATE DATABASE IF NOT EXISTS `requestor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `requestor`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `requestor`;
CREATE TABLE IF NOT EXISTS `requestor` (
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `tele_id` varchar(64) NOT NULL,
  `requestor_id` int(12) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`requestor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `requestor` (`first_name`, `last_name`, `username`, `tele_id`, `requestor_id`) VALUES
('Julian', 'Ung', 'julianung', 'JulianUng:)', 1),
('Arthur', 'Hain', 'arthurniah', 'ArthurHain', 2),
('ZenYu', 'Ong', 'ozy', 'zenyu112', 3),
('Joseph', 'Alde', 'joseph_alde', 'junioralde', 4),
('Sabrina', 'Halmi', 'sabbie', 'sabbiedoodle', 5),
('JinLiang', 'Loh', 'LJL', 'Jin_Loh', 6);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;