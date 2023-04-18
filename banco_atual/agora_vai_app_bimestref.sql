-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: agora_vai
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_bimestref`
--

DROP TABLE IF EXISTS `app_bimestref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_bimestref` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bimestre` varchar(25) NOT NULL,
  `materiaf_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_bimestref_materiaf_id_707ed3cb_fk_app_materiaf_id` (`materiaf_id`),
  CONSTRAINT `app_bimestref_materiaf_id_707ed3cb_fk_app_materiaf_id` FOREIGN KEY (`materiaf_id`) REFERENCES `app_materiaf` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_bimestref`
--

LOCK TABLES `app_bimestref` WRITE;
/*!40000 ALTER TABLE `app_bimestref` DISABLE KEYS */;
INSERT INTO `app_bimestref` VALUES (1,'1',1),(2,'2',1),(3,'3',1),(4,'4',1),(5,'1',2),(6,'2',2),(7,'3',2),(8,'4',2),(9,'1',3),(10,'2',3),(11,'3',3),(12,'4',3),(13,'1',4),(14,'2',4),(15,'3',4),(16,'4',4),(17,'1',5),(18,'2',5),(19,'3',5),(20,'4',5),(21,'1',6),(22,'2',6),(23,'3',6),(24,'4',6),(25,'1',7),(26,'2',7),(27,'3',7),(28,'4',7),(29,'1',8),(30,'2',8),(31,'3',8),(32,'4',8);
/*!40000 ALTER TABLE `app_bimestref` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-18 16:18:40
