SET NAMES utf8mb4;
USE inventario_computo;

SET @usuario_app = 'carga_inicial';

INSERT INTO departamentos (id_departamento, nombre) VALUES
 (1, 'Sistemas Computacionales'),
 (2, 'Ingeniería Industrial'),
 (3, 'Ciencias Básicas'),
 (4, 'Centro de Cómputo'),
 (5, 'Dirección Académica');

INSERT INTO solicitantes (id_solicitante, matricula, nombre_completo, tipo, id_departamento) VALUES
 ( 1, 'A21130045', 'Ana Sofía Ramírez Torres',      'ALUMNO',  1),
 ( 2, 'A21130078', 'Luis Fernando Gómez Díaz',      'ALUMNO',  1),
 ( 3, 'A22130112', 'Valeria Hernández Cruz',        'ALUMNO',  1),
 ( 4, 'A22140033', 'Diego Alejandro Martínez Ruiz', 'ALUMNO',  2),
 ( 5, 'A23140057', 'Camila Flores Medina',          'ALUMNO',  2),
 ( 6, 'A23150021', 'Jorge Iván Sánchez Pérez',      'ALUMNO',  3),
 ( 7, 'D1001',     'Dra. Patricia Navarro Salinas', 'DOCENTE', 1),
 ( 8, 'D1002',     'Mtro. Héctor Aguilar Ríos',     'DOCENTE', 2),
 ( 9, 'D1003',     'Ing. Laura Jiménez Campos',     'DOCENTE', 3);

INSERT INTO equipos (id_equipo, codigo_barras, descripcion, ubicacion) VALUES
 ( 1, 'INV000101', 'Laptop HP ProBook 440 G9',         'Almacén de TI'),
 ( 2, 'INV000102', 'Laptop HP ProBook 440 G9',         'Almacén de TI'),
 ( 3, 'INV000103', 'Laptop Lenovo ThinkPad E14',       'Almacén de TI'),
 ( 4, 'INV000104', 'Laptop Lenovo ThinkPad E14',       'Almacén de TI'),
 ( 5, 'INV000105', 'Laptop Dell Latitude 3440',        'Almacén de TI'),
 ( 6, 'INV000106', 'Laptop Dell Latitude 3440',        'Almacén de TI'),
 ( 7, 'INV000107', 'Laptop Apple MacBook Air M2',      'Almacén de TI'),
 ( 8, 'INV000108', 'PC HP ProDesk 400 G9',             'Laboratorio de Programación'),
 ( 9, 'INV000109', 'PC HP ProDesk 400 G9',             'Laboratorio de Programación'),
 (10, 'INV000110', 'PC HP ProDesk 400 G9',             'Laboratorio de Programación'),
 (11, 'INV000111', 'PC Lenovo ThinkCentre M70s',       'Laboratorio de Redes'),
 (12, 'INV000112', 'PC Lenovo ThinkCentre M70s',       'Laboratorio de Redes'),
 (13, 'INV000113', 'PC Dell OptiPlex 7010',            'Almacén de TI'),
 (14, 'INV000114', 'Proyector Epson PowerLite E20',    'Almacén de TI'),
 (15, 'INV000115', 'Proyector Epson PowerLite E20',    'Almacén de TI'),
 (16, 'INV000116', 'Proyector BenQ MS560',             'Almacén de TI'),
 (17, 'INV000117', 'Tablet Samsung Galaxy Tab A9+',    'Almacén de TI'),
 (18, 'INV000118', 'Tablet Samsung Galaxy Tab A9+',    'Almacén de TI'),
 (19, 'INV000119', 'Tablet Apple iPad 10',             'Almacén de TI'),
 (20, 'INV000120', 'Impresora HP LaserJet Pro M404dn', 'Almacén de TI'),
 (21, 'INV000121', 'Impresora Epson EcoTank L3250',    'Almacén de TI'),
 (22, 'INV000122', 'Monitor Dell P2422H',              'Laboratorio de Programación'),
 (23, 'INV000123', 'Monitor Dell P2422H',              'Laboratorio de Programación'),
 (24, 'INV000124', 'Switch Cisco Catalyst 2960-L',     'Almacén de TI'),
 (25, 'INV000125', 'Switch Cisco Catalyst 2960-L',     'Almacén de TI'),
 (26, 'INV000126', 'Router TP-Link Archer AX55',       'Almacén de TI'),
 (27, 'INV000127', 'Cámara web Logitech C920',         'Almacén de TI'),
 (28, 'INV000128', 'Cámara web Logitech C920',         'Almacén de TI'),
 (29, 'INV000129', 'Laptop HP 240 G8',                 'Almacén de TI'),
 (30, 'INV000130', 'PC HP ProDesk 400 G6',             'Almacén de TI');

INSERT INTO prestamos (id_equipo, id_solicitante, fecha_prestamo, fecha_limite, fecha_devolucion) VALUES
 ( 1, 1, NOW() - INTERVAL 60 DAY, NOW() - INTERVAL 53 DAY, NOW() - INTERVAL 52 DAY),
 ( 1, 7, NOW() - INTERVAL 30 DAY, NOW() - INTERVAL 23 DAY, NOW() - INTERVAL 24 DAY),
 ( 3, 3, NOW() - INTERVAL 45 DAY, NOW() - INTERVAL 38 DAY, NOW() - INTERVAL 36 DAY),
 ( 5, 7, NOW() - INTERVAL 40 DAY, NOW() - INTERVAL 33 DAY, NOW() - INTERVAL 34 DAY),
 ( 5, 2, NOW() - INTERVAL 20 DAY, NOW() - INTERVAL 13 DAY, NOW() - INTERVAL 13 DAY),
 (14, 8, NOW() - INTERVAL 25 DAY, NOW() - INTERVAL 22 DAY, NOW() - INTERVAL 22 DAY),
 (14, 9, NOW() - INTERVAL 15 DAY, NOW() - INTERVAL 12 DAY, NOW() - INTERVAL 11 DAY),
 (14, 7, NOW() - INTERVAL  8 DAY, NOW() - INTERVAL  5 DAY, NOW() - INTERVAL  5 DAY),
 (17, 5, NOW() - INTERVAL 28 DAY, NOW() - INTERVAL 21 DAY, NOW() - INTERVAL 22 DAY);

INSERT INTO prestamos (id_equipo, id_solicitante, fecha_prestamo, fecha_limite) VALUES
 ( 2, 1, NOW() - INTERVAL 10 DAY, NOW() - INTERVAL 3 DAY),
 (16, 8, NOW() - INTERVAL  5 DAY, NOW() - INTERVAL 2 DAY),
 ( 4, 3, NOW() - INTERVAL  2 DAY, NOW() + INTERVAL 5 DAY),
 (18, 5, NOW() - INTERVAL  1 DAY, NOW() + INTERVAL 6 DAY);

INSERT INTO asignaciones (id_equipo, id_solicitante, id_departamento, ubicacion, fecha_asignacion, fecha_fin) VALUES
 (11, 7, NULL, 'Cubículo D-12', NOW() - INTERVAL 150 DAY, NOW() - INTERVAL 100 DAY);

INSERT INTO asignaciones (id_equipo, id_solicitante, id_departamento, ubicacion, fecha_asignacion) VALUES
 (13, NULL, 5,    'Oficina de Dirección Académica', NOW() - INTERVAL  90 DAY),
 (20, NULL, 5,    'Sala de Maestros',               NOW() - INTERVAL  85 DAY),
 (24, NULL, 1,    'Laboratorio de Redes',           NOW() - INTERVAL 150 DAY),
 (25, NULL, 1,    'Laboratorio de Redes',           NOW() - INTERVAL 150 DAY),
 ( 9, 7,    NULL, 'Cubículo D-12',                  NOW() - INTERVAL  40 DAY),
 ( 3, 9,    NULL, 'Aula B-204',                     NOW() - INTERVAL  20 DAY);

UPDATE equipos SET estado = 'PRESTADO' WHERE id_equipo IN (2, 16, 4, 18);
UPDATE equipos e
  JOIN asignaciones a ON a.id_equipo = e.id_equipo AND a.fecha_fin IS NULL
   SET e.estado = 'ASIGNADO', e.ubicacion = a.ubicacion;

SET @usuario_app = NULL;
