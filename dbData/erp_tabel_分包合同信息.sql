CREATE DATABASE  IF NOT EXISTS `erp` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `erp`;
-- MySQL dump 10.13  Distrib 5.7.21, for Linux (i686)
--
-- Host: localhost    Database: erp
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tabel_分包合同信息`
--

DROP TABLE IF EXISTS `tabel_分包合同信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_分包合同信息` (
  `分包合同识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `立项识别码` bigint(20) DEFAULT NULL,
  `合同识别码` bigint(20) DEFAULT NULL,
  `分包合同编号` varchar(255) DEFAULT NULL,
  `分包合同名称` varchar(255) DEFAULT NULL,
  `分包合同主要内容` varchar(255) DEFAULT NULL,
  `分包合同类别` varchar(255) DEFAULT NULL,
  `甲方识别码` bigint(20) DEFAULT NULL,
  `乙方识别码` bigint(20) DEFAULT NULL,
  `丙方识别码` bigint(20) DEFAULT NULL,
  `丁方识别码` bigint(20) DEFAULT NULL,
  `分包合同签订时间` date DEFAULT NULL,
  `分包合同值_签订时` decimal(12,2) DEFAULT NULL,
  `分包合同值_最新值` decimal(12,2) DEFAULT NULL,
  `分包合同值_最终值` decimal(12,2) DEFAULT NULL,
  `分包合同备注` longtext,
  PRIMARY KEY (`分包合同识别码`),
  UNIQUE KEY `分包合同编号` (`分包合同编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_分包合同信息`
--

LOCK TABLES `tabel_分包合同信息` WRITE;
/*!40000 ALTER TABLE `tabel_分包合同信息` DISABLE KEYS */;
/*!40000 ALTER TABLE `tabel_分包合同信息` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-01 19:30:31
