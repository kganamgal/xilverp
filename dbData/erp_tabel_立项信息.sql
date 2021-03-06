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
-- Table structure for table `tabel_立项信息`
--

DROP TABLE IF EXISTS `tabel_立项信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_立项信息` (
  `立项识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `项目名称` varchar(255) NOT NULL,
  `分项名称` varchar(255) DEFAULT NULL,
  `父项立项识别码` bigint(20) DEFAULT NULL,
  `建设单位识别码` bigint(20) DEFAULT NULL,
  `代建单位识别码` bigint(20) DEFAULT NULL,
  `立项文件名称` varchar(255) DEFAULT NULL,
  `立项时间` date DEFAULT NULL,
  `项目概算` decimal(12,2) DEFAULT NULL,
  `立项备注` longtext,
  `立项简介` longtext,
  PRIMARY KEY (`立项识别码`),
  UNIQUE KEY `TABEL_立项信息_项目名称_分项名称_e2baf4cb_uniq` (`项目名称`,`分项名称`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_立项信息`
--

LOCK TABLES `tabel_立项信息` WRITE;
/*!40000 ALTER TABLE `tabel_立项信息` DISABLE KEYS */;
INSERT INTO `tabel_立项信息` VALUES (1,'大珠山',NULL,NULL,4,NULL,NULL,NULL,1000000000.00,NULL,NULL),(2,'琅琊台',NULL,NULL,5,NULL,NULL,NULL,1000000000.00,NULL,NULL),(3,'凤凰岛',NULL,NULL,2,NULL,NULL,NULL,1000000000.00,NULL,NULL),(4,'辛安府团结新城二期',NULL,NULL,2,NULL,NULL,NULL,2000000000.00,NULL,NULL),(5,'集团本部',NULL,NULL,1,NULL,NULL,NULL,2000000000.00,NULL,NULL),(6,'九龙湾',NULL,NULL,3,NULL,NULL,NULL,3000000000.00,NULL,NULL),(9,'大珠山','2018花卉活动',1,4,NULL,NULL,NULL,660000.00,NULL,NULL),(10,'集团本部','2018发行公司债所需会计事务所、律师事务所',5,1,NULL,NULL,NULL,1800000.00,NULL,NULL),(11,'辛安府团结新城二期','监理',4,2,NULL,NULL,NULL,7000000.00,NULL,NULL);
/*!40000 ALTER TABLE `tabel_立项信息` ENABLE KEYS */;
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
