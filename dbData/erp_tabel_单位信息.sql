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
-- Table structure for table `tabel_单位信息`
--

DROP TABLE IF EXISTS `tabel_单位信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_单位信息` (
  `单位识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `单位名称` varchar(255) NOT NULL,
  `单位类别` varchar(255) DEFAULT NULL,
  `单位性质` varchar(255) DEFAULT NULL,
  `法定代表人` varchar(255) DEFAULT NULL,
  `注册资金` decimal(12,2) DEFAULT NULL,
  `单位资质` varchar(255) DEFAULT NULL,
  `银行账号` varchar(255) DEFAULT NULL,
  `联系人` varchar(255) DEFAULT NULL,
  `联系方式` varchar(255) DEFAULT NULL,
  `单位备注` longtext,
  PRIMARY KEY (`单位识别码`),
  UNIQUE KEY `单位名称` (`单位名称`),
  UNIQUE KEY `TABEL_单位信息_单位名称_0821d540_uniq` (`单位名称`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_单位信息`
--

LOCK TABLES `tabel_单位信息` WRITE;
/*!40000 ALTER TABLE `tabel_单位信息` DISABLE KEYS */;
INSERT INTO `tabel_单位信息` VALUES (1,'青岛西海岸旅游投资集团有限公司','集团或子公司','国有企业','李彩元',3000000000.00,NULL,NULL,NULL,NULL,NULL),(2,'文旅',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'九龙湾公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'大珠山公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'琅琊台公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `tabel_单位信息` ENABLE KEYS */;
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
