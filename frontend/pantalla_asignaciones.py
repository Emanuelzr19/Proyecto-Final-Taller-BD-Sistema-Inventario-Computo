import tkinter as tk
from tkinter import ttk

from backend import asignaciones, solicitantes
from backend.conexion import ErrorSistema
from frontend.componentes import TITULO, EntradaCodigo, Tabla, aviso, confirmar, error, info


class PantallaAsignaciones(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.departamentos = {}
        ttk.Label(self, text="Asignaciones", font=TITULO).pack(anchor="w")

        caja = ttk.LabelFrame(self, text="Nueva asignación", padding=10)
        caja.pack(fill="x", pady=10)
        self.equipo = EntradaCodigo(caja, "Equipo:", lambda _c: self.ent_matricula.focus_set())
        self.equipo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.var_destino = tk.StringVar(value="persona")
        ttk.Radiobutton(caja, text="Alumno o docente (matrícula):", value="persona",
                        variable=self.var_destino).grid(row=1, column=0, sticky="w")
        self.var_matricula = tk.StringVar()
        self.ent_matricula = ttk.Entry(caja, textvariable=self.var_matricula, width=18)
        self.ent_matricula.grid(row=1, column=1, sticky="w", padx=6)
        ttk.Radiobutton(caja, text="Departamento:", value="departamento",
                        variable=self.var_destino).grid(row=2, column=0, sticky="w", pady=4)
        self.var_depto = tk.StringVar()
        self.cmb_depto = ttk.Combobox(caja, textvariable=self.var_depto, state="readonly", width=30)
        self.cmb_depto.grid(row=2, column=1, sticky="w", padx=6)
        ttk.Label(caja, text="Nueva ubicación:").grid(row=3, column=0, sticky="w")
        self.var_ubicacion = tk.StringVar()
        ttk.Entry(caja, textvariable=self.var_ubicacion, width=40).grid(row=3, column=1, sticky="w", padx=6)
        ttk.Button(caja, text="Asignar equipo", command=self.asignar).grid(row=4, column=0, sticky="w", pady=8)

        caja2 = ttk.LabelFrame(self, text="Finalizar asignación", padding=10)
        caja2.pack(fill="x")
        ttk.Label(caja2, text="Regresa a:").pack(side="left")
        self.var_regreso = tk.StringVar(value="Almacén de TI")
        ttk.Entry(caja2, textvariable=self.var_regreso, width=22).pack(side="left", padx=6)
        self.fin = EntradaCodigo(caja2, "Equipo:", self.finalizar)
        self.fin.pack(side="left", padx=10)

        ttk.Label(self, text="Asignaciones activas").pack(anchor="w", pady=(12, 2))
        self.tabla = Tabla(self, [("codigo_barras", "Código", 100), ("descripcion", "Equipo", 230),
                                  ("asignado_a", "Asignado a", 240), ("ubicacion", "Ubicación", 220),
                                  ("fecha_asignacion", "Desde", 130)])
        self.tabla.pack(fill="both", expand=True)

    def mostrar(self):
        try:
            self.departamentos = {d["nombre"]: d["id_departamento"] for d in solicitantes.departamentos()}
            self.cmb_depto.configure(values=list(self.departamentos))
            self.tabla.cargar(asignaciones.activas())
        except ErrorSistema as e:
            error(self, e)
        self.equipo.limpiar()

    def asignar(self):
        codigo, ubicacion = self.equipo.valor(), self.var_ubicacion.get()
        if self.var_destino.get() == "persona":
            matricula, id_depto, destino = self.var_matricula.get(), None, self.var_matricula.get()
        else:
            matricula, id_depto, destino = None, self.departamentos.get(self.var_depto.get()), self.var_depto.get()
        if not codigo or not destino.strip():
            aviso(self, "Escanee el equipo e indique el destino.")
            return
        if not confirmar(self, f"¿Asignar {codigo} a {destino} en «{ubicacion}»?"):
            return
        try:
            id_asignacion = asignaciones.asignar(codigo, ubicacion, matricula, id_depto)
        except ErrorSistema as e:
            error(self, e)
            return
        info(self, f"Asignación #{id_asignacion} registrada.")
        self.var_matricula.set("")
        self.var_ubicacion.set("")
        self.mostrar()

    def finalizar(self, codigo):
        if not confirmar(self, f"¿Finalizar la asignación de {codigo}?"):
            return
        try:
            asignaciones.finalizar(codigo, self.var_regreso.get())
        except ErrorSistema as e:
            error(self, e)
            return
        info(self, "Asignación finalizada; el equipo quedó DISPONIBLE.")
        self.fin.limpiar()
        self.mostrar()
