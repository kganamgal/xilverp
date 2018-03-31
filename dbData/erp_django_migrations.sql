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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-12-22 03:32:58.268948'),(2,'auth','0001_initial','2017-12-22 03:33:00.078551'),(3,'admin','0001_initial','2017-12-22 03:33:00.562152'),(4,'admin','0002_logentry_remove_auto_add','2017-12-22 03:33:00.562152'),(5,'contenttypes','0002_remove_content_type_name','2017-12-22 03:33:00.718152'),(6,'auth','0002_alter_permission_name_max_length','2017-12-22 03:33:00.780552'),(7,'auth','0003_alter_user_email_max_length','2017-12-22 03:33:00.874152'),(8,'auth','0004_alter_user_username_opts','2017-12-22 03:33:00.889752'),(9,'auth','0005_alter_user_last_login_null','2017-12-22 03:33:00.936552'),(10,'auth','0006_require_contenttypes_0002','2017-12-22 03:33:00.952152'),(11,'auth','0007_alter_validators_add_error_messages','2017-12-22 03:33:00.967752'),(12,'auth','0008_alter_user_username_max_length','2017-12-22 03:33:01.045753'),(13,'online','0001_initial','2017-12-22 03:33:01.123753'),(14,'online','0002_delete_user','2017-12-22 03:33:01.342153'),(15,'online','0003_table_version','2017-12-22 03:33:01.404553'),(16,'online','0004_table_permission','2017-12-22 03:33:01.560554'),(17,'online','0005_table_user','2017-12-22 03:33:01.638554'),(18,'online','0006_auto_20171031_1419','2017-12-22 03:33:02.106554'),(19,'online','0007_auto_20171031_1421','2017-12-22 03:33:02.122155'),(20,'online','0008_auto_20171031_1427','2017-12-22 03:33:03.666557'),(21,'online','0009_auto_20171031_1445','2017-12-22 03:33:03.791357'),(22,'online','0010_auto_20171031_1447','2017-12-22 03:33:03.978558'),(23,'online','0011_auto_20171031_1450','2017-12-22 03:33:04.914559'),(24,'online','0012_table_bidding','2017-12-22 03:33:05.039360'),(25,'online','0013_auto_20171101_0942','2017-12-22 03:33:06.053361'),(26,'online','0014_table_contract','2017-12-22 03:33:06.131362'),(27,'online','0015_auto_20171101_1051','2017-12-22 03:33:07.550964'),(28,'sessions','0001_initial','2017-12-22 03:33:07.597764');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-22  9:08:28
