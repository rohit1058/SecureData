-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jul 24, 2024 at 12:29 PM
-- Server version: 8.3.0
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `securedata_2024`
--

-- --------------------------------------------------------

--
-- Table structure for table `securedata_2024_file`
--

DROP TABLE IF EXISTS `securedata_2024_file`;
CREATE TABLE IF NOT EXISTS `securedata_2024_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `file` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `publickey` varchar(255) NOT NULL,
  `document` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `securedata_2024_file`
--

INSERT INTO `securedata_2024_file` (`id`, `uid`, `user`, `username`, `date`, `file`, `filename`, `author`, `publickey`, `document`) VALUES
(6, 'DOC457920', 'user@user.com', 'user', '2024-07-24', 'd:\\wamp64\\www\\python\\securedata\\static\\docs\\education.jpg', 'education.jpg', 'Author ', '207232', 'Document ');

-- --------------------------------------------------------

--
-- Table structure for table `securedata_2024_request`
--

DROP TABLE IF EXISTS `securedata_2024_request`;
CREATE TABLE IF NOT EXISTS `securedata_2024_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `fid` varchar(255) NOT NULL,
  `file` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `document` varchar(255) NOT NULL,
  `requestedby` varchar(255) NOT NULL,
  `requestedbyname` varchar(255) NOT NULL,
  `uploadedby` varchar(255) NOT NULL,
  `uploadedbyname` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `securedata_2024_request`
--

INSERT INTO `securedata_2024_request` (`id`, `uid`, `fid`, `file`, `filename`, `document`, `requestedby`, `requestedbyname`, `uploadedby`, `uploadedbyname`, `date`, `status`) VALUES
(2, 'uid_3KOfdEqSZf', 'DOC457920', 'd:\\wamp64\\www\\python\\securedata\\static\\docs\\education.jpg', 'education.jpg', 'Document ', 'laughumust@gmail.com', 'user2', 'user@user.com', 'user', '2024-07-24', 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `securedata_2024_user`
--

DROP TABLE IF EXISTS `securedata_2024_user`;
CREATE TABLE IF NOT EXISTS `securedata_2024_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `securedata_2024_user`
--

INSERT INTO `securedata_2024_user` (`id`, `uid`, `name`, `email`, `password`, `phone`, `address`, `status`) VALUES
(7, 'uid_13AYXqjD6u', 'user', 'user@user.com', 'user', '9876543210', 'address', 'approved'),
(8, 'uid_GHXg9M0tE3', 'user2', 'user2@user2.com', 'user2', '9876543212', 'adress2', 'approved');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
