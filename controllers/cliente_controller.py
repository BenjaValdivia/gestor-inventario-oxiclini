from database.connection import SessionLocal
from database.models import Cliente
from database.models import Cliente, PrecioPersonalizado, Producto

class ClienteController:
    @staticmethod
    def obtener_todos():
        """Obtiene la lista de clientes como diccionarios."""
        db = SessionLocal()
        try:
            clientes = db.query(Cliente).all()
            resultado = []
            for c in clientes:
                resultado.append({
                    "id": c.id,
                    "rut": c.rut if c.rut else "S/N",
                    "nombre": c.nombre,
                    "telefono": c.telefono if c.telefono else "No registrado",
                    "direccion": c.direccion if c.direccion else "No registrada"
                })
            return resultado
        finally:
            db.close()

    @staticmethod
    def crear_cliente(rut, nombre, telefono, direccion):
        """Valida e inserta un nuevo cliente en la BD."""
        if not nombre:
            return False, "El nombre del cliente es obligatorio."

        db = SessionLocal()
        try:
            # Validar RUT duplicado solo si el usuario escribió algo
            if rut:
                existe = db.query(Cliente).filter(Cliente.rut == rut).first()
                if existe:
                    return False, f"El RUT '{rut}' ya está registrado en el sistema."

            nuevo_cliente = Cliente(
                rut=rut,
                nombre=nombre,
                telefono=telefono,
                direccion=direccion
            )
            db.add(nuevo_cliente)
            db.commit()
            return True, "Cliente guardado correctamente."

        except Exception as e:
            db.rollback()
            return False, f"Error de Base de Datos: {str(e)}"
        finally:
            db.close()

    @staticmethod
    def obtener_precios_cliente(cliente_id):
        """Devuelve los precios personalizados de un cliente específico."""
        db = SessionLocal()
        try:
            # Hacemos un JOIN para traer el nombre del producto y su precio base
            precios = db.query(PrecioPersonalizado, Producto).join(
                Producto, PrecioPersonalizado.producto_id == Producto.id
            ).filter(PrecioPersonalizado.cliente_id == cliente_id).all()
            
            resultado = []
            for precio, prod in precios:
                resultado.append({
                    "codigo": prod.codigo,
                    "producto": prod.nombre,
                    "precio_base": prod.precio_base,
                    "precio_acordado": precio.precio_acordado
                })
            return resultado
        finally:
            db.close()

    @staticmethod
    def guardar_precio_especial(cliente_id, codigo_producto, precio_nuevo):
        """Asigna o actualiza un precio especial para el cliente."""
        if not precio_nuevo or not codigo_producto:
            return False, "Debe seleccionar un producto e ingresar un precio."
            
        try:
            precio_float = float(precio_nuevo)
        except ValueError:
            return False, "El precio debe ser un número válido."

        db = SessionLocal()
        try:
            producto = db.query(Producto).filter(Producto.codigo == codigo_producto).first()
            if not producto:
                return False, "Producto no encontrado."

            # Buscar si el cliente ya tenía un precio para este producto
            precio_exist = db.query(PrecioPersonalizado).filter_by(
                cliente_id=cliente_id, producto_id=producto.id
            ).first()
            
            if precio_exist:
                precio_exist.precio_acordado = precio_float # Actualiza
            else:
                nuevo = PrecioPersonalizado(
                    cliente_id=cliente_id, 
                    producto_id=producto.id, 
                    precio_acordado=precio_float
                )
                db.add(nuevo) # Crea uno nuevo
            
            db.commit()
            return True, "Precio asignado correctamente."
        except Exception as e:
            db.rollback()
            return False, f"Error BD: {str(e)}"
        finally:
            db.close()