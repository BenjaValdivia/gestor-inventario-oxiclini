from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

# ==========================================
# 1. CATÁLOGO Y CLIENTES
# ==========================================

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    direccion = Column(String)
    
    # Relaciones para acceder fácilmente desde el código
    precios_especiales = relationship("PrecioPersonalizado", back_populates="cliente")
    movimientos = relationship("Movimiento", back_populates="cliente")
    cilindros_en_poder = relationship("Cilindro", back_populates="cliente_actual")

class Producto(Base):
    """
    Catálogo maestro. Aquí va "Oxígeno 10m3", "Manguera 5m", etc.
    """
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True) # Ej: OX-10
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)       # 'Cilindro' o 'Insumo'
    precio_base = Column(Float, nullable=False)      # Precio por defecto
    stock_insumos = Column(Integer, default=0)       # Solo se usa si es un 'Insumo'
    
    # Relaciones
    cilindros_fisicos = relationship("Cilindro", back_populates="producto")

class PrecioPersonalizado(Base):
    """
    Resuelve la asignación manual de precios. Si un cliente no está aquí, 
    se le cobra el 'precio_base' de la tabla Producto.
    """
    __tablename__ = 'precios_personalizados'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    precio_acordado = Column(Float, nullable=False)
    
    cliente = relationship("Cliente", back_populates="precios_especiales")
    producto = relationship("Producto")

# ==========================================
# 2. INVENTARIO FÍSICO Y TRAZABILIDAD
# ==========================================

class Cilindro(Base):
    """
    Control individual de cada envase. 
    """
    __tablename__ = 'cilindros'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, unique=True, index=True, nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    
    # Estados sugeridos: 'Disponible', 'En Cliente', 'En Planta', 'Mantenimiento'
    estado = Column(String, default="Disponible", nullable=False)
    
    # Saber quién lo tiene si está prestado
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True) 
    
    es_propiedad_cliente = Column(Boolean, default=False)
    
    producto = relationship("Producto", back_populates="cilindros_fisicos")
    cliente_actual = relationship("Cliente", back_populates="cilindros_en_poder")

# ==========================================
# 3. TRANSACCIONES Y FLUJO (El "Cuaderno")
# ==========================================

class Movimiento(Base):
    """
    Cabecera de la transacción. ¿Qué pasó hoy?
    """
    __tablename__ = 'movimientos'
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    # Tipos: 'Venta', 'Recepción Cliente', 'Envío Planta', 'Recepción Planta'
    tipo_movimiento = Column(String, nullable=False) 
    
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    observaciones = Column(String, nullable=True)
    
    cliente = relationship("Cliente", back_populates="movimientos")
    detalles = relationship("DetalleMovimiento", back_populates="movimiento")

class DetalleMovimiento(Base):
    """
    Lo que iba dentro del camión o lo que se llevó el cliente.
    """
    __tablename__ = 'detalles_movimiento'
    
    id = Column(Integer, primary_key=True)
    movimiento_id = Column(Integer, ForeignKey('movimientos.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    
    # Puede ser nulo si el movimiento es de un insumo (que no tiene N° de serie)
    cilindro_id = Column(Integer, ForeignKey('cilindros.id'), nullable=True)
    
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Float, nullable=False) # El precio que se cobró en ese momento exacto
    
    movimiento = relationship("Movimiento", back_populates="detalles")
    producto = relationship("Producto")
    cilindro = relationship("Cilindro")