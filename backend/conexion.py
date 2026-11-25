import configparser
import os

import mysql.connector

RUTA_CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini")

_conexion = None
_usuario_app = None


class ErrorSistema(Exception):
    pass


def _mensaje(e):
    if e.sqlstate == "45000":
        return e.msg
    if e.errno == 1062:
        return "Ya existe un registro con ese valor (código de barras o matrícula duplicados)."
    if e.errno == 1452:
        return "Uno de los datos hace referencia a un registro que no existe."
    if e.errno == 3819:
        return "Los datos no cumplen una regla de validación de la base de datos."
    if e.errno in (1045, 1049, 2003, 2005):
        return f"No fue posible conectarse a MySQL. Revise config.ini.\n\n{e.msg}"
    return f"Error de base de datos ({e.errno}): {e.msg}"


def _conectar():
    global _conexion
    if _conexion is None or not _conexion.is_connected():
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.read(RUTA_CONFIG, encoding="utf-8")
        datos = cfg["mysql"]
        try:
            _conexion = mysql.connector.connect(
                host=datos.get("host", "localhost"),
                port=datos.getint("puerto", 3306),
                user=datos.get("usuario", "root"),
                password=datos.get("clave", ""),
                database=datos.get("base_datos", "inventario_computo"),
                autocommit=True,
            )
        except mysql.connector.Error as e:
            raise ErrorSistema(_mensaje(e)) from e
        _variable_auditoria()
    return _conexion


def _variable_auditoria():
    cursor = _conexion.cursor()
    cursor.execute("SET @usuario_app = %s", (_usuario_app,))
    cursor.close()


def establecer_usuario(nombre_usuario):
    global _usuario_app
    _usuario_app = nombre_usuario
    _conectar()
    _variable_auditoria()


def consultar(sql, params=()):
    try:
        cursor = _conectar().cursor(dictionary=True)
        cursor.execute(sql, params)
        filas = cursor.fetchall()
        cursor.close()
        return filas
    except mysql.connector.Error as e:
        raise ErrorSistema(_mensaje(e)) from e


def ejecutar(sql, params=()):
    try:
        cursor = _conectar().cursor()
        cursor.execute(sql, params)
        cursor.close()
    except mysql.connector.Error as e:
        raise ErrorSistema(_mensaje(e)) from e


def llamar(procedimiento, argumentos):
    try:
        cursor = _conectar().cursor()
        salida = cursor.callproc(procedimiento, argumentos)
        filas = []
        for resultado in cursor.stored_results():
            columnas = resultado.column_names
            filas = [dict(zip(columnas, fila)) for fila in resultado.fetchall()]
        cursor.close()
        return salida, filas
    except mysql.connector.Error as e:
        raise ErrorSistema(_mensaje(e)) from e
