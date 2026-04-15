-- Cria o banco de dados
CREATE DATABASE IF NOT EXISTS biblioteca;

-- Usa o banco criado
USE biblioteca;

-- Cria a tabela de autores
CREATE TABLE IF NOT EXISTS autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nome_autor VARCHAR(255) NOT NULL,
    data_nascimento DATE NULL,
    nacionalidade VARCHAR(100) NULL,
    biografia TEXT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);
