from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.categoria.model import Categoria
    from app.modules.movimiento.model import Movimiento


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    categoria_id: int = Field(foreign_key="categoria.id")
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    activo: bool = True

    categoria: "Categoria" = Relationship(back_populates="productos")
    movimientos: "Movimiento" = Relationship(back_populates="producto")
