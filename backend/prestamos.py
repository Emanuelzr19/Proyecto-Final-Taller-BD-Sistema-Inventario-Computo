from backend.conexion import consultar, llamar
from backend.equipos import normalizar
from backend.seguridad import requiere


def activos():
    return consultar("""
        SELECT e.codigo_barras, e.descripcion, s.matricula, s.nombre_completo,
               p.fecha_prestamo, p.fecha_limite, fn_dias_retraso(p.id_prestamo) AS dias_retraso
          FROM prestamos p
          JOIN equipos e      ON e.id_equipo = p.id_equipo
          JOIN solicitantes s ON s.id_solicitante = p.id_solicitante
         WHERE p.fecha_devolucion IS NULL
         ORDER BY p.fecha_limite""")


def prestar(codigo, matricula, dias):
    requiere("prestamos")
    salida, _ = llamar("sp_registrar_prestamo", (normalizar(codigo), normalizar(matricula), int(dias), 0))
    return salida[3]


def devolver(codigo):
    requiere("prestamos")
    salida, _ = llamar("sp_registrar_devolucion", (normalizar(codigo), 0))
    return salida[1]
