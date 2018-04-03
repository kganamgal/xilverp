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
-- Table structure for table `tabel_付款信息`
--

DROP TABLE IF EXISTS `tabel_付款信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_付款信息` (
  `付款识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `付款登记时间` date DEFAULT NULL,
  `付款支付时间` date DEFAULT NULL,
  `立项识别码` bigint(20) DEFAULT NULL,
  `合同识别码` bigint(20) DEFAULT NULL,
  `付款事由` longtext,
  `付款单位识别码` bigint(20) DEFAULT NULL,
  `收款单位识别码` bigint(20) DEFAULT NULL,
  `预算识别码` bigint(20) DEFAULT NULL,
  `付款时预算总额` decimal(12,2) DEFAULT NULL,
  `付款时项目概算` decimal(12,2) DEFAULT NULL,
  `付款时合同付款上限` decimal(12,2) DEFAULT NULL,
  `付款时合同值` decimal(12,2) DEFAULT NULL,
  `付款时预算余额` decimal(12,2) DEFAULT NULL,
  `付款时概算余额` decimal(12,2) DEFAULT NULL,
  `付款时合同可付余额` decimal(12,2) DEFAULT NULL,
  `付款时合同未付额` decimal(12,2) DEFAULT NULL,
  `付款时预算已付额` decimal(12,2) DEFAULT NULL,
  `付款时合同已付额` decimal(12,2) DEFAULT NULL,
  `付款时概算已付额` decimal(12,2) DEFAULT NULL,
  `付款时形象进度` longtext,
  `本次付款额` decimal(12,2) DEFAULT NULL,
  `付款备注` longtext,
  PRIMARY KEY (`付款识别码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_付款信息`
--

LOCK TABLES `tabel_付款信息` WRITE;
/*!40000 ALTER TABLE `tabel_付款信息` DISABLE KEYS */;
/*!40000 ALTER TABLE `tabel_付款信息` ENABLE KEYS */;
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
