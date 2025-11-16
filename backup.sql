-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: manutencao_micro
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_peca_id` int NOT NULL,
  `quantidade` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  CONSTRAINT `estoque_ibfk_1` FOREIGN KEY (`tipo_peca_id`) REFERENCES `tipos_peca` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque_defeituoso`
--

DROP TABLE IF EXISTS `estoque_defeituoso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque_defeituoso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_peca_id` int NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  CONSTRAINT `estoque_defeituoso_ibfk_1` FOREIGN KEY (`tipo_peca_id`) REFERENCES `tipos_peca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque_defeituoso`
--

LOCK TABLES `estoque_defeituoso` WRITE;
/*!40000 ALTER TABLE `estoque_defeituoso` DISABLE KEYS */;
INSERT INTO `estoque_defeituoso` VALUES (1,5,1),(2,1,4);
/*!40000 ALTER TABLE `estoque_defeituoso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque_novo`
--

DROP TABLE IF EXISTS `estoque_novo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque_novo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_peca_id` int NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  CONSTRAINT `estoque_novo_ibfk_1` FOREIGN KEY (`tipo_peca_id`) REFERENCES `tipos_peca` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque_novo`
--

LOCK TABLES `estoque_novo` WRITE;
/*!40000 ALTER TABLE `estoque_novo` DISABLE KEYS */;
INSERT INTO `estoque_novo` VALUES (1,1,2),(2,2,2),(3,3,1),(4,4,3),(5,5,1);
/*!40000 ALTER TABLE `estoque_novo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pecas_defeituosas`
--

DROP TABLE IF EXISTS `pecas_defeituosas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pecas_defeituosas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_peca_id` int NOT NULL,
  `numero_serie` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tecnico_id` int NOT NULL,
  `data_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_serie` (`numero_serie`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  KEY `tecnico_id` (`tecnico_id`),
  CONSTRAINT `pecas_defeituosas_ibfk_1` FOREIGN KEY (`tipo_peca_id`) REFERENCES `tipos_peca` (`id`),
  CONSTRAINT `pecas_defeituosas_ibfk_2` FOREIGN KEY (`tecnico_id`) REFERENCES `tecnicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pecas_defeituosas`
--

LOCK TABLES `pecas_defeituosas` WRITE;
/*!40000 ALTER TABLE `pecas_defeituosas` DISABLE KEYS */;
INSERT INTO `pecas_defeituosas` VALUES (1,5,'12345',2,'2025-11-16 00:43:25'),(3,1,'12346',2,'2025-11-16 00:44:49'),(4,1,'23456',2,'2025-11-16 00:52:10');
/*!40000 ALTER TABLE `pecas_defeituosas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tecnicos`
--

DROP TABLE IF EXISTS `tecnicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tecnicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_supervisor` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tecnicos`
--

LOCK TABLES `tecnicos` WRITE;
/*!40000 ALTER TABLE `tecnicos` DISABLE KEYS */;
INSERT INTO `tecnicos` VALUES (1,'Elisangela',1),(2,'João A',0);
/*!40000 ALTER TABLE `tecnicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_peca`
--

DROP TABLE IF EXISTS `tipos_peca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_peca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_peca`
--

LOCK TABLES `tipos_peca` WRITE;
/*!40000 ALTER TABLE `tipos_peca` DISABLE KEYS */;
INSERT INTO `tipos_peca` VALUES (4,'Fonte 500W'),(3,'Placa-mae LGA1155'),(5,'Ssd 120gb'),(1,'SSD 128GB'),(2,'SSD 240GB');
/*!40000 ALTER TABLE `tipos_peca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trocas`
--

DROP TABLE IF EXISTS `trocas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trocas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `peca_defeituosa_id` int NOT NULL,
  `tipo_peca_id` int NOT NULL,
  `supervisora_id` int NOT NULL,
  `data_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `peca_defeituosa_id` (`peca_defeituosa_id`),
  KEY `tipo_peca_id` (`tipo_peca_id`),
  KEY `supervisora_id` (`supervisora_id`),
  CONSTRAINT `trocas_ibfk_1` FOREIGN KEY (`peca_defeituosa_id`) REFERENCES `pecas_defeituosas` (`id`),
  CONSTRAINT `trocas_ibfk_2` FOREIGN KEY (`tipo_peca_id`) REFERENCES `tipos_peca` (`id`),
  CONSTRAINT `trocas_ibfk_3` FOREIGN KEY (`supervisora_id`) REFERENCES `tecnicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trocas`
--

LOCK TABLES `trocas` WRITE;
/*!40000 ALTER TABLE `trocas` DISABLE KEYS */;
INSERT INTO `trocas` VALUES (1,3,1,1,'2025-11-16 00:48:01'),(2,4,1,1,'2025-11-16 00:52:27');
/*!40000 ALTER TABLE `trocas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 15:54:08
