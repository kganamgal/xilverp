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
-- Table structure for table `tabel_招标信息`
--

DROP TABLE IF EXISTS `tabel_招标信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_招标信息` (
  `招标识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `立项识别码` bigint(20) DEFAULT NULL,
  `招标方式` varchar(255) DEFAULT NULL,
  `招标单位识别码` bigint(20) DEFAULT NULL,
  `招标代理识别码` bigint(20) DEFAULT NULL,
  `预算控制价` decimal(12,2) DEFAULT NULL,
  `招标文件定稿时间` date DEFAULT NULL,
  `公告邀请函发出时间` date DEFAULT NULL,
  `开标时间` date DEFAULT NULL,
  `中标通知书发出时间` date DEFAULT NULL,
  `中标单位识别码` bigint(20) DEFAULT NULL,
  `中标价` decimal(12,2) DEFAULT NULL,
  `招标备注` longtext,
  `招标简介` longtext,
  `投标单位` longtext,
  PRIMARY KEY (`招标识别码`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_招标信息`
--

LOCK TABLES `tabel_招标信息` WRITE;
/*!40000 ALTER TABLE `tabel_招标信息` DISABLE KEYS */;
INSERT INTO `tabel_招标信息` VALUES (1,9,'竞争性谈判',4,NULL,660000.00,'2018-03-27',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,10,'竞争性磋商',1,NULL,1200000.00,'2018-03-01',NULL,NULL,NULL,NULL,NULL,NULL,'会计事务所',NULL),(4,10,'竞争性磋商',1,NULL,600000.00,'2018-03-02',NULL,NULL,NULL,NULL,NULL,NULL,'律师事务所',NULL);
/*!40000 ALTER TABLE `tabel_招标信息` ENABLE KEYS */;
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
