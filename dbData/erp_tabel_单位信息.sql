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
-- Table structure for table `tabel_单位信息`
--

DROP TABLE IF EXISTS `tabel_单位信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabel_单位信息` (
  `单位识别码` bigint(20) NOT NULL AUTO_INCREMENT,
  `单位名称` varchar(255) DEFAULT NULL,
  `单位类别` varchar(255) DEFAULT NULL,
  `单位性质` varchar(255) DEFAULT NULL,
  `法定代表人` varchar(255) DEFAULT NULL,
  `注册资金` decimal(12,2) DEFAULT NULL,
  `单位资质` varchar(255) DEFAULT NULL,
  `银行账号` varchar(255) DEFAULT NULL,
  `联系人` varchar(255) DEFAULT NULL,
  `联系方式` varchar(255) DEFAULT NULL,
  `单位备注` text,
  PRIMARY KEY (`单位识别码`),
  UNIQUE KEY `单位名称` (`单位名称`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabel_单位信息`
--

LOCK TABLES `tabel_单位信息` WRITE;
/*!40000 ALTER TABLE `tabel_单位信息` DISABLE KEYS */;
INSERT INTO `tabel_单位信息` VALUES (1,'青岛世园新城镇开发投资有限公司','房地产开发商','国有','姜民秀',200000000.00,'房地产开发三级',NULL,'顾翔','0532-58703628',NULL),(2,'青岛世园（集团）有限公司','房地产开发商','国有','丁伟',3000000000.00,NULL,NULL,'顾翔','0532-58703628',NULL),(3,'青岛市公安局','国家机关','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'山东世元工程管理有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,'王姗',NULL,NULL),(5,'青岛辉宏置业有限公司','施工','非国有',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,'青岛市勘察测绘研究院','勘察','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'山东同圆设计集团有限公司','设计','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,'派出所设计单位'),(8,'青岛华鹏工程咨询集团有限公司','监理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9,'青岛琴岛工程造价咨询有限公司','造价','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'青岛市市政工程设计研究院有限责任公司','前期咨询','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,'青岛市水利勘测设计研究院有限公司','前期咨询','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(12,'青岛市建设工程施工图设计审查中心','其他','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(13,'青岛市城市建设档案馆','其他','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(14,'青岛市白蚁防治研究所','其他','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(15,'李沧区财政局国库支付中心','其他','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(16,'崂山区财政局','其他','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,'青岛市财政局','其他','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,'青岛市李沧区世园街道办事处北王家上流社区居民委员会','其他','行政单位','王进达',NULL,NULL,NULL,NULL,NULL,NULL),(19,'青岛兴水实业有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,'山东三阳项目管理有限公司青岛分公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,'青岛集合工程设计咨询有限公司','设计咨询','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(22,'青岛誉光建筑工程咨询有限公司','造价','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(23,'青岛国信工程咨询有限公司','前期咨询','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(24,'山东海逸恒安项目管理有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,'山东地矿开元勘察施工总公司','勘察','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,'青岛精信工程管理有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,'青岛利业建设咨询有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,'山东华烨规划建筑设计有限公司','设计','非国有企业','王鹏',NULL,NULL,NULL,NULL,NULL,NULL),(29,'青岛理工大学环境影响评价中心','前期咨询','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,'青岛恒源水土保持咨询有限公司','前期咨询','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(31,'青岛佳易工程管理有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(32,'青岛建安建设集团有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(33,'青岛康太源建设集团有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(34,'青岛华德仪表工程有限公司','施工','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(35,'青岛城阳希望电气有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(36,'青岛瑞昊非融资担保有限公司','担保','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,'山东正元建设工程有限责任公司','勘察','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,'青岛广信建设咨询有限公司','监理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,'青岛市规划建筑服务中心','设计',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(40,'青岛海洋地质工程勘察院','勘察','非国有企业','周连成',10000000.00,'工程勘察综合类甲级（B137027551-6/4）、工程测量乙级（乙测资字3711781）',NULL,'周小时','13583286296',NULL),(41,'其他代理业务资金-待清算代理财政非税收入资金过渡户',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(42,'青岛市建筑企业养老保证金管理办公室','政府机构','行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(43,'华优建筑设计院','设计','非国有企业','赵新石',NULL,'人防设计',NULL,NULL,NULL,NULL),(44,'青岛汇文市政工程设计有限责任公司','设计','非国有企业','赵晓丹',NULL,'市政设计',NULL,NULL,NULL,NULL),(45,'山东正元建设工程有限责任公司青岛分公司','设计','非国有企业','刘庆祥',NULL,'基坑支护设计',NULL,NULL,NULL,NULL),(46,'胡朝龙',NULL,'自然人',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(47,'任云飞',NULL,'自然人',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(48,'丁源',NULL,'自然人',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(49,'李建乐',NULL,'自然人',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(50,'青岛福莱易通软件有限公司','软件','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(51,'青岛三和施工图审查有限公司','审图','非国有企业','刘跃进',NULL,NULL,NULL,NULL,NULL,NULL),(52,'青岛人防工程设计文件审查咨询有限公司','审图','非国有企业','朱燕妮',NULL,NULL,NULL,NULL,NULL,NULL),(53,'青岛竣业房地产评估所','前期咨询','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(54,'青岛昊佳房地产评估事务所','前期咨询','非国有企业','赵建民',NULL,NULL,NULL,NULL,NULL,NULL),(55,'雷拓国际建筑设计顾问（北京）有限公司','设计','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(56,'悉地国际设计顾问（深圳）有限公司','设计','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(57,'国网山东省电力公司青岛供电公司','电力','国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(58,'青岛市地方税务局',NULL,'行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(59,'青岛东达建筑工程有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(60,'青岛森泰建设工程有限公司','施工','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(61,'青岛市昊金海建设项目管理有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(62,'青岛市李沧区人力资源和社会保障局',NULL,'行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(63,'青岛市人民防空办公室',NULL,'行政单位',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(64,'山东中钢招标有限公司','招标代理','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(65,'青岛世园土地整理有限公司','房地产开发','国有企业','姜民秀',NULL,NULL,NULL,NULL,NULL,NULL),(66,'青岛市人防建筑设计研究院','设计','国有企业',NULL,NULL,'建筑设计甲级、人防设计甲级',NULL,NULL,NULL,NULL),(67,'青岛青咨工程咨询有限公司','前期咨询','非国有企业',NULL,NULL,'工程咨询甲级、工程造价咨询甲级',NULL,NULL,NULL,NULL),(68,'郑州欧丽信大电子信息股份有限公司','设计','非国有企业',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(69,'青岛圣辰建筑安装工程有限公司','施工','非国有企业','张其利',20000000.00,'市政二级','中国农业银行青岛市城阳区支行夏庄-38100401040007840','张其利','13606391258',NULL),(70,'青岛世园发展有限公司',NULL,'国有企业','孙卫东',NULL,NULL,NULL,NULL,NULL,NULL),(71,'青岛兰德资产评估有限公司','前期咨询','非国有企业','高玉青',NULL,NULL,'37101986106051008681',NULL,NULL,NULL);
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

-- Dump completed on 2018-01-22  9:08:30
