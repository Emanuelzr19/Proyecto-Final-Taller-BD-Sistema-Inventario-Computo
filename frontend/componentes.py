import datetime
import tkinter as tk
from tkinter import messagebox, ttk

TITULO = ("Segoe UI", 16, "bold")
SUBTITULO = ("Segoe UI", 11, "bold")


class EntradaCodigo(ttk.Frame):

    def __init__(self, master, texto, al_leer):
        super().__init__(master)
        self.al_leer = al_leer
        self.var = tk.StringVar()
        ttk.Label(self, text=texto).pack(side="left", padx=(0, 6))
        self.entrada = ttk.Entry(self, textvariable=self.var, width=20, font=("Consolas", 14))
        self.entrada.pack(side="left")
        ttk.Button(self, text="Aceptar", command=self._leer).pack(side="left", padx=6)
        self.entrada.bind("<Return>", self._leer)

    def _leer(self, _evento=None):
        codigo = self.var.get().strip().upper()
        self.var.set(codigo)
        if codigo:
            self.al_leer(codigo)
        self.entrada.select_range(0, "end")

    def valor(self):
        return self.var.get().strip().upper()

    def limpiar(self):
        self.var.set("")
        self.entrada.focus_set()


class Tabla(ttk.Frame):

    def __init__(self, master, columnas, alto=10):
        super().__init__(master)
        self.columnas = columnas
        self.filas = []
        self.arbol = ttk.Treeview(self, columns=[c[0] for c in columnas], show="headings", height=alto)
        for clave, titulo, ancho in columnas:
            self.arbol.heading(clave, text=titulo)
            self.arbol.column(clave, width=ancho)
        barra = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra.set)
        self.arbol.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.arbol.tag_configure("alerta", background="#f8d7da")

    def cargar(self, filas, alerta=None):
        self.arbol.delete(*self.arbol.get_children())
        self.filas = filas
        for i, fila in enumerate(filas):
            valores = [formatear(fila.get(c[0])) for c in self.columnas]
            tags = ("alerta",) if alerta and alerta(fila) else ()
            self.arbol.insert("", "end", iid=str(i), values=valores, tags=tags)

    def seleccion(self):
        sel = self.arbol.selection()
        return self.filas[int(sel[0])] if sel else None


def formatear(valor):
    if valor is None:
        return ""
    if isinstance(valor, datetime.datetime):
        return valor.strftime("%d/%m/%Y %H:%M")
    return str(valor)


def error(padre, e):
    messagebox.showerror("Error", str(e), parent=padre)


def aviso(padre, texto):
    messagebox.showwarning("Atención", texto, parent=padre)


def info(padre, texto):
    messagebox.showinfo("Operación realizada", texto, parent=padre)


def confirmar(padre, texto):
    return messagebox.askyesno("Confirmar", texto, parent=padre)


def pedir_datos(padre, titulo, campos, valores=None):
    valores = valores or {}
    ventana = tk.Toplevel(padre)
    ventana.title(titulo)
    ventana.resizable(False, False)
    ventana.transient(padre)
    marco = ttk.Frame(ventana, padding=15)
    marco.pack()
    variables = {}
    for i, (clave, etiqueta, opciones) in enumerate(campos):
        ttk.Label(marco, text=etiqueta).grid(row=i, column=0, sticky="e", padx=5, pady=4)
        variables[clave] = tk.StringVar(value=formatear(valores.get(clave)))
        if opciones is None:
            widget = ttk.Entry(marco, textvariable=variables[clave], width=36)
        else:
            widget = ttk.Combobox(marco, textvariable=variables[clave], values=opciones,
                                  state="readonly", width=34)
        widget.grid(row=i, column=1, sticky="w", pady=4)
    resultado = {}

    def aceptar():
        for clave, etiqueta, _ in campos:
            if not variables[clave].get().strip():
                aviso(ventana, f"Capture: {etiqueta}")
                return
        resultado.update({clave: var.get().strip() for clave, var in variables.items()})
        ventana.destroy()

    botones = ttk.Frame(marco)
    botones.grid(row=len(campos), column=0, columnspan=2, pady=(10, 0))
    ttk.Button(botones, text="Guardar", command=aceptar).pack(side="left", padx=5)
    ttk.Button(botones, text="Cancelar", command=ventana.destroy).pack(side="left", padx=5)
    ventana.wait_visibility()
    ventana.grab_set()
    ventana.wait_window()
    return resultado or None
