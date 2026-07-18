import customtkinter as ctk
# Importamos nuestra nueva vista modular
from gui.views.inventario_view import InventarioView
from gui.views.clientes_view import ClientesView

ctk.set_appearance_mode("Light")  # Forzamos modo claro para que combine con el estilo corporativo
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestor Inventario OxiClini")
        self.geometry("1000x600")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_sidebar()
        self.crear_pantallas()
        
        self.mostrar_pantalla("inventario")

    def crear_sidebar(self):
        # ... (Tu código anterior del sidebar se mantiene igual) ...
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OxiClini", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_movimientos = ctk.CTkButton(self.sidebar_frame, text="Movimientos", command=lambda: self.mostrar_pantalla("movimientos"))
        self.btn_movimientos.grid(row=1, column=0, padx=20, pady=10)

        self.btn_inventario = ctk.CTkButton(self.sidebar_frame, text="Inventario", command=lambda: self.mostrar_pantalla("inventario"))
        self.btn_inventario.grid(row=2, column=0, padx=20, pady=10)

        self.btn_clientes = ctk.CTkButton(self.sidebar_frame, text="Clientes", command=lambda: self.mostrar_pantalla("clientes"))
        self.btn_clientes.grid(row=3, column=0, padx=20, pady=10)

    def crear_pantallas(self):
        self.pantallas = {}

        # 1. PANTALLA INVENTARIO (Ahora viene de nuestro módulo externo)
        self.pantallas["inventario"] = InventarioView(self, corner_radius=0, fg_color="transparent")

        # 2. PANTALLA MOVIMIENTOS (Dummie temporal)
        frame_movimientos = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(frame_movimientos, text="Registro de Movimientos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20, padx=20, anchor="w")
        self.pantallas["movimientos"] = frame_movimientos

        # 3. PANTALLA CLIENTES (Dummie temporal)
        frame_clientes = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(frame_clientes, text="Directorio de Clientes y Precios", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20, padx=20, anchor="w")
        self.pantallas["clientes"] = ClientesView(self, corner_radius=0, fg_color="transparent")

    def mostrar_pantalla(self, nombre_pantalla):
        for frame in self.pantallas.values():
            frame.grid_forget()

        frame_actual = self.pantallas[nombre_pantalla]
        frame_actual.grid(row=0, column=1, sticky="nsew")