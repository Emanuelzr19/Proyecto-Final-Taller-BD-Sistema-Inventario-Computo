from tkinter import ttk

from backend import seguridad, solicitantes
from backend.conexion import ErrorSistema
from frontend.componentes import TITULO, Tabla, aviso, error, pedir_datos


class PantallaSolicitantes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.departamentos = {}
        barra = ttk.Frame(self)
        barra.pack(fill="x")
        ttk.Label(barra, text="Alumnos y docentes", font=TITULO).pack(side="left")
        ttk.Button(barra, text="Nuevo", command=self.nuevo).pack(side="right")
        ttk.Button(barra, text="Editar seleccionado", command=self.editar).pack(side="right", padx=5)
        self.tabla = Tabla(self, [("matricula", "Matrícula", 110), ("nombre_completo", "Nombre", 280),
                                  ("tipo", "Tipo", 100), ("departamento", "Departamento", 240)], alto=20)
        self.tabla.pack(fill="both", expand=True, pady=10)

    def mostrar(self):
        try:
            self.departamentos = {d["nombre"]: d["id_departamento"] for d in solicitantes.departamentos()}
            self.tabla.cargar(solicitantes.listar())
        except ErrorSistema as e:
            error(self, e)

    def _formulario(self, titulo, valores):
        if not seguridad.puede("solicitantes"):
            aviso(self, "Solo el administrador puede modificar alumnos y docentes.")
            return None
        return pedir_datos(self, titulo, [
            ("matricula", "Matrícula / No. empleado", None), ("nombre_completo", "Nombre completo", None),
            ("tipo", "Tipo", ["ALUMNO", "DOCENTE"]),
            ("departamento", "Departamento", list(self.departamentos))], valores)

    def nuevo(self):
        datos = self._formulario("Nuevo alumno o docente", {"tipo": "ALUMNO"})
        if datos:
            self._guardar(datos, None)

    def editar(self):
        fila = self.tabla.seleccion()
        if fila is None:
            aviso(self, "Seleccione un registro.")
            return
        datos = self._formulario("Editar", fila)
        if datos:
            self._guardar(datos, fila["id_solicitante"])

    def _guardar(self, datos, id_solicitante):
        try:
            solicitantes.guardar(datos["matricula"], datos["nombre_completo"], datos["tipo"],
                                 self.departamentos[datos["departamento"]], id_solicitante)
        except ErrorSistema as e:
            error(self, e)
            return
        self.mostrar()
