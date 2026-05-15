-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2026 at 06:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `healthcheck_ph`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES
(1, 'admin', 'admin@example.com', 'scrypt:32768:8:1$4qNkrx85mx3qSOEE$18a7d423bca0718db802f15254eebf49f4bb3bbf76414ac3940eadb2d1c9daf966ba28ba615c8cd7b703b9b1d10f3de43dc9c89ad3510d0fa0f48b99cc816912', '2026-05-16 00:08:23');

-- --------------------------------------------------------

--
-- Table structure for table `health_records`
--

CREATE TABLE `health_records` (
  `record_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `body_temperature` decimal(5,2) DEFAULT NULL,
  `heart_rate` int(11) DEFAULT NULL,
  `spo2` int(11) DEFAULT NULL,
  `blood_pressure` varchar(20) DEFAULT NULL,
  `height` decimal(5,2) DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `bmi` decimal(5,2) DEFAULT NULL,
  `bmi_category` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `measurement_datetime` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `health_records`
--

INSERT INTO `health_records` (`record_id`, `user_id`, `body_temperature`, `heart_rate`, `spo2`, `blood_pressure`, `height`, `weight`, `bmi`, `bmi_category`, `status`, `measurement_datetime`) VALUES
(1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'In Progress', '2026-05-06 19:27:05'),
(2, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'In Progress', '2026-05-06 19:27:51'),
(3, 3, 36.40, 86, 96, '121/80', 156.50, 61.30, 25.00, 'Overweight', 'Needs Review', '2026-05-06 19:34:34'),
(4, 4, 36.80, 76, 99, '124/84', 162.40, 56.40, 21.40, 'Normal', 'Normal', '2026-05-06 19:41:54'),
(5, 5, 36.60, 84, 96, '123/73', 167.60, 68.20, 24.30, 'Normal', 'Normal', '2026-05-06 19:49:49'),
(6, 6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'In Progress', '2026-05-06 19:52:55'),
(7, 7, 36.50, 89, 97, '123/83', 168.90, 58.30, 20.40, 'Normal', 'Normal', '2026-05-06 20:07:23'),
(8, 8, 37.10, 84, 97, '117/79', 168.80, 52.20, 18.30, 'Underweight', 'Needs Review', '2026-05-06 20:16:51'),
(9, 9, 37.00, 71, 97, '110/72', 174.90, 66.90, 21.90, 'Normal', 'Normal', '2026-05-10 21:27:06'),
(10, 10, 36.60, 93, 98, '116/79', 177.40, 69.70, 22.10, 'Normal', 'Normal', '2026-05-15 19:03:05'),
(11, 11, 36.50, 72, 97, '116/76', 169.80, 60.20, 20.90, 'Normal', 'Normal', '2026-05-15 19:17:31'),
(12, 12, 36.50, 92, 97, '121/74', 155.10, 64.50, 26.80, 'Overweight', 'Needs Review', '2026-05-15 19:22:52'),
(13, 13, 36.60, 86, 96, '112/85', 170.20, 68.00, 23.50, 'Normal', 'Normal', '2026-05-15 19:27:34'),
(14, 14, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'In Progress', '2026-05-15 19:33:47'),
(15, 15, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'In Progress', '2026-05-15 23:50:35'),
(16, 16, 36.50, 96, 98, '125/78', 161.10, 72.20, 27.80, 'Overweight', 'Needs Review', '2026-05-15 23:54:50'),
(17, 17, 36.80, 76, 98, '113/85', 175.00, 69.60, 22.70, 'Normal', 'In Progress', '2026-05-15 23:56:23'),
(18, 18, 36.40, 94, 97, '124/82', 176.10, 65.20, 21.00, 'Normal', 'In Progress', '2026-05-16 00:35:35');

-- --------------------------------------------------------

--
-- Table structure for table `qr_code_records`
--

CREATE TABLE `qr_code_records` (
  `qr_id` int(11) NOT NULL,
  `record_id` int(11) NOT NULL,
  `qr_code` varchar(255) NOT NULL,
  `generated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qr_code_records`
--

INSERT INTO `qr_code_records` (`qr_id`, `record_id`, `qr_code`, `generated_at`) VALUES
(1, 1, 'HC-1-2f138245', '2026-05-06 19:27:05'),
(2, 2, 'HC-2-effd6425', '2026-05-06 19:27:51'),
(3, 3, 'HC-3-1153d2c6', '2026-05-06 19:34:34'),
(4, 4, 'HC-4-76353efc', '2026-05-06 19:41:54'),
(5, 5, 'HC-5-80ab8fce', '2026-05-06 19:49:49'),
(6, 6, 'HC-6-47c3816a', '2026-05-06 19:52:55'),
(7, 7, 'HC-7-5e6e255a', '2026-05-06 20:07:23'),
(8, 8, 'HC-8-833dc0c0', '2026-05-06 20:16:51'),
(9, 9, 'HC-9-fabcb643', '2026-05-10 21:27:06'),
(10, 10, 'HC-10-125bced7', '2026-05-15 19:03:05'),
(11, 11, 'HC-11-6211fd63', '2026-05-15 19:17:31'),
(12, 12, 'HC-12-b4212866', '2026-05-15 19:22:52'),
(13, 13, 'HC-13-f02bed78', '2026-05-15 19:27:34'),
(14, 14, 'HC-14-9529dda8', '2026-05-15 19:33:47'),
(15, 15, 'HC-15-ac3e8a47', '2026-05-15 23:50:35'),
(16, 16, 'HC-16-ddaf9580', '2026-05-15 23:54:50'),
(17, 17, 'HC-17-75828aca', '2026-05-15 23:56:23'),
(18, 18, 'HC-18-4d916e83', '2026-05-16 00:35:35');

-- --------------------------------------------------------

--
-- Table structure for table `sensor_data`
--

CREATE TABLE `sensor_data` (
  `sensor_data_id` int(11) NOT NULL,
  `record_id` int(11) NOT NULL,
  `sensor_type` varchar(100) NOT NULL,
  `sensor_value` varchar(100) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor_data`
--

INSERT INTO `sensor_data` (`sensor_data_id`, `record_id`, `sensor_type`, `sensor_value`, `timestamp`) VALUES
(3, 3, 'Temperature Sensor', '36.4', '2026-05-06 19:34:35'),
(4, 3, 'Heart Rate Sensor', '86', '2026-05-06 19:34:37'),
(5, 3, 'SpO2 Sensor', '96', '2026-05-06 19:34:37'),
(6, 3, 'Blood Pressure Sensor', '121/80', '2026-05-06 19:34:38'),
(7, 3, 'Height Sensor', '156.5', '2026-05-06 19:34:40'),
(8, 3, 'Weight Sensor', '61.3', '2026-05-06 19:34:41'),
(9, 3, 'BMI Calculation', '25.0 - Overweight', '2026-05-06 19:34:42'),
(10, 4, 'Temperature Sensor', '36.8', '2026-05-06 19:41:57'),
(11, 4, 'Heart Rate Sensor', '76', '2026-05-06 19:41:58'),
(12, 4, 'SpO2 Sensor', '99', '2026-05-06 19:41:58'),
(13, 4, 'Blood Pressure Sensor', '124/84', '2026-05-06 19:42:00'),
(14, 4, 'Height Sensor', '162.4', '2026-05-06 19:42:02'),
(15, 4, 'Weight Sensor', '56.4', '2026-05-06 19:42:04'),
(16, 4, 'BMI Calculation', '21.4 - Normal', '2026-05-06 19:42:05'),
(17, 5, 'Temperature Sensor', '36.6', '2026-05-06 19:49:51'),
(18, 5, 'Heart Rate Sensor', '84', '2026-05-06 19:49:53'),
(19, 5, 'SpO2 Sensor', '96', '2026-05-06 19:49:53'),
(20, 5, 'Blood Pressure Sensor', '123/73', '2026-05-06 19:49:54'),
(21, 5, 'Height Sensor', '167.6', '2026-05-06 19:49:56'),
(22, 5, 'Weight Sensor', '68.2', '2026-05-06 19:49:57'),
(23, 5, 'BMI Calculation', '24.3 - Normal', '2026-05-06 19:49:58'),
(24, 7, 'Temperature Sensor', '36.5', '2026-05-06 20:07:23'),
(25, 7, 'Heart Rate Sensor', '89', '2026-05-06 20:07:25'),
(26, 7, 'SpO2 Sensor', '97', '2026-05-06 20:07:25'),
(27, 7, 'Blood Pressure Sensor', '123/83', '2026-05-06 20:07:26'),
(28, 7, 'Height Sensor', '168.9', '2026-05-06 20:07:27'),
(29, 7, 'Weight Sensor', '58.3', '2026-05-06 20:07:29'),
(30, 7, 'BMI Calculation', '20.4 - Normal', '2026-05-06 20:07:35'),
(31, 8, 'Temperature Sensor', '37.1', '2026-05-06 20:16:52'),
(32, 8, 'Heart Rate Sensor', '84', '2026-05-06 20:16:53'),
(33, 8, 'SpO2 Sensor', '97', '2026-05-06 20:16:53'),
(34, 8, 'Blood Pressure Sensor', '117/79', '2026-05-06 20:16:54'),
(35, 8, 'Height Sensor', '168.8', '2026-05-06 20:16:55'),
(36, 8, 'Weight Sensor', '52.2', '2026-05-06 20:16:57'),
(37, 8, 'BMI Calculation', '18.3 - Underweight', '2026-05-06 20:16:58'),
(38, 9, 'Temperature Sensor', '37.0', '2026-05-10 21:27:07'),
(39, 9, 'Heart Rate Sensor', '71', '2026-05-10 21:27:09'),
(40, 9, 'SpO2 Sensor', '97', '2026-05-10 21:27:09'),
(41, 9, 'Blood Pressure Sensor', '110/72', '2026-05-10 21:27:10'),
(42, 9, 'Height Sensor', '174.9', '2026-05-10 21:27:11'),
(43, 9, 'Weight Sensor', '66.9', '2026-05-10 21:27:12'),
(44, 9, 'BMI Calculation', '21.9 - Normal', '2026-05-10 21:27:13'),
(45, 10, 'Temperature Sensor', '36.6', '2026-05-15 19:03:06'),
(46, 10, 'Heart Rate Sensor', '93', '2026-05-15 19:03:07'),
(47, 10, 'SpO2 Sensor', '98', '2026-05-15 19:03:07'),
(48, 10, 'Blood Pressure Sensor', '116/79', '2026-05-15 19:03:09'),
(49, 10, 'Height Sensor', '177.4', '2026-05-15 19:03:10'),
(50, 10, 'Weight Sensor', '69.7', '2026-05-15 19:03:11'),
(51, 10, 'BMI Calculation', '22.1 - Normal', '2026-05-15 19:03:12'),
(52, 11, 'Temperature Sensor', '36.5', '2026-05-15 19:17:32'),
(53, 11, 'Heart Rate Sensor', '72', '2026-05-15 19:17:33'),
(54, 11, 'SpO2 Sensor', '97', '2026-05-15 19:17:33'),
(55, 11, 'Blood Pressure Sensor', '116/76', '2026-05-15 19:17:34'),
(56, 11, 'Height Sensor', '169.8', '2026-05-15 19:17:36'),
(57, 11, 'Weight Sensor', '60.2', '2026-05-15 19:17:37'),
(58, 11, 'BMI Calculation', '20.9 - Normal', '2026-05-15 19:17:38'),
(59, 12, 'Temperature Sensor', '36.5', '2026-05-15 19:22:52'),
(60, 12, 'Heart Rate Sensor', '92', '2026-05-15 19:22:53'),
(61, 12, 'SpO2 Sensor', '97', '2026-05-15 19:22:53'),
(62, 12, 'Blood Pressure Sensor', '121/74', '2026-05-15 19:22:54'),
(63, 12, 'Height Sensor', '155.1', '2026-05-15 19:22:56'),
(64, 12, 'Weight Sensor', '64.5', '2026-05-15 19:22:57'),
(65, 12, 'BMI Calculation', '26.8 - Overweight', '2026-05-15 19:22:58'),
(66, 13, 'Temperature Sensor', '36.6', '2026-05-15 19:27:35'),
(67, 13, 'Heart Rate Sensor', '86', '2026-05-15 19:27:36'),
(68, 13, 'SpO2 Sensor', '96', '2026-05-15 19:27:36'),
(69, 13, 'Blood Pressure Sensor', '112/85', '2026-05-15 19:27:38'),
(70, 13, 'Height Sensor', '170.2', '2026-05-15 19:27:38'),
(71, 13, 'Weight Sensor', '68.0', '2026-05-15 19:27:39'),
(72, 13, 'BMI Calculation', '23.5 - Normal', '2026-05-15 19:27:41'),
(73, 16, 'Temperature Sensor', '36.5', '2026-05-15 23:54:51'),
(74, 16, 'Heart Rate Sensor', '96', '2026-05-15 23:54:52'),
(75, 16, 'SpO2 Sensor', '98', '2026-05-15 23:54:52'),
(76, 16, 'Blood Pressure Sensor', '125/78', '2026-05-15 23:54:56'),
(77, 16, 'Height Sensor', '161.1', '2026-05-15 23:54:57'),
(78, 16, 'Weight Sensor', '72.2', '2026-05-15 23:54:59'),
(79, 16, 'BMI Calculation', '27.8 - Overweight', '2026-05-15 23:55:00'),
(80, 17, 'Temperature Sensor', '36.8', '2026-05-15 23:56:24'),
(81, 17, 'Heart Rate Sensor', '76', '2026-05-15 23:56:25'),
(82, 17, 'SpO2 Sensor', '98', '2026-05-15 23:56:25'),
(83, 17, 'Blood Pressure Sensor', '113/85', '2026-05-15 23:56:27'),
(84, 17, 'Height Sensor', '175.0', '2026-05-15 23:56:28'),
(85, 17, 'Weight Sensor', '69.6', '2026-05-15 23:56:30'),
(86, 17, 'BMI Calculation', '22.7 - Normal', '2026-05-15 23:56:31'),
(87, 18, 'Temperature Sensor', '36.4', '2026-05-16 00:35:36'),
(88, 18, 'Heart Rate Sensor', '94', '2026-05-16 00:35:46'),
(89, 18, 'SpO2 Sensor', '97', '2026-05-16 00:35:46'),
(90, 18, 'Blood Pressure Sensor', '124/82', '2026-05-16 00:35:48'),
(91, 18, 'Height Sensor', '176.1', '2026-05-16 00:35:49'),
(92, 18, 'Weight Sensor', '65.2', '2026-05-16 00:35:50'),
(93, 18, 'BMI Calculation', '21.0 - Normal', '2026-05-16 00:35:55');

-- --------------------------------------------------------

--
-- Table structure for table `system_logs`
--

CREATE TABLE `system_logs` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `activity` varchar(255) NOT NULL,
  `system_event` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_logs`
--

INSERT INTO `system_logs` (`log_id`, `user_id`, `activity`, `system_event`, `timestamp`) VALUES
(1, 1, 'Patient check-up started', 'New patient record created', '2026-05-06 19:27:05'),
(2, 2, 'Patient check-up started', 'New patient record created', '2026-05-06 19:27:51'),
(3, 3, 'Patient check-up started', 'New patient record created', '2026-05-06 19:34:34'),
(4, 4, 'Patient check-up started', 'New patient record created', '2026-05-06 19:41:54'),
(5, 4, 'Health results viewed', 'Final health status generated', '2026-05-06 19:42:07'),
(6, 5, 'Patient check-up started', 'New patient record created', '2026-05-06 19:49:49'),
(7, 5, 'Health results viewed', 'Final health status generated', '2026-05-06 19:50:01'),
(8, 6, 'Patient check-up started', 'New patient record created', '2026-05-06 19:52:55'),
(9, 7, 'Patient check-up started', 'New patient record created', '2026-05-06 20:07:23'),
(10, 7, 'temperature measured', 'Measurement saved successfully', '2026-05-06 20:07:23'),
(11, 7, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-06 20:07:25'),
(12, 7, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-06 20:07:26'),
(13, 7, 'height measured', 'Measurement saved successfully', '2026-05-06 20:07:27'),
(14, 7, 'weight measured', 'Measurement saved successfully', '2026-05-06 20:07:29'),
(15, 7, 'bmi measured', 'Measurement saved successfully', '2026-05-06 20:07:35'),
(16, 7, 'Health results viewed', 'Final health status generated', '2026-05-06 20:07:36'),
(17, 8, 'Patient check-up started', 'New patient record created', '2026-05-06 20:16:51'),
(18, 8, 'temperature measured', 'Measurement saved successfully', '2026-05-06 20:16:52'),
(19, 8, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-06 20:16:53'),
(20, 8, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-06 20:16:54'),
(21, 8, 'height measured', 'Measurement saved successfully', '2026-05-06 20:16:55'),
(22, 8, 'weight measured', 'Measurement saved successfully', '2026-05-06 20:16:57'),
(23, 8, 'bmi measured', 'Measurement saved successfully', '2026-05-06 20:16:58'),
(24, 8, 'Health results viewed', 'Final health status generated', '2026-05-06 20:16:59'),
(25, 9, 'Patient check-up started', 'New patient record created', '2026-05-10 21:27:06'),
(26, 9, 'temperature measured', 'Measurement saved successfully', '2026-05-10 21:27:07'),
(27, 9, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-10 21:27:09'),
(28, 9, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-10 21:27:10'),
(29, 9, 'height measured', 'Measurement saved successfully', '2026-05-10 21:27:11'),
(30, 9, 'weight measured', 'Measurement saved successfully', '2026-05-10 21:27:12'),
(31, 9, 'bmi measured', 'Measurement saved successfully', '2026-05-10 21:27:13'),
(32, 9, 'Health results viewed', 'Final health status generated', '2026-05-10 21:27:14'),
(33, 10, 'Patient check-up started', 'New patient record created', '2026-05-15 19:03:05'),
(34, 10, 'temperature measured', 'Measurement saved successfully', '2026-05-15 19:03:06'),
(35, 10, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-15 19:03:07'),
(36, 10, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-15 19:03:09'),
(37, 10, 'height measured', 'Measurement saved successfully', '2026-05-15 19:03:10'),
(38, 10, 'weight measured', 'Measurement saved successfully', '2026-05-15 19:03:11'),
(39, 10, 'bmi measured', 'Measurement saved successfully', '2026-05-15 19:03:12'),
(40, 10, 'Health results viewed', 'Final health status generated', '2026-05-15 19:03:14'),
(41, 11, 'Patient check-up started', 'New patient record created', '2026-05-15 19:17:31'),
(42, 11, 'temperature measured', 'Measurement saved successfully', '2026-05-15 19:17:32'),
(43, 11, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-15 19:17:33'),
(44, 11, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-15 19:17:34'),
(45, 11, 'height measured', 'Measurement saved successfully', '2026-05-15 19:17:36'),
(46, 11, 'weight measured', 'Measurement saved successfully', '2026-05-15 19:17:37'),
(47, 11, 'bmi measured', 'Measurement saved successfully', '2026-05-15 19:17:38'),
(48, 11, 'Health results viewed', 'Final health status generated', '2026-05-15 19:17:39'),
(49, 12, 'Patient check-up started', 'New patient record created', '2026-05-15 19:22:52'),
(50, 12, 'temperature measured', 'Measurement saved successfully', '2026-05-15 19:22:52'),
(51, 12, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-15 19:22:53'),
(52, 12, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-15 19:22:54'),
(53, 12, 'height measured', 'Measurement saved successfully', '2026-05-15 19:22:56'),
(54, 12, 'weight measured', 'Measurement saved successfully', '2026-05-15 19:22:57'),
(55, 12, 'bmi measured', 'Measurement saved successfully', '2026-05-15 19:22:58'),
(56, 12, 'Health results viewed', 'Final health status generated', '2026-05-15 19:23:00'),
(57, 13, 'Patient check-up started', 'New patient record created', '2026-05-15 19:27:34'),
(58, 13, 'temperature measured', 'Measurement saved successfully', '2026-05-15 19:27:35'),
(59, 13, 'heart_spo2 measured', 'Measurement saved successfully', '2026-05-15 19:27:36'),
(60, 13, 'blood_pressure measured', 'Measurement saved successfully', '2026-05-15 19:27:38'),
(61, 13, 'height measured', 'Measurement saved successfully', '2026-05-15 19:27:38'),
(62, 13, 'weight measured', 'Measurement saved successfully', '2026-05-15 19:27:39'),
(63, 13, 'bmi measured', 'Measurement saved successfully', '2026-05-15 19:27:41'),
(64, 13, 'Health results viewed', 'Final health status generated', '2026-05-15 19:27:42'),
(65, 14, 'Patient check-up started', 'New patient record created', '2026-05-15 19:33:47'),
(66, 7, 'Health results viewed', 'Final health status generated', '2026-05-15 20:33:07'),
(67, 8, 'Health results viewed', 'Final health status generated', '2026-05-15 20:33:45'),
(68, 9, 'Health results viewed', 'Final health status generated', '2026-05-15 20:35:21'),
(69, 16, 'Health results viewed', 'Final health status generated', '2026-05-15 23:55:02'),
(70, 15, 'Patient record printed', 'Record ID 15 printed from admin dashboard', '2026-05-16 00:23:30'),
(71, 17, 'Patient record printed', 'Record ID 17 printed from admin dashboard', '2026-05-16 00:26:09'),
(72, 16, 'Patient record printed', 'Record ID 16 printed from admin dashboard', '2026-05-16 00:26:19'),
(73, 17, 'Patient record printed', 'Record ID 17 printed from admin dashboard', '2026-05-16 00:33:15');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT 'patient',
  `session_timestamp` datetime DEFAULT current_timestamp(),
  `full_name` varchar(150) NOT NULL,
  `age` int(11) NOT NULL,
  `sex` varchar(20) NOT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `student_id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `role`, `session_timestamp`, `full_name`, `age`, `sex`, `contact`, `student_id`) VALUES
(1, 'lors', NULL, 'patient', '2026-05-06 19:27:05', 'lors', 21, 'Male', '09949677824', NULL),
(2, 'lors', NULL, 'patient', '2026-05-06 19:27:51', 'lors', 21, 'Male', '09949677824', NULL),
(3, 'lors', NULL, 'patient', '2026-05-06 19:34:34', 'lors', 21, 'Male', '09949677824', NULL),
(4, 'prans', NULL, 'patient', '2026-05-06 19:41:54', 'prans', 21, 'Male', '123123', NULL),
(5, 'debid', NULL, 'patient', '2026-05-06 19:49:49', 'debid', 21, 'Male', '09124212424', NULL),
(6, 'non', NULL, 'patient', '2026-05-06 19:52:55', 'non', 12, 'Male', '09124212424', NULL),
(7, 'bogart', NULL, 'patient', '2026-05-06 20:07:23', 'bogart', 15, 'Female', '09124212424', NULL),
(8, 'bogart', NULL, 'patient', '2026-05-06 20:16:51', 'bogart', 99, 'Male', '09124212424', NULL),
(9, 'lors', NULL, 'patient', '2026-05-10 21:27:06', 'lors', 12, 'Male', '01293912323', NULL),
(10, 'laurenze villanueva', NULL, 'patient', '2026-05-15 19:03:05', 'laurenze villanueva', 21, 'Male', '09949677824', '23-39230'),
(11, 'laurenze villanueva', NULL, 'patient', '2026-05-15 19:17:31', 'laurenze villanueva', 21, 'Male', '09949677824', '23-39230'),
(12, 'laurenze villanueva', NULL, 'patient', '2026-05-15 19:22:52', 'laurenze villanueva', 21, 'Male', '09949677824', '23-39230'),
(13, 'laurenze villanueva', NULL, 'patient', '2026-05-15 19:27:34', 'laurenze villanueva', 21, 'Male', '09949677824', ''),
(14, 'laurenze villanueva', NULL, 'patient', '2026-05-15 19:33:47', 'laurenze villanueva', 100, 'Male', '09949677824', '23-39230'),
(15, 'laurenze villanueva', NULL, 'patient', '2026-05-15 23:50:35', 'laurenze villanueva', 21, 'Male', '09949677824', '23-39230'),
(16, 'kenneth barte', NULL, 'patient', '2026-05-15 23:54:50', 'kenneth barte', 21, 'Male', '09912399213', '23-39234'),
(17, 'kenneth barte', NULL, 'patient', '2026-05-15 23:56:23', 'kenneth barte', 12, 'Male', '09949677824', '23-39234'),
(18, 'athina mojares', NULL, 'patient', '2026-05-16 00:35:35', 'athina mojares', 100, 'Female', '09123123232', '23-49242');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `health_records`
--
ALTER TABLE `health_records`
  ADD PRIMARY KEY (`record_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `qr_code_records`
--
ALTER TABLE `qr_code_records`
  ADD PRIMARY KEY (`qr_id`),
  ADD KEY `record_id` (`record_id`);

--
-- Indexes for table `sensor_data`
--
ALTER TABLE `sensor_data`
  ADD PRIMARY KEY (`sensor_data_id`),
  ADD KEY `record_id` (`record_id`);

--
-- Indexes for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `health_records`
--
ALTER TABLE `health_records`
  MODIFY `record_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `qr_code_records`
--
ALTER TABLE `qr_code_records`
  MODIFY `qr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `sensor_data`
--
ALTER TABLE `sensor_data`
  MODIFY `sensor_data_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `health_records`
--
ALTER TABLE `health_records`
  ADD CONSTRAINT `health_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `qr_code_records`
--
ALTER TABLE `qr_code_records`
  ADD CONSTRAINT `qr_code_records_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `health_records` (`record_id`);

--
-- Constraints for table `sensor_data`
--
ALTER TABLE `sensor_data`
  ADD CONSTRAINT `sensor_data_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `health_records` (`record_id`);

--
-- Constraints for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
