from sqlmodel import SQLModel


class CategoriaBase(SQLModel):
    nombre: str
    descripcion: str | None = None


class CategoriaCreate(CategoriaBase):
    pass


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


class CategoriaFullRead(CategoriaBase):
    id: int
    activo: bool
    productos: list[ProductoBasicRead] = []


class CategoriaBaseRead(CategoriaBase):
    id: int
    activo: bool
