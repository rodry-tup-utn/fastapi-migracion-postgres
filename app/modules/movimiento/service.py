from app.modules.movimiento.model import Movimiento, TIPO_MOVIMIENTO
from app.core.errors import NotFoundException
from sqlmodel import Session, select, desc, col
from app.modules.movimiento import schemas
from app.modules.producto import service as service_producto
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.modules.producto.model import Producto


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


def get_dashboard_stats(session: Session) -> schemas.DashboardStats:

    # --- 1. ESTADÍSTICAS DE PRODUCTOS (1 sola query) ---
    # Contamos los IDs (variedad) y sumamos el stock actual
    query_productos = select(
        func.count(col(Producto.id)), func.coalesce(func.sum(Producto.stock), 0)
    ).where(Producto.activo)

    # .first() nos devuelve una tupla con los dos valores
    variedad_productos, stock_total = session.exec(
        query_productos
    ).first()  # type:ignore

    # --- 2. ESTADÍSTICAS DE COMPRAS / ENTRADAS (1 sola query) ---
    query_compras = select(
        func.count(col(Movimiento.id)),
        func.coalesce(func.sum(Movimiento.precio_total), 0.0),
    ).where(Movimiento.tipo_movimiento == TIPO_MOVIMIENTO.ENTRADA, Movimiento.activo)
    compras_count, compras_total = session.exec(query_compras).first()  # type:ignore

    # --- 3. ESTADÍSTICAS DE VENTAS / SALIDAS (1 sola query) ---
    query_ventas = select(
        func.count(col(Movimiento.id)),
        func.coalesce(func.sum(Movimiento.precio_total), 0.0),
    ).where(Movimiento.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA, Movimiento.activo)
    ventas_count, ventas_total = session.exec(query_ventas).first()  # type:ignore

    # --- 4. ARMADO DEL DASHBOARD ---
    # Calculamos el balance en memoria, que es una simple resta
    balance = ventas_total - compras_total

    return schemas.DashboardStats(
        total_compras_count=compras_count,
        total_ventas_count=ventas_count,
        monto_total_ventas=ventas_total,
        monto_total_compras=compras_total,
        balance_caja=balance,
        varidad_productos=variedad_productos,
        stock_total_actual=stock_total,
    )
