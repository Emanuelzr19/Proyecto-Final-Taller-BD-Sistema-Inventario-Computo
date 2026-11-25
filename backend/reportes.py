from backend.conexion import consultar
from backend.seguridad import requiere


def equipos_con_mas_asignaciones():
    requiere("reportes")
    return consultar("""
        WITH movimientos AS (
            SELECT id_equipo, 'ASIGNACION' AS tipo FROM asignaciones
            UNION ALL
            SELECT id_equipo, 'PRESTAMO' FROM prestamos
        )
        SELECT RANK() OVER (ORDER BY COUNT(*) DESC) AS lugar,
               e.codigo_barras,
               e.descripcion,
               SUM(m.tipo = 'ASIGNACION') AS asignaciones,
               SUM(m.tipo = 'PRESTAMO')   AS prestamos,
               COUNT(*)                   AS total
          FROM movimientos m
          JOIN equipos e ON e.id_equipo = m.id_equipo
         GROUP BY e.id_equipo, e.codigo_barras, e.descripcion
         ORDER BY total DESC, e.codigo_barras
         LIMIT 10""")


def departamentos_con_mas_equipos():
    requiere("reportes")
    return consultar("""
        SELECT d.nombre                           AS departamento,
               COUNT(*)                           AS equipos,
               SUM(a.id_departamento IS NOT NULL) AS al_departamento,
               SUM(a.id_solicitante IS NOT NULL)  AS a_su_personal
          FROM asignaciones a
          LEFT JOIN solicitantes s ON s.id_solicitante = a.id_solicitante
          JOIN departamentos d     ON d.id_departamento = COALESCE(a.id_departamento, s.id_departamento)
         WHERE a.fecha_fin IS NULL
         GROUP BY d.id_departamento, d.nombre
        HAVING COUNT(*) > 0
         ORDER BY equipos DESC, departamento""")
