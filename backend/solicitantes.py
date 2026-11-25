from backend.conexion import ErrorSistema, consultar, ejecutar
from backend.equipos import normalizar
from backend.seguridad import requiere


def departamentos():
    return consultar("SELECT id_departamento, nombre FROM departamentos ORDER BY nombre")


def listar():
    return consultar("""
        SELECT s.id_solicitante, s.matricula, s.nombre_completo, s.tipo, s.id_departamento,
               d.nombre AS departamento
          FROM solicitantes s
          JOIN departamentos d ON d.id_departamento = s.id_departamento
         ORDER BY s.nombre_completo""")


def guardar(matricula, nombre_completo, tipo, id_departamento, id_solicitante=None):
    requiere("solicitantes")
    if not matricula.strip() or not nombre_completo.strip():
        raise ErrorSistema("Capture la matrícula y el nombre.")
    datos = (normalizar(matricula), nombre_completo.strip(), tipo, id_departamento)
    if id_solicitante is None:
        ejecutar("INSERT INTO solicitantes (matricula, nombre_completo, tipo, id_departamento) "
                 "VALUES (%s, %s, %s, %s)", datos)
    else:
        ejecutar("UPDATE solicitantes SET matricula = %s, nombre_completo = %s, tipo = %s, "
                 "id_departamento = %s WHERE id_solicitante = %s", datos + (id_solicitante,))
