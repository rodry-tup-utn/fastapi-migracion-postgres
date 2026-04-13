from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.producto.model import Producto


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: str | None = Field(default=None)
    activo: bool = True
    productos: list["Producto"] = Relationship(back_populates="categoria")
