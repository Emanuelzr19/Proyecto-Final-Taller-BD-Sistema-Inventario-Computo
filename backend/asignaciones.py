from backend.conexion import ErrorSistema, consultar, llamar
from backend.equipos import normalizar
from backend.seguridad import requiere


def activas():
    return consultar("""
        SELECT e.codigo_barras, e.descripcion, COALESCE(s.nombre_completo, d.nombre) AS asignado_a,
               a.ubicacion, a.fecha_asignacion
          FROM asignaciones a
          JOIN equipos e            ON e.id_equipo = a.id_equipo
          LEFT JOIN solicitantes s  ON s.id_solicitante = a.id_solicitante
          LEFT JOIN departamentos d ON d.id_departamento = a.id_departamento
         WHERE a.fecha_fin IS NULL
         ORDER BY a.fecha_asignacion DESC""")


def asignar(codigo, ubicacion, matricula=None, id_departamento=None):
    requiere("asignaciones")
    matricula = normalizar(matricula) or None
    if (matricula is None) == (id_departamento is None):
        raise ErrorSistema("Indique una matrícula o un departamento (solo uno).")
    if not ubicacion.strip():
        raise ErrorSistema("Indique la nueva ubicación del equipo.")
    salida, _ = llamar("sp_asignar_equipo",
                       (normalizar(codigo), matricula, id_departamento, ubicacion.strip(), 0))
    return salida[4]


def finalizar(codigo, ubicacion):
    requiere("asignaciones")
    if not ubicacion.strip():
        raise ErrorSistema("Indique la ubicación a la que regresa el equipo.")
    llamar("sp_finalizar_asignacion", (normalizar(codigo), ubicacion.strip()))
