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
-- Table structure for table `app_coordenadoria`
--

DROP TABLE IF EXISTS `app_coordenadoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_coordenadoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `coordenadoria` varchar(50) NOT NULL,
  `jurisdicao_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_coordenadoria_jurisdicao_id_7c8ca8ec_fk_app_jurisdicao_id` (`jurisdicao_id`),
  CONSTRAINT `app_coordenadoria_jurisdicao_id_7c8ca8ec_fk_app_jurisdicao_id` FOREIGN KEY (`jurisdicao_id`) REFERENCES `app_jurisdicao` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_coordenadoria`
--

LOCK TABLES `app_coordenadoria` WRITE;
/*!40000 ALTER TABLE `app_coordenadoria` DISABLE KEYS */;
INSERT INTO `app_coordenadoria` VALUES (1,'CDE 01',1),(2,'CDE 02',1),(3,'CDE 03',1),(4,'CDE 04',1),(5,'CDE 05',1),(6,'CDE 06',1),(7,'CDE 07',1),(8,'Alvarães',2),(9,'Amaturá',2),(10,'Anamã',2),(11,'Anori',2),(12,'Apuí',2),(13,'Atalaia do Norte',2),(14,'Autazes',2),(15,'Barcelos',2),(16,'Barreirinha',2),(17,'Benjamin Constant',2),(18,'Beruri',2),(19,'Boa Vista do Ramos',2),(20,'Boca do Acre',2),(21,'Borba',2),(22,'Caapiranga',2),(23,'Canutama',2),(24,'Carauari',2),(25,'Careiro',2),(26,'Careiro da Várzea',2),(27,'Coari',2),(28,'Codajás',2),(29,'Eirunepé',2),(30,'Envira',2),(31,'Fonte Boa',2),(32,'Guajará',2),(33,'Humaitá',2),(34,'Ipixuna',2),(35,'Iranduba',2),(36,'Itacoatiara',2),(37,'Itamarati',2),(38,'Itapiranga',2),(39,'Japurá',2),(40,'Juruá',2),(41,'Jutaí',2),(42,'Lábrea',2),(43,'Manacapuru',2),(44,'Manaquiri',2),(45,'Manicoré',2),(46,'Maraã',2),(47,'Maués',2),(48,'Nhamundá',2),(49,'Nova Olinda do Norte',2),(50,'Novo Airão',2),(51,'Novo Aripuanã',2),(52,'Parintins',2),(53,'Pauini',2),(54,'Presidente Figueiredo',2),(55,'Rio Preto da Eva',2),(56,'Santa Isabel do Rio Negro',2),(57,'Santo Antônio do Içá',2),(58,'São Gabriel da Cachoeira',2),(59,'São Paulo de Olivença',2),(60,'São Sebastião do Uatumã',2),(61,'Silves',2),(62,'Tabatinga',2),(63,'Tapauá',2),(64,'Tefé',2),(65,'Tonantins',2),(66,'Uarini',2),(67,'Urucará',2),(68,'Urucurituba',2);
/*!40000 ALTER TABLE `app_coordenadoria` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-03 13:13:44
