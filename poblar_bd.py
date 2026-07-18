from database.connection import SessionLocal

from database.models import Producto

db = SessionLocal()

# Creamos unos productos reales para probar
productos_prueba = [
    Producto(codigo="OX-10", nombre="Oxígeno Industrial 10m3", categoria="Cilindro", precio_base=25000),
    Producto(codigo="ARG-05", nombre="Argón 5m3", categoria="Cilindro", precio_base=30000),
    Producto(codigo="MAN-01", nombre="Manguera Alta Presión 5m", categoria="Insumo", precio_base=15000)
]

# Los añadimos y guardamos (commit)
db.add_all(productos_prueba)
db.commit()
db.close()

print("¡Productos guardados exitosamente en SQLite!")