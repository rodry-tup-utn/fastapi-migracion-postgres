from app.modules.producto.schemas import ProductoCreate, ProductoUpdate
from app.modules.producto.model import Producto
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload


def create_producto(session: Session, data: ProductoCreate):
    producto = Producto.model_validate(data)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def get_productos(session: Session, incluir_inactivos: bool = False):
    query = select(Producto).options(selectinload(Producto.categoria))  # type:ignore

    if not incluir_inactivos:
        query = query.where(Producto.activo)

    return list(session.exec(query).all())


def get_producto(
    session: Session, producto_id: int, incluir_inactivos: bool = False
) -> Producto:
    query = (
        select(Producto)
        .where(Producto.id == producto_id)
        .options(selectinload(Producto.categoria))  # type:ignore
    )

    if not incluir_inactivos:
        query = query.where(Producto.activo)

    producto = session.exec(query).first()

    if not producto:
        raise LookupError(f"No se encontró producto con el id {producto_id}")

    return producto


def delete_producto(session: Session, producto_id: int):
    producto = get_producto(session, producto_id)

    producto.activo = False

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def update_producto(session: Session, producto_id: int, data: ProductoUpdate):
    # solo se permite modificar productos activos
    producto = get_producto(session, producto_id)

    data_dict = data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in data_dict.items():
        setattr(producto, key, value)

    session.commit()
    session.refresh(producto)

    return producto
