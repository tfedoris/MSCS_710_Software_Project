CREATE DATABASE `waruserinfo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE waruserinfo;

CREATE TABLE `registration_info` (
  `user_id` varchar(40) NOT NULL,
  `registration_id` varchar(40) NOT NULL,
  `public_key` varchar(2000) NOT NULL,
  `private_key` varchar(4000) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
