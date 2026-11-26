import tkinter as tk
from tkinter import ttk

from backend import equipos, prestamos
from backend.conexion import ErrorSistema
from frontend.componentes import TITULO, EntradaCodigo, Tabla, aviso, confirmar, error, info


class PantallaPrestamos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        ttk.Label(self, text="Préstamos y devoluciones", font=TITULO).pack(anchor="w")

        caja = ttk.LabelFrame(self, text="Nuevo préstamo", padding=10)
        caja.pack(fill="x", pady=10)
        self.equipo = EntradaCodigo(caja, "1. Equipo:", self.equipo_leido)
        self.equipo.grid(row=0, column=0, columnspan=2, sticky="w")
        self.lbl_equipo = ttk.Label(caja, text="")
        self.lbl_equipo.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 8))
        ttk.Label(caja, text="2. Matrícula del alumno o docente:").grid(row=2, column=0, sticky="w")
        self.var_matricula = tk.StringVar()
        self.ent_matricula = ttk.Entry(caja, textvariable=self.var_matricula, width=16, font=("Consolas", 14))
        self.ent_matricula.grid(row=2, column=1, sticky="w", padx=6)
        self.ent_matricula.bind("<Return>", lambda _e: self.prestar())
        ttk.Label(caja, text="3. Días de préstamo:").grid(row=3, column=0, sticky="w", pady=6)
        self.var_dias = tk.StringVar(value="7")
        ttk.Spinbox(caja, from_=1, to=30, textvariable=self.var_dias, width=5).grid(row=3, column=1, sticky="w", padx=6)
        ttk.Button(caja, text="Registrar préstamo", command=self.prestar).grid(row=4, column=0, sticky="w")

        caja2 = ttk.LabelFrame(self, text="Devolución", padding=10)
        caja2.pack(fill="x")
        self.devolucion = EntradaCodigo(caja2, "Escanee el equipo que se devuelve:", self.devolver)
        self.devolucion.pack(anchor="w")

        ttk.Label(self, text="Préstamos activos (en rojo los vencidos)").pack(anchor="w", pady=(12, 2))
        self.tabla = Tabla(self, [("codigo_barras", "Código", 100), ("descripcion", "Equipo", 230),
                                  ("matricula", "Matrícula", 100), ("nombre_completo", "Solicitante", 220),
                                  ("fecha_prestamo", "Prestado", 130), ("fecha_limite", "Fecha límite", 130),
                                  ("dias_retraso", "Días de retraso", 100)])
        self.tabla.pack(fill="both", expand=True)

    def mostrar(self):
        try:
            self.tabla.cargar(prestamos.activos(), alerta=lambda f: f["dias_retraso"] > 0)
        except ErrorSistema as e:
            error(self, e)
        self.equipo.limpiar()

    def equipo_leido(self, codigo):
        try:
            equipo = equipos.buscar(codigo)
        except ErrorSistema as e:
            error(self, e)
            return
        texto = f"{equipo['descripcion']} — {equipo['estado']}" if equipo else "Código no registrado"
        self.lbl_equipo.configure(text=texto)
        self.ent_matricula.focus_set()

    def prestar(self):
        codigo, matricula = self.equipo.valor(), self.var_matricula.get().strip().upper()
        if not codigo or not matricula:
            aviso(self, "Escanee el equipo y capture la matrícula.")
            return
        if not self.var_dias.get().isdigit():
            aviso(self, "Los días deben ser un número.")
            return
        if not confirmar(self, f"¿Prestar {codigo} a {matricula} por {self.var_dias.get()} día(s)?"):
            return
        try:
            id_prestamo = prestamos.prestar(codigo, matricula, self.var_dias.get())
        except ErrorSistema as e:
            error(self, e)
            return
        info(self, f"Préstamo #{id_prestamo} registrado.")
        self.var_matricula.set("")
        self.lbl_equipo.configure(text="")
        self.mostrar()

    def devolver(self, codigo):
        if not confirmar(self, f"¿Registrar la devolución del equipo {codigo}?"):
            return
        try:
            dias_retraso = prestamos.devolver(codigo)
        except ErrorSistema as e:
            error(self, e)
            return
        info(self, f"Devolución registrada. Días de retraso: {dias_retraso}")
        self.devolucion.limpiar()
        self.mostrar()
