-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2025 at 07:38 PM
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
-- Database: `leo`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `comment` varchar(500) NOT NULL,
  `commentedBy` varchar(100) NOT NULL,
  `commentedOn` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`comment_id`, `post_id`, `comment`, `commentedBy`, `commentedOn`) VALUES
(1, 8, '', 'siva kumar', '2025-03-23 10:57:53.785662'),
(2, 9, '', 'siva kumar', '2025-03-23 10:58:26.670686');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `contact_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `friends`
--

CREATE TABLE `friends` (
  `friends_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `request_id` int(11) NOT NULL,
  `isAccepted` varchar(10) NOT NULL DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `friends`
--

INSERT INTO `friends` (`friends_id`, `user_id`, `request_id`, `isAccepted`) VALUES
(1, 6, 4, 'True'),
(5, 6, 6, 'True'),
(6, 6, 1, 'False'),
(7, 7, 6, 'False');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(500) NOT NULL,
  `image` varchar(500) NOT NULL,
  `date` date DEFAULT current_timestamp(),
  `time` time NOT NULL,
  `likes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_id`, `email`, `name`, `title`, `description`, `image`, `date`, `time`, `likes`) VALUES
(8, 'ss@gmail.com', 'siva kumar', 'school', 'moment', 'IMG-20210422-WA0105.jpg', '2025-03-19', '00:00:00', 2),
(9, 'ss@gmail.com', 'siva kumar', 'jygjgj', 'htffhgvh', 'pexels-stein-egil-liland-1933239.jpg', '2025-03-19', '00:00:00', 1),
(10, 'ss@gmail.com', 'siva kumar', 'ugk', 'jhgja', 'pexels-pixabay-36717.jpg', '2025-03-22', '18:31:34', 2),
(11, 'leo@gmail.com', 'leo das', 'qwer', 'popiu', 'pic11.JPG', '2025-05-03', '20:31:27', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `signup`
--

CREATE TABLE `signup` (
  `id` int(11) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `phone_no` varchar(10) NOT NULL,
  `profileimage` varchar(500) NOT NULL DEFAULT 'profile.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `signup`
--

INSERT INTO `signup` (`id`, `firstname`, `lastname`, `email`, `password`, `phone_no`, `profileimage`) VALUES
(1, 'Subramaniya', 'siva', 'ak@gmail.com', 'qwer', '2147483647', 'profile.jpg'),
(4, 'bala', 'vijay', 'ss@gmail.com', 'scrypt:32768:8:1$y3Znq4l8vnFyJS05$44858678870a71754a0bc2eba8a1659fc54da71e2fd746f005daa799af50b76d103939d2404d6f92f61edb0ce434cb56d91bad3958dc743783d20d0caee7bc9a', '2147483647', 'profile.jpg'),
(5, 'akash', 'siva', 'sss@gmail.com', 'scrypt:32768:8:1$eiyK0alzgJQlUPY1$fad624b0013536afff820e9b9277c9c11e3c2ff2bf9f496b1d4d2d540c88458d66ce3194cf56895f65297e08202644e12b39d9b69270efc4acee85e2af17ce50', '2147483647', 'profile.jpg'),
(6, 'leo', 'das', 'leo@gmail.com', 'scrypt:32768:8:1$3Ko4drkUBZEodYuQ$1e830f19e55a02d11ab86134db17d9475479bc31b63ec68bb078fa4c83a54afa7402bfaeb5410b68e312f32c206bd48c941c534f0d409524312a95a59faeb317', '9489581762', 'pic12.JPG'),
(7, 'vikram', 'vedha', 'www@gmail.com', 'scrypt:32768:8:1$ESXNsKsHZtc24lyn$464e6d5187a3b478d136c8e42f54a2f4a1487ce0a668bd1f7e1da5a7765fb6fe1a11db64188aa8cf6f8d51b4b49cbfd1aa0c961a100a4197bdf459195b621f32', '9809809833', 'profile.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`contact_id`);

--
-- Indexes for table `friends`
--
ALTER TABLE `friends`
  ADD PRIMARY KEY (`friends_id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_id`);

--
-- Indexes for table `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `friends`
--
ALTER TABLE `friends`
  MODIFY `friends_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `signup`
--
ALTER TABLE `signup`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
