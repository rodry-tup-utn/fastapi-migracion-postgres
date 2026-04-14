from app.modules.movimiento.model import Movimiento, TIPO_MOVIMIENTO
from app.core.errors import NotFoundException
from sqlmodel import Session, select, desc
from app.modules.movimiento import schemas
from app.modules.producto import service as service_producto
from sqlalchemy.orm import selectinload


def create_movimiento(session: Session, data: schemas.MovimientoCreate):
    factor = -1 if data.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA else 1

    producto = service_producto.update_stock(
        session, data.producto_id, data.cantidad * factor
    )

    if data.precio_unitario is None:
        data.precio_unitario = producto.precio

    precio_total = data.cantidad * data.precio_unitario

    movimiento_data = data.model_dump()
    movimiento_data["precio_total"] = precio_total

    movimiento = Movimiento.model_validate(movimiento_data)

    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)

    return movimiento


def get_all(session: Session, incluir_inactivos: bool = False):
    query = select(Movimiento).order_by(desc(Movimiento.fecha))

    if not incluir_inactivos:
        query = query.where(Movimiento.activo)

    return session.exec(query).all()


def get_by_id(session: Session, id: int, incluir_inactivos: bool = False):
    query = (
        select(Movimiento)
        .where(Movimiento.id == id)
        .options(selectinload(Movimiento.producto))  # type:ignore
    )

    if not incluir_inactivos:
        query = query.where(Movimiento.activo)

    movimiento = session.exec(query).first()

    if not movimiento:
        raise NotFoundException(f"No se encontro movimiento con el id {id}")

    return movimiento


def delete(session: Session, id: int):
    movimiento = get_by_id(session, id)

    factor = 1 if movimiento.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA else -1

    service_producto.update_stock(
        session, movimiento.producto_id, movimiento.cantidad * factor
    )
    movimiento.activo = False

    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)

    return movimiento
