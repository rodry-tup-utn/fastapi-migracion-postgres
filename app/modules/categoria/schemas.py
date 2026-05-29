from sqlmodel import SQLModel


class CategoriaCreate(SQLModel):
    nombre: str
    descripcion: str | None = None


class CategoriaUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None


class ProductoBasicRead(SQLModel):
    id: int
    nombre: str
    precio: float
    stock: int
    stock_minimo: int


class CategoriaRead(SQLModel):
    nombre: str
    descripcion: str | None = None
    id: int
    activo: bool


class CategoriaFullRead(CategoriaRead):
    productos: list[ProductoBasicRead] = []
