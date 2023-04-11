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
-- Table structure for table `app_professor`
--

DROP TABLE IF EXISTS `app_professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_professor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `coordenadoria_id` bigint NOT NULL,
  `escola_id` bigint NOT NULL,
  `jurisdicao_id` bigint NOT NULL,
  `materia_id` bigint NOT NULL,
  `serie_id` bigint NOT NULL,
  `turma_id` bigint NOT NULL,
  `turno_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_professor_serie_id_b71f0e8a_fk_app_serie_id` (`serie_id`),
  KEY `app_professor_turma_id_8aad84ea_fk_app_turma_id` (`turma_id`),
  KEY `app_professor_turno_id_35f69385_fk_app_turno_id` (`turno_id`),
  KEY `app_professor_coordenadoria_id_5637c424_fk_app_coordenadoria_id` (`coordenadoria_id`),
  KEY `app_professor_escola_id_622ef56f_fk_app_escola_id` (`escola_id`),
  KEY `app_professor_jurisdicao_id_12565b7d_fk_app_jurisdicao_id` (`jurisdicao_id`),
  KEY `app_professor_materia_id_7b016fda_fk_app_materia_id` (`materia_id`),
  CONSTRAINT `app_professor_coordenadoria_id_5637c424_fk_app_coordenadoria_id` FOREIGN KEY (`coordenadoria_id`) REFERENCES `app_coordenadoria` (`id`),
  CONSTRAINT `app_professor_escola_id_622ef56f_fk_app_escola_id` FOREIGN KEY (`escola_id`) REFERENCES `app_escola` (`id`),
  CONSTRAINT `app_professor_jurisdicao_id_12565b7d_fk_app_jurisdicao_id` FOREIGN KEY (`jurisdicao_id`) REFERENCES `app_jurisdicao` (`id`),
  CONSTRAINT `app_professor_materia_id_7b016fda_fk_app_materia_id` FOREIGN KEY (`materia_id`) REFERENCES `app_materia` (`id`),
  CONSTRAINT `app_professor_serie_id_b71f0e8a_fk_app_serie_id` FOREIGN KEY (`serie_id`) REFERENCES `app_serie` (`id`),
  CONSTRAINT `app_professor_turma_id_8aad84ea_fk_app_turma_id` FOREIGN KEY (`turma_id`) REFERENCES `app_turma` (`id`),
  CONSTRAINT `app_professor_turno_id_35f69385_fk_app_turno_id` FOREIGN KEY (`turno_id`) REFERENCES `app_turno` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_professor`
--

LOCK TABLES `app_professor` WRITE;
/*!40000 ALTER TABLE `app_professor` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_professor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-03 13:13:45
