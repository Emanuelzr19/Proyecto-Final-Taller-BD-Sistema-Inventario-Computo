import hashlib

from backend.conexion import ErrorSistema, consultar, establecer_usuario

PERMISOS = {
    "ADMINISTRADOR": {"equipos.registrar", "equipos.editar", "prestamos", "asignaciones",
                      "solicitantes", "reportes"},
    "OPERADOR": {"equipos.registrar", "prestamos", "asignaciones", "reportes"},
    "CONSULTA": {"reportes"},
}

usuario_actual = None


def iniciar_sesion(nombre_usuario, password):
    global usuario_actual
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    filas = consultar(
        "SELECT id_usuario, nombre_completo, nombre_usuario, rol, estado FROM usuarios "
        "WHERE nombre_usuario = %s AND password_hash = %s",
        (nombre_usuario.strip(), password_hash))
    if not filas:
        raise ErrorSistema("Usuario o contraseña incorrectos.")
    if filas[0]["estado"] != "ACTIVO":
        raise ErrorSistema("La cuenta está inactiva.")
    usuario_actual = filas[0]
    establecer_usuario(usuario_actual["nombre_usuario"])
    return usuario_actual


def cerrar_sesion():
    global usuario_actual
    usuario_actual = None
    establecer_usuario(None)


def puede(permiso):
    return usuario_actual is not None and permiso in PERMISOS[usuario_actual["rol"]]


def requiere(permiso):
    if usuario_actual is None:
        raise ErrorSistema("Debe iniciar sesión.")
    if not puede(permiso):
        raise ErrorSistema(f"Su rol ({usuario_actual['rol']}) no tiene permiso para esta operación.")
