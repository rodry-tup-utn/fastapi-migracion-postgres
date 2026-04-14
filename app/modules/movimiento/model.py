from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.modules.producto.model import Producto


class TIPO_MOVIMIENTO(Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"


class Movimiento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo_movimiento: TIPO_MOVIMIENTO
    cantidad: int = Field(ge=1)
    descripcion: str | None = Field(default=None)
    precio_unitario: float = Field(ge=0)
    precio_total: float = Field(ge=0)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    producto_id: int = Field(foreign_key="producto.id")
    producto: "Producto" = Relationship(back_populates="movimientos")
    activo: bool = True
