-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 06, 2026 at 05:04 PM
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
(8, 8, 37.10, 84, 97, '117/79', 168.80, 52.20, 18.30, 'Underweight', 'Needs Review', '2026-05-06 20:16:51');

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
(8, 8, 'HC-8-833dc0c0', '2026-05-06 20:16:51');

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
(37, 8, 'BMI Calculation', '18.3 - Underweight', '2026-05-06 20:16:58');

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
(24, 8, 'Health results viewed', 'Final health status generated', '2026-05-06 20:16:59');

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
  `branch` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `role`, `session_timestamp`, `full_name`, `age`, `sex`, `contact`, `branch`) VALUES
(1, 'lors', NULL, 'patient', '2026-05-06 19:27:05', 'lors', 21, 'Male', '09949677824', 'bsu lipa'),
(2, 'lors', NULL, 'patient', '2026-05-06 19:27:51', 'lors', 21, 'Male', '09949677824', 'bsu lipa'),
(3, 'lors', NULL, 'patient', '2026-05-06 19:34:34', 'lors', 21, 'Male', '09949677824', 'bsu lipa'),
(4, 'prans', NULL, 'patient', '2026-05-06 19:41:54', 'prans', 21, 'Male', '123123', 'bsu lipa'),
(5, 'debid', NULL, 'patient', '2026-05-06 19:49:49', 'debid', 21, 'Male', '09124212424', 'bsu lipa'),
(6, 'non', NULL, 'patient', '2026-05-06 19:52:55', 'non', 12, 'Male', '09124212424', 'bsu lipa'),
(7, 'bogart', NULL, 'patient', '2026-05-06 20:07:23', 'bogart', 15, 'Female', '09124212424', 'bsu lipa'),
(8, 'bogart', NULL, 'patient', '2026-05-06 20:16:51', 'bogart', 99, 'Male', '09124212424', 'bsu lipa');

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT for table `health_records`
--
ALTER TABLE `health_records`
  MODIFY `record_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `qr_code_records`
--
ALTER TABLE `qr_code_records`
  MODIFY `qr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `sensor_data`
--
ALTER TABLE `sensor_data`
  MODIFY `sensor_data_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
