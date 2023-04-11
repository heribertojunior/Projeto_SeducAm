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
-- Table structure for table `app_resposta`
--

DROP TABLE IF EXISTS `app_resposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_resposta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `resposta` tinyint(1) NOT NULL,
  `foi_possivel` tinyint(1) NOT NULL,
  `motivo` varchar(100) DEFAULT NULL,
  `outros` varchar(150) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `pergunta_id` bigint NOT NULL,
  `professor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_resposta_pergunta_id_8a2e3b0a_fk_app_pergunta_id` (`pergunta_id`),
  KEY `app_resposta_professor_id_03f92601_fk_app_professor_id` (`professor_id`),
  CONSTRAINT `app_resposta_pergunta_id_8a2e3b0a_fk_app_pergunta_id` FOREIGN KEY (`pergunta_id`) REFERENCES `app_pergunta` (`id`),
  CONSTRAINT `app_resposta_professor_id_03f92601_fk_app_professor_id` FOREIGN KEY (`professor_id`) REFERENCES `app_professor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_resposta`
--

LOCK TABLES `app_resposta` WRITE;
/*!40000 ALTER TABLE `app_resposta` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_resposta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-05 14:33:40
