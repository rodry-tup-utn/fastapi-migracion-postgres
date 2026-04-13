from sqlmodel import SQLModel, Field


class ProductoBase(SQLModel):
    nombre: str
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)


class ProductoCreate(ProductoBase):
    categoria_id: int


class ProductoUpdate(SQLModel):
    nombre: str | None = None
    categoria_id: int | None = None
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    activo: bool | None = None


class ProductoRead(ProductoBase):
    id: int
    categoria_id: int
    activo: bool


class CategoriaBasicRead(SQLModel):
    id: int
    nombre: str
    descripcion: str | None = None


class ProductoFullRead(ProductoRead):
    categoria: CategoriaBasicRead | None = None
