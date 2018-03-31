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
-- Table structure for table `tabel_变更信息`
--

DROP TABLE IF EXISTS `tabel_变更信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_变更信息` (
  `变更识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `立项识别码` bigint(20) DEFAULT NULL,
  `合同识别码` bigint(20) DEFAULT NULL,
  `变更类型` varchar(255) DEFAULT NULL,
  `变更编号` varchar(255) DEFAULT NULL,
  `变更主题` varchar(255) DEFAULT NULL,
  `变更登记日期` date DEFAULT NULL,
  `变更生效日期` date DEFAULT NULL,
  `变更原因` text,
  `预估变更额度` decimal(12,2) DEFAULT NULL,
  `变更额度` decimal(12,2) DEFAULT NULL,
  `变更备注` text,
  PRIMARY KEY (`变更识别码`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_变更信息`
--

LOCK TABLES `tabel_变更信息` WRITE;
/*!40000 ALTER TABLE `tabel_变更信息` DISABLE KEYS */;
INSERT INTO `tabel_变更信息` VALUES (1,47,29,'批价','BWD-PJ-001','防水材料','2017-09-26','2017-07-19','通过询价方式重新确认防水材料（原暂估价项目）价格',NULL,NULL,NULL),(2,47,29,'批价','BWD-PJ-002','电梯','2017-09-26','2017-07-19','通过询价方式认电梯（通过设计变更增加）价格',NULL,NULL,NULL),(3,48,30,'批价','BWG-PJ-001','防水材料','2017-09-26','2017-07-13','通过询价方式重新确认防水材料（原暂估价项目）价格',NULL,NULL,NULL),(4,48,30,'批价','BWG-PJ-002','电梯','2017-09-26','2017-07-19','通过询价方式重新确认电梯（原暂估价项目）价格',6873000.00,NULL,NULL),(5,48,30,'批价','BWG-PJ-003','淤泥','2017-09-26','2017-07-10','淤泥报价',NULL,NULL,NULL),(6,48,30,'批价','BWG-CL-002','毛石','2017-09-26','2017-07-10','毛石（因设计变更增加）',NULL,NULL,NULL),(7,48,30,'批价','BWG-CL-003','商砼','2017-09-26','2017-08-31','商砼（2017年6月按月批价）',531038.00,NULL,NULL),(8,48,30,'批价','BWG-CL-004','商砼','2017-09-26','2017-08-31','商砼（2016年7月份按月批价）',585305.00,NULL,NULL);
/*!40000 ALTER TABLE `tabel_变更信息` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-22  9:08:29
