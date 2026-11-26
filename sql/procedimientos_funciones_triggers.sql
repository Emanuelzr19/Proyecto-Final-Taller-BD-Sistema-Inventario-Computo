SET NAMES utf8mb4;
USE inventario_computo;

DELIMITER $$

CREATE FUNCTION fn_dias_retraso(p_id_prestamo INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_limite     DATETIME;
    DECLARE v_devolucion DATETIME;

    SELECT fecha_limite, fecha_devolucion INTO v_limite, v_devolucion
      FROM prestamos WHERE id_prestamo = p_id_prestamo;

    RETURN GREATEST(0, DATEDIFF(COALESCE(v_devolucion, NOW()), v_limite));
END $$

CREATE FUNCTION fn_equipo_disponible(p_id_equipo INT)
RETURNS TINYINT
READS SQL DATA
BEGIN
    DECLARE v_estado VARCHAR(20);

    SELECT estado INTO v_estado FROM equipos WHERE id_equipo = p_id_equipo;

    RETURN IF(v_estado = 'DISPONIBLE', 1, 0);
END $$

CREATE PROCEDURE sp_buscar_equipo(IN p_codigo VARCHAR(30))
BEGIN
    SELECT e.codigo_barras, e.descripcion, e.ubicacion, e.estado,
           s.nombre_completo                      AS prestado_a,
           p.fecha_limite,
           fn_dias_retraso(p.id_prestamo)         AS dias_retraso,
           COALESCE(sa.nombre_completo, d.nombre) AS asignado_a
      FROM equipos e
      LEFT JOIN prestamos p     ON p.id_equipo = e.id_equipo AND p.fecha_devolucion IS NULL
      LEFT JOIN solicitantes s  ON s.id_solicitante = p.id_solicitante
      LEFT JOIN asignaciones a  ON a.id_equipo = e.id_equipo AND a.fecha_fin IS NULL
      LEFT JOIN solicitantes sa ON sa.id_solicitante = a.id_solicitante
      LEFT JOIN departamentos d ON d.id_departamento = a.id_departamento
     WHERE e.codigo_barras = p_codigo;
END $$

CREATE PROCEDURE sp_historial_equipo(IN p_codigo VARCHAR(30))
BEGIN
    SELECT 'PRÉSTAMO' AS movimiento, p.fecha_prestamo AS inicio, p.fecha_devolucion AS fin,
           s.nombre_completo AS destino
      FROM prestamos p
      JOIN equipos e      ON e.id_equipo = p.id_equipo
      JOIN solicitantes s ON s.id_solicitante = p.id_solicitante
     WHERE e.codigo_barras = p_codigo
    UNION ALL
    SELECT 'ASIGNACIÓN', a.fecha_asignacion, a.fecha_fin,
           CONCAT(COALESCE(s.nombre_completo, d.nombre), ' - ', a.ubicacion)
      FROM asignaciones a
      JOIN equipos e            ON e.id_equipo = a.id_equipo
      LEFT JOIN solicitantes s  ON s.id_solicitante = a.id_solicitante
      LEFT JOIN departamentos d ON d.id_departamento = a.id_departamento
     WHERE e.codigo_barras = p_codigo
     ORDER BY inicio DESC;
END $$

CREATE PROCEDURE sp_registrar_prestamo(
    IN  p_codigo      VARCHAR(30),
    IN  p_matricula   VARCHAR(20),
    IN  p_dias        INT,
    OUT p_id_prestamo INT)
BEGIN
    DECLARE v_id_equipo      INT DEFAULT NULL;
    DECLARE v_id_solicitante INT DEFAULT NULL;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT id_equipo INTO v_id_equipo FROM equipos WHERE codigo_barras = p_codigo FOR UPDATE;
    SELECT id_solicitante INTO v_id_solicitante FROM solicitantes WHERE matricula = p_matricula;

    IF v_id_equipo IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un equipo con ese código de barras.';
    END IF;
    IF v_id_solicitante IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un alumno o docente con esa matrícula.';
    END IF;
    IF p_dias < 1 OR p_dias > 30 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los días de préstamo deben estar entre 1 y 30.';
    END IF;

    INSERT INTO prestamos (id_equipo, id_solicitante, fecha_prestamo, fecha_limite)
    VALUES (v_id_equipo, v_id_solicitante, NOW(), NOW() + INTERVAL p_dias DAY);
    SET p_id_prestamo = LAST_INSERT_ID();

    UPDATE equipos SET estado = 'PRESTADO' WHERE id_equipo = v_id_equipo;

    COMMIT;
END $$

CREATE PROCEDURE sp_registrar_devolucion(
    IN  p_codigo       VARCHAR(30),
    OUT p_dias_retraso INT)
BEGIN
    DECLARE v_id_equipo   INT DEFAULT NULL;
    DECLARE v_id_prestamo INT DEFAULT NULL;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT e.id_equipo, p.id_prestamo INTO v_id_equipo, v_id_prestamo
      FROM equipos e
      JOIN prestamos p ON p.id_equipo = e.id_equipo AND p.fecha_devolucion IS NULL
     WHERE e.codigo_barras = p_codigo
       FOR UPDATE;

    IF v_id_prestamo IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ese equipo no tiene un préstamo activo.';
    END IF;

    UPDATE prestamos SET fecha_devolucion = NOW() WHERE id_prestamo = v_id_prestamo;
    UPDATE equipos   SET estado = 'DISPONIBLE'     WHERE id_equipo   = v_id_equipo;

    COMMIT;

    SET p_dias_retraso = fn_dias_retraso(v_id_prestamo);
END $$

CREATE PROCEDURE sp_asignar_equipo(
    IN  p_codigo          VARCHAR(30),
    IN  p_matricula       VARCHAR(20),
    IN  p_id_departamento INT,
    IN  p_ubicacion       VARCHAR(100),
    OUT p_id_asignacion   INT)
BEGIN
    DECLARE v_id_equipo      INT DEFAULT NULL;
    DECLARE v_id_solicitante INT DEFAULT NULL;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT id_equipo INTO v_id_equipo FROM equipos WHERE codigo_barras = p_codigo FOR UPDATE;
    IF v_id_equipo IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un equipo con ese código de barras.';
    END IF;

    IF p_matricula IS NOT NULL THEN
        SELECT id_solicitante INTO v_id_solicitante FROM solicitantes WHERE matricula = p_matricula;
        IF v_id_solicitante IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe un alumno o docente con esa matrícula.';
        END IF;
    END IF;

    INSERT INTO asignaciones (id_equipo, id_solicitante, id_departamento, ubicacion)
    VALUES (v_id_equipo, v_id_solicitante, p_id_departamento, p_ubicacion);
    SET p_id_asignacion = LAST_INSERT_ID();

    UPDATE equipos SET estado = 'ASIGNADO', ubicacion = p_ubicacion WHERE id_equipo = v_id_equipo;

    COMMIT;
END $$

CREATE PROCEDURE sp_finalizar_asignacion(
    IN p_codigo    VARCHAR(30),
    IN p_ubicacion VARCHAR(100))
BEGIN
    DECLARE v_id_equipo     INT DEFAULT NULL;
    DECLARE v_id_asignacion INT DEFAULT NULL;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT e.id_equipo, a.id_asignacion INTO v_id_equipo, v_id_asignacion
      FROM equipos e
      JOIN asignaciones a ON a.id_equipo = e.id_equipo AND a.fecha_fin IS NULL
     WHERE e.codigo_barras = p_codigo
       FOR UPDATE;

    IF v_id_asignacion IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ese equipo no tiene una asignación activa.';
    END IF;

    UPDATE asignaciones SET fecha_fin = NOW() WHERE id_asignacion = v_id_asignacion;
    UPDATE equipos SET estado = 'DISPONIBLE', ubicacion = p_ubicacion WHERE id_equipo = v_id_equipo;

    COMMIT;
END $$

CREATE TRIGGER trg_equipos_validar
BEFORE INSERT ON equipos
FOR EACH ROW
BEGIN
    IF NEW.codigo_barras IS NULL OR TRIM(NEW.codigo_barras) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El código de barras no puede estar vacío.';
    END IF;
END $$

CREATE TRIGGER trg_prestamos_validar
BEFORE INSERT ON prestamos
FOR EACH ROW
BEGIN
    IF fn_equipo_disponible(NEW.id_equipo) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El equipo no está disponible: ya está prestado o asignado.';
    END IF;
END $$

CREATE TRIGGER trg_asignaciones_validar
BEFORE INSERT ON asignaciones
FOR EACH ROW
BEGIN
    IF fn_equipo_disponible(NEW.id_equipo) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El equipo no está disponible: ya está prestado o asignado.';
    END IF;
END $$

CREATE TRIGGER trg_auditoria_equipos
AFTER UPDATE ON equipos
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, operacion, usuario, datos_anteriores, datos_nuevos)
    VALUES ('equipos', 'UPDATE', COALESCE(@usuario_app, USER()),
            CONCAT(OLD.codigo_barras, ' | estado: ', OLD.estado, ' | ubicación: ', OLD.ubicacion),
            CONCAT(NEW.codigo_barras, ' | estado: ', NEW.estado, ' | ubicación: ', NEW.ubicacion));
END $$

CREATE TRIGGER trg_auditoria_prestamos
AFTER INSERT ON prestamos
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, operacion, usuario, datos_anteriores, datos_nuevos)
    VALUES ('prestamos', 'INSERT', COALESCE(@usuario_app, USER()), NULL,
            CONCAT('préstamo ', NEW.id_prestamo, ' | equipo ', NEW.id_equipo,
                   ' | solicitante ', NEW.id_solicitante, ' | límite ', NEW.fecha_limite));
END $$

DELIMITER ;
