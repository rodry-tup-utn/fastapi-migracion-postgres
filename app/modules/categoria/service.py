from sqlmodel import Session, select
from app.modules.categoria.schemas import (
    CategoriaCreate,
    CategoriaUpdate,
)
from app.modules.categoria.model import Categoria
from app.core.errors import NotFoundException


def create_categoria(session: Session, data: CategoriaCreate):
    categoria = Categoria.model_validate(data)

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


def get_categorias(session: Session, incluir_inactivos: bool = False):
    query = select(Categoria)

    if not incluir_inactivos:
        query = query.where(Categoria.activo)

    return session.exec(query).all()


def get_categoria(session: Session, categoria_id: int, incluir_inactivos: bool = False):
    query = select(Categoria).where(Categoria.id == categoria_id)

    if not incluir_inactivos:
        query = query.where(Categoria.activo)

    categoria = session.exec(query).first()

    if not categoria:
        raise NotFoundException(
            f"No se encontro una categoria con el id {categoria_id}"
        )

    return categoria


def eliminar_categoria(session: Session, categoria_id: int):
    categoria = get_categoria(session, categoria_id)

    categoria.activo = False

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def update_categoria(session: Session, categoria_id: int, data: CategoriaUpdate):
    categoria = get_categoria(session, categoria_id)

    data_dict = data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in data_dict.items():
        setattr(categoria, key, value)

    session.commit()
    session.refresh(categoria)

    return categoria


def delete_categoria(session: Session, categoria_id: int):
    categoria = get_categoria(session, categoria_id)
    categoria.activo = False
    session.commit()
    session.refresh(categoria)

    return categoria
