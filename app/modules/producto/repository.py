from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.modules.producto.model import Producto


class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int, incluir_inactivos: bool = False) -> Producto | None:
        query = (
            select(Producto)
            .where(Producto.id == id)
            .options(selectinload(Producto.categoria))
        )
        if not incluir_inactivos:
            query = query.where(Producto.activo)
        return self.session.exec(query).first()

    def get_all(self, incluir_inactivos: bool = False) -> list[Producto]:
        query = select(Producto).options(selectinload(Producto.categoria))
        if not incluir_inactivos:
            query = query.where(Producto.activo)
        return list(self.session.exec(query).all())

    def create(self, producto: Producto) -> Producto:
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def save(self, producto: Producto) -> Producto:
        self.session.commit()
        self.session.refresh(producto)
        return producto
