import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController
from controllers.producto_controller import ProductoController # Necesitamos los productos para el menú desplegable

# ... (Aquí se mantiene la clase FormularioCliente igual que antes, 
# pégala aquí o déjala como estaba en tu archivo original) ...
class FormularioCliente(ctk.CTkToplevel):
    # (Mismo código de FormularioCliente del paso anterior)
    def __init__(self, parent, callback_actualizar):
        super().__init__(parent)
        self.title("Nuevo Cliente")
        self.geometry("400x450")
        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self.callback_actualizar = callback_actualizar
        ctk.CTkLabel(self, text="Datos del Cliente", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        frame_campos = ctk.CTkFrame(self, fg_color="transparent")
        frame_campos.pack(fill="both", expand=True, padx=30, pady=10)
        ctk.CTkLabel(frame_campos, text="RUT (Opcional):", anchor="w").pack(fill="x")
        self.entrada_rut = ctk.CTkEntry(frame_campos)
        self.entrada_rut.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(frame_campos, text="Nombre / Razón Social (*):", anchor="w").pack(fill="x")
        self.entrada_nombre = ctk.CTkEntry(frame_campos)
        self.entrada_nombre.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(frame_campos, text="Teléfono:", anchor="w").pack(fill="x")
        self.entrada_telefono = ctk.CTkEntry(frame_campos)
        self.entrada_telefono.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(frame_campos, text="Dirección:", anchor="w").pack(fill="x")
        self.entrada_direccion = ctk.CTkEntry(frame_campos)
        self.entrada_direccion.pack(fill="x", pady=(0, 20))
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))
        btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", command=self.procesar_guardado, fg_color="#1f538d")
        btn_guardar.pack(side="left", expand=True, padx=(0, 5))
        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy, fg_color="#d43b3b", hover_color="#a82d2d")
        btn_cancelar.pack(side="right", expand=True, padx=(5, 0))

    def procesar_guardado(self):
        exito, msj = ClienteController.crear_cliente(self.entrada_rut.get(), self.entrada_nombre.get(), self.entrada_telefono.get(), self.entrada_direccion.get())
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.callback_actualizar()
            self.destroy()
        else:
            messagebox.showerror("Error", msj)

# ==========================================
# NUEVA CLASE: LA FICHA DEL CLIENTE
# ==========================================
class FichaCliente(ctk.CTkToplevel):
    def __init__(self, parent, cliente_id, cliente_nombre):
        super().__init__(parent)
        self.title(f"Ficha Cliente: {cliente_nombre}")
        self.geometry("700x500") # Más ancha para ver la tabla
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self.cliente_id = cliente_id
        
        # Título principal
        ctk.CTkLabel(self, text=f"Ficha de Cobranza: {cliente_nombre}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15, padx=20, anchor="w")

        # --- Zona Superior: Asignar Nuevo Precio ---
        frame_asignar = ctk.CTkFrame(self)
        frame_asignar.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_asignar, text="Asignar Precio Especial:").pack(side="left", padx=10, pady=10)
        
        # Cargar productos en el combobox formateados como "CODIGO | Nombre"
        productos = ProductoController.obtener_todos()
        lista_prods = [f"{p['codigo']} | {p['nombre']}" for p in productos]
        
        self.combo_productos = ctk.CTkComboBox(frame_asignar, values=lista_prods, width=250)
        self.combo_productos.pack(side="left", padx=10)
        
        self.entrada_precio = ctk.CTkEntry(frame_asignar, placeholder_text="Nuevo Precio ($)", width=120)
        self.entrada_precio.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_asignar, text="Guardar Precio", command=self.guardar_precio).pack(side="left", padx=10)

        # --- Zona Inferior: Tabla de Precios del Cliente ---
        columnas = ("codigo", "producto", "precio_base", "precio_acordado")
        self.tabla_precios = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        
        self.tabla_precios.heading("codigo", text="Cód.")
        self.tabla_precios.heading("producto", text="Producto")
        self.tabla_precios.heading("precio_base", text="Precio Base")
        self.tabla_precios.heading("precio_acordado", text="Precio Acordado")

        self.tabla_precios.column("codigo", width=80, anchor="center")
        self.tabla_precios.column("producto", width=250, anchor="w")
        self.tabla_precios.column("precio_base", width=100, anchor="e")
        self.tabla_precios.column("precio_acordado", width=120, anchor="e")

        self.tabla_precios.pack(fill="both", expand=True, padx=20, pady=20)
        self.cargar_precios_cliente()

    def guardar_precio(self):
        seleccion = self.combo_productos.get()
        precio = self.entrada_precio.get().strip()
        
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
            
        # Extraer solo el código (ej: de "OX-10 | Oxígeno" sacamos "OX-10")
        codigo_prod = seleccion.split(" | ")[0]
        
        exito, msj = ClienteController.guardar_precio_especial(self.cliente_id, codigo_prod, precio)
        if exito:
            self.entrada_precio.delete(0, "end")
            self.cargar_precios_cliente() # Refresca la tablita
        else:
            messagebox.showerror("Error", msj)

    def cargar_precios_cliente(self):
        for item in self.tabla_precios.get_children():
            self.tabla_precios.delete(item)
            
        precios = ClienteController.obtener_precios_cliente(self.cliente_id)
        for p in precios:
            base_fmt = f"$ {p['precio_base']:,.0f}".replace(",", ".")
            acordado_fmt = f"$ {p['precio_acordado']:,.0f}".replace(",", ".")
            self.tabla_precios.insert("", "end", values=(p["codigo"], p["producto"], base_fmt, acordado_fmt))


# ==========================================
# DIRECTORIO PRINCIPAL
# ==========================================
class ClientesView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header_frame, text="Directorio de Clientes", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="(Doble clic en un cliente para ver precios)", text_color="gray").pack(side="left", padx=15)
        ctk.CTkButton(header_frame, text="+ Agregar Cliente", command=self.abrir_formulario).pack(side="right")

        # --- Tabla con ID Oculto ---
        # Definimos 'id' en columnas, pero usamos displaycolumns para NO mostrarlo en pantalla
        columnas = ("id", "rut", "nombre", "telefono", "direccion")
        self.tabla_clientes = ttk.Treeview(self, columns=columnas, show="headings", displaycolumns=("rut", "nombre", "telefono", "direccion"))

        self.tabla_clientes.heading("rut", text="RUT")
        self.tabla_clientes.heading("nombre", text="Nombre / Razón Social")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("direccion", text="Dirección")

        self.tabla_clientes.column("rut", width=120, anchor="center")
        self.tabla_clientes.column("nombre", width=300, anchor="w")
        self.tabla_clientes.column("telefono", width=120, anchor="center")
        self.tabla_clientes.column("direccion", width=250, anchor="w")

        self.tabla_clientes.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.cargar_datos()

        # EVENTO ESTRELLA: Doble Clic
        self.tabla_clientes.bind("<Double-1>", self.abrir_ficha_cliente)

    def abrir_formulario(self):
        FormularioCliente(self, self.cargar_datos)

    def abrir_ficha_cliente(self, event):
        """Captura la fila seleccionada y abre su ficha."""
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            return
            
        # Obtenemos los valores de la fila
        item = self.tabla_clientes.item(seleccion[0])
        valores = item['values']
        
        # valores[0] es el ID oculto, valores[2] es el nombre
        cliente_id = valores[0]
        cliente_nombre = valores[2]
        
        FichaCliente(self, cliente_id, cliente_nombre)

    def cargar_datos(self):
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)

        clientes = ClienteController.obtener_todos()
        for i, cli in enumerate(clientes):
            tag = "par" if i % 2 == 0 else "impar"
            # Insertamos el ID en la posición 0, aunque no se vea en pantalla
            self.tabla_clientes.insert("", "end", values=(cli["id"], cli["rut"], cli["nombre"], cli["telefono"], cli["direccion"]), tags=(tag,))