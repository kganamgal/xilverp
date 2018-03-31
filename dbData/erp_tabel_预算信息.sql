CREATE DATABASE  IF NOT EXISTS `erp` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `erp`;
-- MySQL dump 10.13  Distrib 5.7.20, for Linux (i686)
--
-- Host: 172.17.22.176    Database: erp
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `tabel_预算信息`
--

DROP TABLE IF EXISTS `tabel_预算信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_预算信息` (
  `预算识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `父项预算识别码` bigint(20) DEFAULT NULL,
  `预算名称` varchar(255) DEFAULT NULL,
  `预算周期` varchar(255) DEFAULT NULL,
  `预算总额` decimal(12,2) DEFAULT NULL,
  `预算备注` text,
  PRIMARY KEY (`预算识别码`),
  UNIQUE KEY `预算名称` (`预算名称`,`预算周期`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_预算信息`
--

LOCK TABLES `tabel_预算信息` WRITE;
/*!40000 ALTER TABLE `tabel_预算信息` DISABLE KEYS */;
INSERT INTO `tabel_预算信息` VALUES (1,NULL,'天水路派出所','全过程',29212000.00,NULL),(2,1,'天水路派出所-工程费','全过程',23678555.81,NULL),(3,1,'天水路派出所-其他费用','全过程',4504389.23,NULL),(4,NULL,'预算外支出',NULL,9999999999.00,'所有不需要预算的付款，用本项即可'),(5,NULL,'北王安置房多层进度款',NULL,187836032.46,NULL),(8,NULL,'北王安置房高层区进度款',NULL,200000000.00,NULL),(9,8,'北王安置房高层区进度款','2017/6-8',9788537.84,NULL),(10,8,'北王安置房高层区进度款','2017/9',5608912.62,NULL),(11,NULL,'1609工程','2017年第4季度',6500000.00,NULL);
/*!40000 ALTER TABLE `tabel_预算信息` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-22  9:08:30
