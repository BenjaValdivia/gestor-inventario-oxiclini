import customtkinter as ctk
from tkinter import ttk, messagebox
# Importamos el controlador, NO la base de datos directamente
from controllers.producto_controller import ProductoController

class FormularioProducto(ctk.CTkToplevel):
    def __init__(self, parent, callback_actualizar):
        super().__init__(parent)
        self.title("Nuevo Producto Maestro")
        self.geometry("400x450")
        self.resizable(False, False)
        
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self.callback_actualizar = callback_actualizar

        ctk.CTkLabel(self, text="Datos del Producto", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        frame_campos = ctk.CTkFrame(self, fg_color="transparent")
        frame_campos.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(frame_campos, text="Código (Ej: OX-10):", anchor="w").pack(fill="x")
        self.entrada_codigo = ctk.CTkEntry(frame_campos, placeholder_text="Ingrese código único")
        self.entrada_codigo.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(frame_campos, text="Descripción del Producto:", anchor="w").pack(fill="x")
        self.entrada_nombre = ctk.CTkEntry(frame_campos, placeholder_text="Ej: Oxígeno Industrial 10m3")
        self.entrada_nombre.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(frame_campos, text="Categoría:", anchor="w").pack(fill="x")
        self.entrada_categoria = ctk.CTkComboBox(frame_campos, values=["Cilindro", "Insumo"])
        self.entrada_categoria.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(frame_campos, text="Precio Base (CLP):", anchor="w").pack(fill="x")
        self.entrada_precio = ctk.CTkEntry(frame_campos, placeholder_text="Ej: 25000")
        self.entrada_precio.pack(fill="x", pady=(0, 20))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))

        btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", command=self.procesar_guardado, fg_color="#1f538d")
        btn_guardar.pack(side="left", expand=True, padx=(0, 5))

        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy, fg_color="#d43b3b", hover_color="#a82d2d")
        btn_cancelar.pack(side="right", expand=True, padx=(5, 0))

    def procesar_guardado(self):
        """Captura los datos visuales y se los manda al Controlador."""
        codigo = self.entrada_codigo.get().strip().upper()
        nombre = self.entrada_nombre.get().strip()
        categoria = self.entrada_categoria.get()
        precio = self.entrada_precio.get().strip()

        # Llamamos al controlador. Nos devolverá un booleano y un mensaje
        exito, mensaje = ProductoController.crear_producto(codigo, nombre, categoria, precio)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.callback_actualizar()
            self.destroy()
        else:
            messagebox.showerror("Error", mensaje)


class InventarioView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header_frame, text="Gestión de Inventario", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        btn_agregar = ctk.CTkButton(header_frame, text="+ Agregar Producto", command=self.abrir_formulario)
        btn_agregar.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam") 
        
        style.configure("Treeview", background="#FFFFFF", foreground="#000000", rowheight=25, fieldbackground="#FFFFFF", bordercolor="#D4D4D4", borderwidth=1)
        style.map('Treeview', background=[('selected', '#C6E2FF')], foreground=[('selected', '#000000')])
        style.configure("Treeview.Heading", background="#F0F0F0", foreground="#000000", bordercolor="#A0A0A0", borderwidth=1, relief="solid", font=("Arial", 10, "bold"))
        style.map("Treeview.Heading", background=[('active', '#E0E0E0')])

        columnas = ("codigo", "nombre", "categoria", "precio")
        self.tabla_productos = ttk.Treeview(self, columns=columnas, show="headings", style="Treeview")

        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Descripción")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio Base")

        self.tabla_productos.column("codigo", width=100, anchor="center")
        self.tabla_productos.column("nombre", width=300, anchor="w")
        self.tabla_productos.column("categoria", width=150, anchor="center")
        self.tabla_productos.column("precio", width=100, anchor="e")

        self.tabla_productos.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tabla_productos.tag_configure("impar", background="#F9F9F9")
        self.tabla_productos.tag_configure("par", background="#FFFFFF")

        self.cargar_datos()

    def abrir_formulario(self):
        FormularioProducto(self, self.cargar_datos)

    def cargar_datos(self):
        """Actualiza la tabla pidiéndole los datos al Controlador."""
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        # El controlador nos entrega una lista limpia de diccionarios
        productos = ProductoController.obtener_todos()
        
        for i, prod in enumerate(productos):
            tag = "par" if i % 2 == 0 else "impar"
            precio_formateado = f"$ {prod['precio_base']:,.0f}".replace(",", ".")

            self.tabla_productos.insert("", "end", values=(
                prod["codigo"],
                prod["nombre"],
                prod["categoria"],
                precio_formateado
            ), tags=(tag,))