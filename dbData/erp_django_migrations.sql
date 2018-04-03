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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-03-30 13:16:04.815438'),(2,'auth','0001_initial','2018-03-30 13:16:10.547846'),(3,'admin','0001_initial','2018-03-30 13:16:11.834216'),(4,'admin','0002_logentry_remove_auto_add','2018-03-30 13:16:11.926702'),(5,'contenttypes','0002_remove_content_type_name','2018-03-30 13:16:12.654565'),(6,'auth','0002_alter_permission_name_max_length','2018-03-30 13:16:13.239053'),(7,'auth','0003_alter_user_email_max_length','2018-03-30 13:16:13.752134'),(8,'auth','0004_alter_user_username_opts','2018-03-30 13:16:13.785618'),(9,'auth','0005_alter_user_last_login_null','2018-03-30 13:16:14.202835'),(10,'auth','0006_require_contenttypes_0002','2018-03-30 13:16:14.226802'),(11,'auth','0007_alter_validators_add_error_messages','2018-03-30 13:16:14.265706'),(12,'auth','0008_alter_user_username_max_length','2018-03-30 13:16:14.769004'),(13,'online','0001_initial','2018-03-30 13:16:14.971190'),(14,'online','0002_delete_user','2018-03-30 13:16:15.099819'),(15,'online','0003_table_version','2018-03-30 13:16:15.330368'),(16,'online','0004_table_permission','2018-03-30 13:16:15.643674'),(17,'online','0005_table_user','2018-03-30 13:16:15.881284'),(18,'online','0006_auto_20171031_1419','2018-03-30 13:16:17.079564'),(19,'online','0007_auto_20171031_1421','2018-03-30 13:16:17.106127'),(20,'online','0008_auto_20171031_1427','2018-03-30 13:16:22.916893'),(21,'online','0009_auto_20171031_1445','2018-03-30 13:16:23.349749'),(22,'online','0010_auto_20171031_1447','2018-03-30 13:16:25.179514'),(23,'online','0011_auto_20171031_1450','2018-03-30 13:16:27.916498'),(24,'online','0012_table_bidding','2018-03-30 13:16:28.272768'),(25,'online','0013_auto_20171101_0942','2018-03-30 13:16:33.730577'),(26,'online','0014_table_contract','2018-03-30 13:16:34.110429'),(27,'online','0015_auto_20171101_1051','2018-03-30 13:16:36.177073'),(28,'online','0016_auto_20180328_0954','2018-03-30 13:16:36.862374'),(29,'online','0017_table_bidding_招标简介','2018-03-30 13:16:37.302827'),(30,'sessions','0001_initial','2018-03-30 13:16:37.668420'),(31,'online','0018_auto_20180331_0130','2018-03-31 01:30:16.208367'),(32,'online','0019_auto_20180331_0138','2018-03-31 01:38:58.538060'),(33,'online','0020_table_bidding_投标单位','2018-03-31 02:27:48.468536');
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

-- Dump completed on 2018-04-01 19:30:31
