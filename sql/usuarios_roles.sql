SET NAMES utf8mb4;
USE inventario_computo;

INSERT INTO usuarios (nombre_completo, nombre_usuario, password_hash, rol) VALUES
 ('Administrador del Sistema', 'admin',    SHA2('Admin2026!',    256), 'ADMINISTRADOR'),
 ('María López Ortega',        'operador', SHA2('Operador2026!', 256), 'OPERADOR'),
 ('Carlos Ruiz Peña',          'consulta', SHA2('Consulta2026!', 256), 'CONSULTA');
