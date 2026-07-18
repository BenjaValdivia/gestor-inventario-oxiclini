from database.connection import SessionLocal
from database.models import Producto

class ProductoController:
    @staticmethod
    def obtener_todos():
        """Consulta los productos y los devuelve como una lista de diccionarios para no amarrar la BD a la vista."""
        db = SessionLocal()
        try:
            productos = db.query(Producto).all()
            # Convertimos a diccionario para evitar errores de "sesión cerrada" en la vista
            resultado = []
            for p in productos:
                resultado.append({
                    "codigo": p.codigo,
                    "nombre": p.nombre,
                    "categoria": p.categoria,
                    "precio_base": p.precio_base
                })
            return resultado
        finally:
            db.close()

    @staticmethod
    def crear_producto(codigo, nombre, categoria, precio):
        """Valida e inserta en la BD. Retorna (True/False, Mensaje)."""
        # Validaciones de negocio
        if not codigo or not nombre or not precio:
            return False, "Por favor, llene todos los campos."
        
        try:
            precio_float = float(precio)
        except ValueError:
            return False, "El precio debe ser un número válido (sin puntos ni letras)."

        db = SessionLocal()
        try:
            # Revisar si el código ya existe
            existe = db.query(Producto).filter(Producto.codigo == codigo).first()
            if existe:
                return False, f"El código '{codigo}' ya existe en el sistema."

            # Crear y guardar
            nuevo = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio_base=precio_float
            )
            db.add(nuevo)
            db.commit()
            return True, "Producto guardado correctamente."

        except Exception as e:
            db.rollback()
            return False, f"Error de Base de Datos: {str(e)}"
        finally:
            db.close()