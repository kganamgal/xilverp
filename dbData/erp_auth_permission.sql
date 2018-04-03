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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add 版本管理表',7,'add_table_version'),(20,'Can change 版本管理表',7,'change_table_version'),(21,'Can delete 版本管理表',7,'delete_table_version'),(22,'Can add 权限信息表',8,'add_table_permission'),(23,'Can change 权限信息表',8,'change_table_permission'),(24,'Can delete 权限信息表',8,'delete_table_permission'),(25,'Can add 用户表',9,'add_table_user'),(26,'Can change 用户表',9,'change_table_user'),(27,'Can delete 用户表',9,'delete_table_user'),(28,'Can add 单位信息表',10,'add_table_company'),(29,'Can change 单位信息表',10,'change_table_company'),(30,'Can delete 单位信息表',10,'delete_table_company'),(31,'Can add 立项信息表',11,'add_table_initiation'),(32,'Can change 立项信息表',11,'change_table_initiation'),(33,'Can delete 立项信息表',11,'delete_table_initiation'),(34,'Can add 招标信息表',12,'add_table_bidding'),(35,'Can change 招标信息表',12,'change_table_bidding'),(36,'Can delete 招标信息表',12,'delete_table_bidding'),(37,'Can add 合同信息表',13,'add_table_contract'),(38,'Can change 合同信息表',13,'change_table_contract'),(39,'Can delete 合同信息表',13,'delete_table_contract'),(40,'Can add 变更信息表',14,'add_table_alteration'),(41,'Can change 变更信息表',14,'change_table_alteration'),(42,'Can delete 变更信息表',14,'delete_table_alteration'),(43,'Can add 预算信息表',15,'add_table_budget'),(44,'Can change 预算信息表',15,'change_table_budget'),(45,'Can delete 预算信息表',15,'delete_table_budget'),(46,'Can add 付款信息表',16,'add_table_payment'),(47,'Can change 付款信息表',16,'change_table_payment'),(48,'Can delete 付款信息表',16,'delete_table_payment'),(49,'Can add 分包合同信息表',17,'add_table_subcontract'),(50,'Can change 分包合同信息表',17,'change_table_subcontract'),(51,'Can delete 分包合同信息表',17,'delete_table_subcontract');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
