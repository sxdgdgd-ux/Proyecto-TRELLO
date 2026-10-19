CREATE DATABASE IF NOT EXISTS trello_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE trello_db;

CREATE TABLE IF NOT EXISTS proyecto (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proyecto VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    fecha_creacion DATE NOT NULL DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS etiqueta (
    id_etiqueta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL DEFAULT '#808080'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS proyecto_usuario (
    id_proyecto INT NOT NULL,
    id_usuario INT NOT NULL,
    rol ENUM('Administrador', 'Lider', 'Miembro', 'Observador')
        NOT NULL DEFAULT 'Miembro',
    PRIMARY KEY (id_proyecto, id_usuario),
    CONSTRAINT fk_proyecto_usuario_proyecto FOREIGN KEY (id_proyecto)
        REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
    CONSTRAINT fk_proyecto_usuario_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tablero (
    id_tablero INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    CONSTRAINT fk_tablero_proyecto FOREIGN KEY (id_proyecto)
        REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tablero_usuario (
    id_tablero INT NOT NULL,
    id_usuario INT NOT NULL,
    rol ENUM('Administrador', 'Lider', 'Miembro', 'Observador')
        NOT NULL DEFAULT 'Miembro',
    PRIMARY KEY (id_tablero, id_usuario),
    CONSTRAINT fk_tablero_usuario_tablero FOREIGN KEY (id_tablero)
        REFERENCES tablero(id_tablero) ON DELETE CASCADE,
    CONSTRAINT fk_tablero_usuario_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS lista (
    id_lista INT AUTO_INCREMENT PRIMARY KEY,
    id_tablero INT NOT NULL,
    nombre_lista VARCHAR(100) NOT NULL,
    posicion INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_lista_tablero FOREIGN KEY (id_tablero)
        REFERENCES tablero(id_tablero) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tarjeta (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    id_lista INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    fecha_limite DATE NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    CONSTRAINT fk_tarjeta_lista FOREIGN KEY (id_lista)
        REFERENCES lista(id_lista) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS asignacion_tarjeta (
    id_tarjeta INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_tarjeta, id_usuario),
    CONSTRAINT fk_asignacion_tarjeta_tarjeta FOREIGN KEY (id_tarjeta)
        REFERENCES tarjeta(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_asignacion_tarjeta_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS comentario (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_tarjeta INT NOT NULL,
    id_usuario INT NOT NULL,
    texto TEXT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comentario_tarjeta FOREIGN KEY (id_tarjeta)
        REFERENCES tarjeta(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_comentario_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tarjeta_etiqueta (
    id_tarjeta INT NOT NULL,
    id_etiqueta INT NOT NULL,
    PRIMARY KEY (id_tarjeta, id_etiqueta),
    CONSTRAINT fk_tarjeta_etiqueta_tarjeta FOREIGN KEY (id_tarjeta)
        REFERENCES tarjeta(id_tarjeta) ON DELETE CASCADE,
    CONSTRAINT fk_tarjeta_etiqueta_etiqueta FOREIGN KEY (id_etiqueta)
        REFERENCES etiqueta(id_etiqueta) ON DELETE CASCADE
) ENGINE=InnoDB;
