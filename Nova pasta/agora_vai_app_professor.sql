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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_professor`
--

LOCK TABLES `app_professor` WRITE;
/*!40000 ALTER TABLE `app_professor` DISABLE KEYS */;
INSERT INTO `app_professor` VALUES (1,'Heriberto',68,617,2,13359,6681,13360,1670),(2,'Joyce',2,36,1,1778,1771,1770,96),(3,'Joao',2,36,1,110,103,6782,96),(4,'Bill',2,38,1,116,109,6788,102),(5,'Teste 1',2,37,1,113,106,6785,99),(6,'Teste 2',3,74,1,1876,1869,8548,194),(7,'Teste 3',2,37,1,1781,1774,1773,99),(8,'Teste 4',2,37,1,3450,3443,10122,100),(9,'Teste 5',3,74,1,1877,1870,1869,195),(10,'Joianne',68,617,2,8350,1677,8356,1670),(11,'Teste 5',2,38,1,6782,109,108,102),(12,'Teste 7',7,242,1,7315,642,641,635),(13,'Teste 8',9,247,2,2330,2323,2322,648),(14,'Teste 9',5,151,1,2075,2068,2067,393),(15,'Heriberto',5,156,1,2088,2081,2080,406),(16,'Heriberto 3',3,76,1,3551,3544,3543,201),(17,'Salvando pergunta',2,36,1,110,103,102,96),(18,'Teste resposta',1,1,1,4,4,4,1),(19,'Teste resposta 1',1,1,1,4,4,6684,1),(20,'Teste resposta 2',8,243,2,650,643,642,636),(21,'Teste os 4 bim',2,36,1,110,103,102,96),(22,'aguhaa',1,1,1,4,4,4,1),(23,'Test',1,14,1,3383,3376,10055,33),(24,'Insanu',68,617,2,13359,6681,13360,1670),(25,'Teste xx',1,1,1,1,1,1,1),(26,'teste xxx',1,1,1,2,2,2,1),(27,'teste z',1,1,1,1,1,1,1),(28,'teste z',1,1,1,1,1,1,1),(29,'Teste ZZ',2,36,1,5114,5107,5106,96),(30,'Teste Y',1,3,1,3353,3346,3345,3),(31,'Teste Y',1,3,1,3353,3346,3345,3),(32,'Teste YY',8,243,2,650,643,642,636),(33,'Teste YY',8,243,2,650,643,642,636),(34,'Teste WW',1,1,1,10,2,2,1),(35,'Carla',1,7,1,6694,21,20,14),(36,'Carla',2,36,1,1778,1771,1770,96),(37,'Joana',10,248,2,2333,2326,2325,651),(38,'Teoria',3,74,1,208,201,200,194),(39,'Agora_vai',2,36,1,8444,1771,1770,96),(40,'Teste ajhuha',2,37,1,11783,5110,5109,99),(41,'Teste ajxlcx',1,1,1,3,3,3,1),(42,'agyegayeguahe',1,1,1,12,4,4,1),(43,'anbjgft',1,1,1,4,4,4,1),(44,'Testyage',1,1,1,3,3,3,1),(45,'sdghshwsh',1,1,1,4,4,4,1),(46,'qwewq',1,1,1,4,4,4,1),(47,'dasfgdasfgd',1,1,1,2,2,2,1),(48,'xfgsfg',1,1,1,1,1,1,1),(49,'aheuoiajejajf',1,1,1,1,1,1,1),(50,'asfagaga',1,1,1,3,3,3,1);
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

-- Dump completed on 2023-04-13 16:04:07
