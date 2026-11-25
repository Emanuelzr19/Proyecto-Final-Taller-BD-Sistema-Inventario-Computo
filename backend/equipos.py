from backend.conexion import ErrorSistema, consultar, ejecutar, llamar
from backend.seguridad import requiere


def normalizar(codigo):
    return (codigo or "").strip().upper()


def buscar(codigo):
    _, filas = llamar("sp_buscar_equipo", (normalizar(codigo),))
    return filas[0] if filas else None


def historial(codigo):
    _, filas = llamar("sp_historial_equipo", (normalizar(codigo),))
    return filas


def listar():
    return consultar("SELECT * FROM equipos ORDER BY codigo_barras")


def registrar(codigo, descripcion, ubicacion):
    requiere("equipos.registrar")
    if not descripcion.strip() or not ubicacion.strip():
        raise ErrorSistema("Capture la descripción y la ubicación.")
    ejecutar("INSERT INTO equipos (codigo_barras, descripcion, ubicacion) VALUES (%s, %s, %s)",
             (normalizar(codigo), descripcion.strip(), ubicacion.strip()))


def editar(id_equipo, descripcion, ubicacion):
    requiere("equipos.editar")
    if not descripcion.strip() or not ubicacion.strip():
        raise ErrorSistema("Capture la descripción y la ubicación.")
    ejecutar("UPDATE equipos SET descripcion = %s, ubicacion = %s WHERE id_equipo = %s",
             (descripcion.strip(), ubicacion.strip(), id_equipo))
