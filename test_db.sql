-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2026 at 07:05 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('479d61e5fce1');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `name`, `email`, `address`, `phone`, `mobile`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 'Ali Ahmed', 'ali@test.com', NULL, '12345678', NULL, '2025-12-19 23:23:54', 1, '2026-01-07 12:49:38', 1),
(2, 'Sara Mohammed', 'sara@test.com', NULL, '123456789', NULL, '2025-12-19 23:23:54', 1, '2026-01-07 12:49:38', 1),
(3, 'aa', 'min@test.com', 'tai', '123456780', '0771821482', '2026-01-07 21:59:44', 4, NULL, 4);

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

CREATE TABLE `invoices` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `invoice_date` datetime DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`id`, `customer_id`, `invoice_date`, `total_amount`, `status`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(23, 2, '2025-12-23 01:59:59', 3500, 'paid', '2025-12-23 01:59:59', 1, '2026-01-07 12:49:38', 1),
(24, 1, '2025-12-23 02:13:36', 3500, 'pending', '2025-12-23 02:13:36', 4, '2025-12-23 02:13:37', 4),
(29, 1, '2026-01-07 21:19:13', 1200, 'pending', '2026-01-07 21:19:13', 4, '2026-01-07 21:19:13', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `invoice_products`
--

CREATE TABLE `invoice_products` (
  `id` int(11) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `invoice_products`
--

INSERT INTO `invoice_products` (`id`, `invoice_id`, `product_id`, `quantity`, `amount`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(14, 23, 1, 1, 3500, '2025-12-23 01:59:59', 1, '2026-01-07 12:49:38', 1),
(15, 24, 1, 1, 3500, '2025-12-23 02:13:37', 1, '2026-01-07 12:49:38', 1),
(16, 29, 3, 4, 1200, '2026-01-07 21:19:13', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `can_create` tinyint(1) DEFAULT NULL,
  `can_read` tinyint(1) DEFAULT NULL,
  `can_update` tinyint(1) DEFAULT NULL,
  `can_delete` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `role_id`, `model_name`, `can_create`, `can_read`, `can_update`, `can_delete`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(20, 1, 'User', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(21, 1, 'Customer', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(22, 1, 'Product', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(23, 1, 'Invoice', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(24, 1, 'Role', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(25, 1, 'Permission', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(26, 2, 'User', 0, 1, 1, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(27, 2, 'Customer', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(28, 2, 'Product', 1, 1, 1, 1, '2026-01-07 13:07:17', NULL, NULL, NULL),
(29, 2, 'Invoice', 1, 1, 1, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(30, 2, 'Role', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(31, 2, 'Permission', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(32, 5, 'User', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(33, 5, 'Customer', 1, 1, 1, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(34, 5, 'Product', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(35, 5, 'Invoice', 1, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(36, 5, 'Role', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(37, 5, 'Permission', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(38, 3, 'User', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(39, 3, 'Customer', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(40, 3, 'Product', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(41, 3, 'Invoice', 1, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(42, 3, 'Role', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL),
(43, 3, 'Permission', 0, 1, 0, 0, '2026-01-07 13:07:17', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `price`, `quantity`, `description`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 'Laptop', 3500, 9, '', '2025-12-19 23:26:50', 1, '2026-01-07 12:50:04', NULL),
(2, 'Mouse', 120.22, 30, '', '2025-12-19 23:26:50', 1, '2026-01-07 12:49:38', 1),
(3, 'Keyboard', 300, 38, '', '2025-12-19 23:26:50', 1, '2026-01-07 21:19:13', 1),
(4, 'pen', 20, 4, 'help student', '2026-01-07 08:07:04', 1, '2026-01-07 12:49:38', 1),
(8, 'car', 22000, 10, 'good', '2026-01-07 08:38:24', 1, '2026-01-07 12:49:38', 1),
(9, 'ss', 20, 22, '', '2026-01-07 08:48:47', 1, '2026-01-07 12:49:38', 1),
(10, 'd', 222, 1, '', '2026-01-07 08:54:16', 1, '2026-01-07 12:49:38', 1),
(11, 'pencile', 30, 2, '', '2026-01-07 12:26:20', 1, '2026-01-07 12:49:38', 1),
(12, 'pe', 22, 10, '', '2026-01-07 21:26:24', 4, NULL, 4),
(13, 'd', 22, 2, '', '2026-01-07 21:26:39', 4, NULL, 4),
(14, 'c', 10, 11, '', '2026-01-07 21:29:38', 4, NULL, 4),
(15, 'h', 1, 11, 'ss', '2026-01-07 21:39:06', 4, NULL, 4);

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `parent_role_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `status`, `parent_role_id`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 'Admin', 1, NULL, '2025-12-19 23:18:40', 1, '2026-01-07 12:49:38', 1),
(2, 'Sales Manager', 1, 1, '2025-12-19 23:18:40', 1, '2026-01-07 12:49:38', 1),
(3, 'Cashier', 1, 4, '2025-12-19 23:18:40', 1, '2026-01-07 12:49:38', 1),
(4, 'Employee', 1, 2, '2025-12-19 23:18:40', 1, '2026-01-07 12:49:38', 1),
(5, 'Sales Employee', 1, 2, '2026-01-07 13:07:17', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `status`, `role_id`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 'Admin User', 'admin@test.com', 'scrypt:32768:8:1$GyrvDeBxbd02BpIW$cdde94c935c08a08870cba94a6c2e7ddd8c289b9fd078745257b3b8889786e1e66352c4f1914af23e04c6e473dc98fed1b3e4eb4567afeb82ed1e706e182ac0e', 1, 1, '2025-12-19 23:21:00', 1, '2026-01-07 13:08:45', 1),
(2, 'Manager User', 'manager@test.com', 'scrypt:32768:8:1$MhEnd9YF1ARexL2i$2b9e15adf78f371d056378233f88722ab7174dd663952cd64d17aaa49e3dc6d58cb6450d4e470347688d8eda5f7b52fcb8051fc9239622fde913d2a5358025f4', 1, 2, '2025-12-19 23:21:00', 1, '2026-01-07 12:49:38', 1),
(3, 'Cashier User', 'cashier@test.com', 'scrypt:32768:8:1$Ca62iiHrPPmOTHoH$434c4be8baeefce8d082bcdd86b72c36ddc5ae848dffd1b19169008e3af1db75bb94424362f798387c456b97e38cdc9146629f9ceb2354af7ef066372237e805', 1, 3, '2025-12-19 23:21:00', 1, '2026-01-07 12:49:38', 1),
(4, 'dmin', 'dmin@test.com', 'scrypt:32768:8:1$jOphu2MvUfa69x6h$55cb52d063250ca0cf2a9586ea59a4d5d43249001889796e00f8b81bcc084294d5c2b67fd27adbdd3b572dcbb0b4a62876b2478d21d2e111d4bf51aa6a9458db', 1, 1, '2025-12-22 22:53:25', 1, '2026-01-07 12:49:38', 1),
(5, 'Sample Sales Employee', 'employee@test.com', 'scrypt:32768:8:1$05fXzUSqRRw2Pfsg$27ddb6d1e5f3db78d1213b1b795480c59cc51cf1c2926c4ae18694ccd28e631464c5d37ab3c62f90d3e561fd4e9aad6ab8dfd2248330377de1ba6d1e67dfd401', 1, 5, '2026-01-07 13:07:17', NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `invoice_products`
--
ALTER TABLE `invoice_products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `invoice_id` (`invoice_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_role_id` (`parent_role_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `invoice_products`
--
ALTER TABLE `invoice_products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

--
-- Constraints for table `invoice_products`
--
ALTER TABLE `invoice_products`
  ADD CONSTRAINT `invoice_products_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoices` (`id`),
  ADD CONSTRAINT `invoice_products_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `permissions`
--
ALTER TABLE `permissions`
  ADD CONSTRAINT `permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `roles`
--
ALTER TABLE `roles`
  ADD CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`parent_role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
