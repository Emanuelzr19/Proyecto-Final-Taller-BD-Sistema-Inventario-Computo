from tkinter import ttk

from backend import equipos, seguridad
from backend.conexion import ErrorSistema
from frontend.componentes import (SUBTITULO, TITULO, EntradaCodigo, Tabla, aviso, confirmar, error,
                                  formatear, info, pedir_datos)


class PantallaEquipos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        ttk.Label(self, text="Equipos", font=TITULO).pack(anchor="w")

        self.lector = EntradaCodigo(self, "Escanee el código del equipo:", self.buscar)
        self.lector.pack(anchor="w", pady=10)
        self.lbl_info = ttk.Label(self, text="", font=("Segoe UI", 10, "bold"), justify="left")
        self.lbl_info.pack(anchor="w")
        ttk.Label(self, text="Historial de préstamos y asignaciones").pack(anchor="w", pady=(10, 2))
        self.historial = Tabla(self, [("movimiento", "Movimiento", 110), ("inicio", "Inicio", 140),
                                      ("fin", "Fin", 140), ("destino", "Destino", 420)], alto=5)
        self.historial.pack(fill="x")

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(15, 5))
        ttk.Label(barra, text="Inventario", font=SUBTITULO).pack(side="left")
        ttk.Button(barra, text="Registrar equipo", command=self.registrar).pack(side="right")
        ttk.Button(barra, text="Editar seleccionado", command=self.editar).pack(side="right", padx=5)
        self.tabla = Tabla(self, [("codigo_barras", "Código", 110), ("descripcion", "Descripción", 280),
                                  ("ubicacion", "Ubicación", 260), ("estado", "Estado", 110)])
        self.tabla.pack(fill="both", expand=True)

    def mostrar(self):
        try:
            self.tabla.cargar(equipos.listar())
        except ErrorSistema as e:
            error(self, e)
        self.lector.limpiar()

    def buscar(self, codigo):
        try:
            equipo = equipos.buscar(codigo)
            if equipo is None:
                self.lbl_info.configure(text=f"El código {codigo} no está registrado.")
                self.historial.cargar([])
                if seguridad.puede("equipos.registrar") and confirmar(
                        self, f"El código {codigo} no existe. ¿Desea registrar el equipo?"):
                    self.registrar(codigo)
                return
            texto = (f"{equipo['codigo_barras']}  |  {equipo['descripcion']}\n"
                     f"Estado: {equipo['estado']}  |  Ubicación: {equipo['ubicacion']}")
            if equipo["prestado_a"]:
                texto += (f"\nPrestado a: {equipo['prestado_a']}  (límite {formatear(equipo['fecha_limite'])}, "
                          f"días de retraso: {equipo['dias_retraso']})")
            if equipo["asignado_a"]:
                texto += f"\nAsignado a: {equipo['asignado_a']}"
            self.lbl_info.configure(text=texto)
            self.historial.cargar(equipos.historial(codigo))
        except ErrorSistema as e:
            error(self, e)

    def registrar(self, codigo=""):
        if not seguridad.puede("equipos.registrar"):
            aviso(self, "Su rol no puede registrar equipos.")
            return
        datos = pedir_datos(self, "Registrar equipo", [
            ("codigo_barras", "Código de barras", None), ("descripcion", "Descripción", None),
            ("ubicacion", "Ubicación", None)], {"codigo_barras": codigo, "ubicacion": "Almacén de TI"})
        if not datos:
            return
        try:
            equipos.registrar(datos["codigo_barras"], datos["descripcion"], datos["ubicacion"])
        except ErrorSistema as e:
            error(self, e)
            return
        info(self, "Equipo registrado.")
        self.mostrar()

    def editar(self):
        if not seguridad.puede("equipos.editar"):
            aviso(self, "Solo el administrador puede editar equipos.")
            return
        fila = self.tabla.seleccion()
        if fila is None:
            aviso(self, "Seleccione un equipo de la lista.")
            return
        datos = pedir_datos(self, f"Editar {fila['codigo_barras']}", [
            ("descripcion", "Descripción", None), ("ubicacion", "Ubicación", None)], fila)
        if not datos:
            return
        try:
            equipos.editar(fila["id_equipo"], datos["descripcion"], datos["ubicacion"])
        except ErrorSistema as e:
            error(self, e)
            return
        self.mostrar()
