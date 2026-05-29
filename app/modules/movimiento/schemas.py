from sqlmodel import SQLModel, Field
from app.modules.movimiento.model import TIPO_MOVIMIENTO
from datetime import datetime


class MovimientoCreate(SQLModel):
    tipo_movimiento: TIPO_MOVIMIENTO
    cantidad: int = Field(ge=1)
    descripcion: str | None = None
    precio_unitario: float | None = None
    producto_id: int


class MovimientoRead(SQLModel):
    tipo_movimiento: TIPO_MOVIMIENTO
    cantidad: int = Field(ge=1)
    descripcion: str | None = None
    precio_unitario: float | None = None
    id: int
    fecha: datetime
    producto_id: int
    activo: bool


class ProductoBaseRead(SQLModel):
    id: int
    nombre: str


class MovimientoFullRead(MovimientoRead):
    producto: ProductoBaseRead


class DashboardStats(SQLModel):
    total_compras_count: int
    total_ventas_count: int
    monto_total_ventas: float
    monto_total_compras: float
    balance_caja: float
    varidad_productos: int
    stock_total_actual: int
