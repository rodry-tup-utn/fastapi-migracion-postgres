from sqlmodel import SQLModel, Field
from app.modules.movimiento.model import TIPO_MOVIMIENTO
from datetime import datetime


class MovimientoBase(SQLModel):
    tipo_movimiento: TIPO_MOVIMIENTO
    cantidad: int = Field(ge=1)
    descripcion: str | None = None
    precio_unitario: float | None = None
    precio_total: float | None = None


class MovimientoCreate(MovimientoBase):
    producto_id: int


class MovimientoRead(MovimientoBase):
    id: int
    fecha: datetime
    producto_id: int
    activo: bool


class ProductoBaseRead(SQLModel):
    id: int
    nombre: str


class MovimientoFullRead(MovimientoRead):
    producto: ProductoBaseRead
