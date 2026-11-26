import tkinter as tk
from tkinter import ttk

from backend import seguridad
from backend.conexion import ErrorSistema
from frontend.componentes import TITULO, confirmar, error
from frontend.pantalla_asignaciones import PantallaAsignaciones
from frontend.pantalla_equipos import PantallaEquipos
from frontend.pantalla_prestamos import PantallaPrestamos
from frontend.pantalla_reportes import PantallaReportes
from frontend.pantalla_solicitantes import PantallaSolicitantes

MENU = [("Equipos", PantallaEquipos), ("Préstamos y devoluciones", PantallaPrestamos),
        ("Asignaciones", PantallaAsignaciones), ("Alumnos y docentes", PantallaSolicitantes),
        ("Reportes", PantallaReportes)]


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario de Equipo de Cómputo")
        self.geometry("1150x720")
        ttk.Style(self).theme_use("clam")
        self.contenido = None
        self.mostrar_login()

    def cambiar_contenido(self, nuevo):
        if self.contenido is not None:
            self.contenido.destroy()
        self.contenido = nuevo
        nuevo.pack(fill="both", expand=True)

    def mostrar_login(self):
        marco = ttk.Frame(self)
        caja = ttk.Frame(marco, padding=30)
        caja.place(relx=0.5, rely=0.4, anchor="center")
        ttk.Label(caja, text="Inventario de Equipo de Cómputo", font=TITULO).pack(pady=(0, 20))
        ttk.Label(caja, text="Usuario").pack(anchor="w")
        usuario = ttk.Entry(caja, width=30)
        usuario.pack(pady=(0, 10))
        ttk.Label(caja, text="Contraseña").pack(anchor="w")
        password = ttk.Entry(caja, width=30, show="*")
        password.pack(pady=(0, 15))

        def entrar(_evento=None):
            try:
                seguridad.iniciar_sesion(usuario.get(), password.get())
            except ErrorSistema as e:
                error(self, e)
                password.delete(0, "end")
                return
            self.mostrar_menu()

        ttk.Button(caja, text="Iniciar sesión", command=entrar).pack(fill="x")
        password.bind("<Return>", entrar)
        usuario.focus_set()
        self.cambiar_contenido(marco)

    def mostrar_menu(self):
        marco = ttk.Frame(self)
        menu = ttk.Frame(marco, padding=10, relief="groove")
        menu.pack(side="left", fill="y")
        usuario = seguridad.usuario_actual
        ttk.Label(menu, text=usuario["nombre_completo"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(menu, text=f"Rol: {usuario['rol']}").pack(anchor="w", pady=(0, 15))
        area = ttk.Frame(marco)
        area.pack(side="left", fill="both", expand=True)
        pantallas = {}

        def abrir(clase):
            for pantalla in pantallas.values():
                pantalla.pack_forget()
            if clase not in pantallas:
                pantallas[clase] = clase(area)
            pantallas[clase].pack(fill="both", expand=True)
            pantallas[clase].mostrar()

        for texto, clase in MENU:
            ttk.Button(menu, text=texto, width=26, command=lambda c=clase: abrir(c)).pack(pady=3)
        ttk.Button(menu, text="Cerrar sesión", width=26, command=self.cerrar_sesion).pack(side="bottom")
        self.cambiar_contenido(marco)
        abrir(PantallaEquipos)

    def cerrar_sesion(self):
        if confirmar(self, "¿Desea cerrar la sesión?"):
            try:
                seguridad.cerrar_sesion()
            except ErrorSistema:
                pass
            self.mostrar_login()
