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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add bimestref',7,'add_bimestref'),(26,'Can change bimestref',7,'change_bimestref'),(27,'Can delete bimestref',7,'delete_bimestref'),(28,'Can view bimestref',7,'view_bimestref'),(29,'Can add coordenadoria',8,'add_coordenadoria'),(30,'Can change coordenadoria',8,'change_coordenadoria'),(31,'Can delete coordenadoria',8,'delete_coordenadoria'),(32,'Can view coordenadoria',8,'view_coordenadoria'),(33,'Can add escola',9,'add_escola'),(34,'Can change escola',9,'change_escola'),(35,'Can delete escola',9,'delete_escola'),(36,'Can view escola',9,'view_escola'),(37,'Can add jurisdicao',10,'add_jurisdicao'),(38,'Can change jurisdicao',10,'change_jurisdicao'),(39,'Can delete jurisdicao',10,'delete_jurisdicao'),(40,'Can view jurisdicao',10,'view_jurisdicao'),(41,'Can add materia',11,'add_materia'),(42,'Can change materia',11,'change_materia'),(43,'Can delete materia',11,'delete_materia'),(44,'Can view materia',11,'view_materia'),(45,'Can add pergunta',12,'add_pergunta'),(46,'Can change pergunta',12,'change_pergunta'),(47,'Can delete pergunta',12,'delete_pergunta'),(48,'Can view pergunta',12,'view_pergunta'),(49,'Can add professor',13,'add_professor'),(50,'Can change professor',13,'change_professor'),(51,'Can delete professor',13,'delete_professor'),(52,'Can view professor',13,'view_professor'),(53,'Can add serie',14,'add_serie'),(54,'Can change serie',14,'change_serie'),(55,'Can delete serie',14,'delete_serie'),(56,'Can view serie',14,'view_serie'),(57,'Can add serief',15,'add_serief'),(58,'Can change serief',15,'change_serief'),(59,'Can delete serief',15,'delete_serief'),(60,'Can view serief',15,'view_serief'),(61,'Can add turno',16,'add_turno'),(62,'Can change turno',16,'change_turno'),(63,'Can delete turno',16,'delete_turno'),(64,'Can view turno',16,'view_turno'),(65,'Can add turma',17,'add_turma'),(66,'Can change turma',17,'change_turma'),(67,'Can delete turma',17,'delete_turma'),(68,'Can view turma',17,'view_turma'),(69,'Can add resposta',18,'add_resposta'),(70,'Can change resposta',18,'change_resposta'),(71,'Can delete resposta',18,'delete_resposta'),(72,'Can view resposta',18,'view_resposta'),(73,'Can add materiaf',19,'add_materiaf'),(74,'Can change materiaf',19,'change_materiaf'),(75,'Can delete materiaf',19,'delete_materiaf'),(76,'Can view materiaf',19,'view_materiaf'),(77,'Can add bimestre',20,'add_bimestre'),(78,'Can change bimestre',20,'change_bimestre'),(79,'Can delete bimestre',20,'delete_bimestre'),(80,'Can view bimestre',20,'view_bimestre');
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

-- Dump completed on 2023-04-18 16:18:41
