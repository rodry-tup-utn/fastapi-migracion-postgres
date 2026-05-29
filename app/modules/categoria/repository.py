from sqlmodel import Session, select
from app.modules.categoria.model import Categoria


class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int, incluir_inactivos: bool = False) -> Categoria | None:
        query = select(Categoria).where(Categoria.id == id)
        if not incluir_inactivos:
            query = query.where(Categoria.activo)
        return self.session.exec(query).first()

    def get_all(self, incluir_inactivos: bool = False) -> list[Categoria]:
        query = select(Categoria)
        if not incluir_inactivos:
            query = query.where(Categoria.activo)
        return list(self.session.exec(query).all())

    def create(self, categoria: Categoria) -> Categoria:
        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def save(self, categoria: Categoria) -> Categoria:
        self.session.commit()
        self.session.refresh(categoria)
        return categoria
