SET NAMES utf8mb4;
DROP DATABASE IF EXISTS inventario_computo;
CREATE DATABASE inventario_computo CHARACTER SET utf8mb4;
USE inventario_computo;

CREATE TABLE usuarios (
    id_usuario       INT          AUTO_INCREMENT PRIMARY KEY,
    nombre_completo  VARCHAR(100) NOT NULL,
    nombre_usuario   VARCHAR(30)  NOT NULL UNIQUE,
    password_hash    CHAR(64)     NOT NULL,
    rol              ENUM('ADMINISTRADOR','OPERADOR','CONSULTA') NOT NULL,
    estado           ENUM('ACTIVO','INACTIVO') NOT NULL DEFAULT 'ACTIVO'
);

CREATE TABLE departamentos (
    id_departamento  INT         AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE solicitantes (
    id_solicitante   INT          AUTO_INCREMENT PRIMARY KEY,
    matricula        VARCHAR(20)  NOT NULL UNIQUE,
    nombre_completo  VARCHAR(100) NOT NULL,
    tipo             ENUM('ALUMNO','DOCENTE') NOT NULL,
    id_departamento  INT          NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos (id_departamento)
);

CREATE TABLE equipos (
    id_equipo      INT          AUTO_INCREMENT PRIMARY KEY,
    codigo_barras  VARCHAR(30)  NOT NULL UNIQUE,
    descripcion    VARCHAR(100) NOT NULL,
    ubicacion      VARCHAR(100) NOT NULL,
    estado         ENUM('DISPONIBLE','PRESTADO','ASIGNADO') NOT NULL DEFAULT 'DISPONIBLE'
);

CREATE TABLE prestamos (
    id_prestamo       INT      AUTO_INCREMENT PRIMARY KEY,
    id_equipo         INT      NOT NULL,
    id_solicitante    INT      NOT NULL,
    fecha_prestamo    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_limite      DATETIME NOT NULL,
    fecha_devolucion  DATETIME NULL,
    FOREIGN KEY (id_equipo)      REFERENCES equipos (id_equipo),
    FOREIGN KEY (id_solicitante) REFERENCES solicitantes (id_solicitante),
    CHECK (fecha_limite > fecha_prestamo)
);

CREATE TABLE asignaciones (
    id_asignacion     INT          AUTO_INCREMENT PRIMARY KEY,
    id_equipo         INT          NOT NULL,
    id_solicitante    INT          NULL,
    id_departamento   INT          NULL,
    ubicacion         VARCHAR(100) NOT NULL,
    fecha_asignacion  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin         DATETIME     NULL,
    FOREIGN KEY (id_equipo)       REFERENCES equipos (id_equipo),
    FOREIGN KEY (id_solicitante)  REFERENCES solicitantes (id_solicitante),
    FOREIGN KEY (id_departamento) REFERENCES departamentos (id_departamento),
    CHECK ((id_solicitante IS NULL) <> (id_departamento IS NULL))
);

CREATE TABLE auditoria (
    id_auditoria      INT          AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada    VARCHAR(30)  NOT NULL,
    operacion         ENUM('INSERT','UPDATE','DELETE') NOT NULL,
    fecha_hora        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario           VARCHAR(100) NOT NULL,
    datos_anteriores  VARCHAR(255) NULL,
    datos_nuevos      VARCHAR(255) NULL
);
