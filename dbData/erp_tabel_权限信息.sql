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
-- Table structure for table `tabel_权限信息`
--

DROP TABLE IF EXISTS `tabel_权限信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_权限信息` (
  `DB_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `用户名` varchar(255) NOT NULL,
  `查看数据概览` smallint(6) DEFAULT NULL,
  `查看单位信息` smallint(6) DEFAULT NULL,
  `查看立项信息` smallint(6) DEFAULT NULL,
  `查看招标信息` smallint(6) DEFAULT NULL,
  `查看合同信息` smallint(6) DEFAULT NULL,
  `查看预算信息` smallint(6) DEFAULT NULL,
  `查看付款信息` smallint(6) DEFAULT NULL,
  `查看变更信息` smallint(6) DEFAULT NULL,
  `查看分包合同信息` smallint(6) DEFAULT NULL,
  `操作单位信息` smallint(6) DEFAULT NULL,
  `允许操作立项的项目` varchar(255) DEFAULT NULL,
  `允许操作招标的项目` varchar(255) DEFAULT NULL,
  `允许操作合同的项目` varchar(255) DEFAULT NULL,
  `操作预算信息` smallint(6) DEFAULT NULL,
  `允许操作付款的项目` varchar(255) DEFAULT NULL,
  `允许操作变更的项目` varchar(255) DEFAULT NULL,
  `允许操作分包合同的项目` varchar(255) DEFAULT NULL,
  `允许调整概算的项目` varchar(255) DEFAULT NULL,
  `允许调整合同额的项目` varchar(255) DEFAULT NULL,
  `删除付款信息` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`DB_id`),
  UNIQUE KEY `用户名` (`用户名`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_权限信息`
--

LOCK TABLES `tabel_权限信息` WRITE;
/*!40000 ALTER TABLE `tabel_权限信息` DISABLE KEYS */;
INSERT INTO `tabel_权限信息` VALUES (1,'guxiang',4,4,4,4,4,4,4,4,4,4,'4','4','4',4,'4','4','4','4','4',4),(2,'pangxiaoyi',4,4,4,4,4,4,4,4,4,4,'4','4','4',4,'4','4','4','4','4',4),(3,'yanglei',4,4,4,4,4,4,4,4,4,4,'4','4','4',4,'4','4','4','4','4',4);
/*!40000 ALTER TABLE `tabel_权限信息` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-01 19:30:32
