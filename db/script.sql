-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS biblioteca_db;

USE biblioteca_db;

-- Tabela de Autores
CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nome_autor VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    nacionalidade VARCHAR(50),
    biografia TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Publicadoras
CREATE TABLE publicadoras (
    id_publicadora INT AUTO_INCREMENT PRIMARY KEY,
    nome_publicadora VARCHAR(100) NOT NULL UNIQUE,
    endereco VARCHAR(200),
    telefone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Categorias
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(50) NOT NULL UNIQUE,
    descricao TEXT
);

-- Tabela de Livros
CREATE TABLE livros (
    id_livro INT AUTO_INCREMENT PRIMARY KEY,
    nome_livro VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    id_autor INT NOT NULL,
    id_publicadora INT NOT NULL,
    id_categoria INT,
    ano_publicacao INT NOT NULL,
    edicao INT DEFAULT 1,
    numero_paginas INT,
    idioma VARCHAR(50) DEFAULT 'Português',
    preco DECIMAL(10, 2),
    quantidade_disponivel INT DEFAULT 0,
    quantidade_total INT DEFAULT 0,
    sinopse TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor) ON DELETE RESTRICT,
    FOREIGN KEY (id_publicadora) REFERENCES publicadoras(id_publicadora) ON DELETE RESTRICT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL,
    INDEX idx_isbn (isbn),
    INDEX idx_autor (id_autor),
    INDEX idx_publicadora (id_publicadora),
    INDEX idx_categoria (id_categoria)
);

-- Tabela de Usuários/Leitores
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    endereco VARCHAR(200),
    data_nascimento DATE,
    cpf VARCHAR(14) UNIQUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

-- Tabela de Empréstimos
CREATE TABLE emprestimos (
    id_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_livro INT NOT NULL,
    id_usuario INT NOT NULL,
    data_emprestimo DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATETIME,
    status ENUM('ativo', 'devolvido', 'atrasado') DEFAULT 'ativo',
    multa DECIMAL(10, 2) DEFAULT 0,
    observacoes TEXT,
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    INDEX idx_usuario (id_usuario),
    INDEX idx_livro (id_livro),
    INDEX idx_status (status)
);

-- Tabela de Avaliações
CREATE TABLE avaliacoes (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_livro INT NOT NULL,
    id_usuario INT NOT NULL,
    nota INT CHECK (nota >= 1 AND nota <= 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    UNIQUE KEY unique_avaliacao (id_livro, id_usuario)
);

-- Índices adicionais para melhor performance
CREATE INDEX idx_livros_nome ON livros(nome_livro);
CREATE INDEX idx_autores_nome ON autores(nome_autor);
CREATE INDEX idx_publicadoras_nome ON publicadoras(nome_publicadora);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_emprestimos_data ON emprestimos(data_emprestimo);

-- =====================================================
-- Dados de Exemplo
-- =====================================================

INSERT INTO autores (nome_autor, nacionalidade) VALUES
('Machado de Assis', 'Brasileira'),
('Paulo Coelho', 'Brasileira'),
('J.K. Rowling', 'Britânica');

INSERT INTO publicadoras (nome_publicadora, email) VALUES
('Companhia das Letras', 'contato@companhiadasletras.com.br'),
('Rocco', 'contato@rocco.com.br');

INSERT INTO categorias (nome_categoria) VALUES
('Romance'),
('Ficção Científica'),
('Mistério'),
('Autoajuda'),
('Clássico');
