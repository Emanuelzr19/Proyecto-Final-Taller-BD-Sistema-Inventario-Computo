from tkinter import ttk

from backend import reportes
from backend.conexion import ErrorSistema
from frontend.componentes import SUBTITULO, TITULO, Tabla, error


class PantallaReportes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        ttk.Label(self, text="Reportes", font=TITULO).pack(anchor="w")

        ttk.Label(self, text="Equipos con más asignaciones y préstamos", font=SUBTITULO).pack(anchor="w", pady=(10, 2))
        self.tabla1 = Tabla(self, [("lugar", "Lugar", 60), ("codigo_barras", "Código", 100),
                                   ("descripcion", "Equipo", 280), ("asignaciones", "Asignaciones", 100),
                                   ("prestamos", "Préstamos", 100), ("total", "Total", 80)])
        self.tabla1.pack(fill="both", expand=True)

        ttk.Label(self, text="Departamentos con mayor cantidad de equipos", font=SUBTITULO).pack(anchor="w", pady=(15, 2))
        self.tabla2 = Tabla(self, [("departamento", "Departamento", 260), ("equipos", "Equipos", 90),
                                   ("al_departamento", "Al departamento", 130),
                                   ("a_su_personal", "A su personal", 130)], alto=6)
        self.tabla2.pack(fill="both", expand=True)

    def mostrar(self):
        try:
            self.tabla1.cargar(reportes.equipos_con_mas_asignaciones())
            self.tabla2.cargar(reportes.departamentos_con_mas_equipos())
        except ErrorSistema as e:
            error(self, e)
