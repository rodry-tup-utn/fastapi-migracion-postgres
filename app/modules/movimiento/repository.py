from sqlmodel import Session, select, desc, col
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.modules.movimiento.model import Movimiento, TIPO_MOVIMIENTO
from app.modules.movimiento import schemas
from app.modules.producto.model import Producto


class MovimientoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int, incluir_inactivos: bool = False) -> Movimiento | None:
        query = (
            select(Movimiento)
            .where(Movimiento.id == id)
            .options(selectinload(Movimiento.producto))
        )
        if not incluir_inactivos:
            query = query.where(Movimiento.activo)
        return self.session.exec(query).first()

    def get_all(self, incluir_inactivos: bool = False) -> list[Movimiento]:
        query = select(Movimiento).order_by(desc(Movimiento.fecha))
        if not incluir_inactivos:
            query = query.where(Movimiento.activo)
        return list(self.session.exec(query).all())

    def create(self, movimiento: Movimiento) -> Movimiento:
        self.session.add(movimiento)
        self.session.commit()
        self.session.refresh(movimiento)
        return movimiento

    def save(self, movimiento: Movimiento) -> Movimiento:
        self.session.add(movimiento)
        self.session.commit()
        self.session.refresh(movimiento)
        return movimiento

    def get_dashboard_stats(self) -> schemas.DashboardStats:
        query_productos = select(
            func.count(col(Producto.id)), func.coalesce(func.sum(Producto.stock), 0)
        ).where(Producto.activo)
        variedad_productos, stock_total = self.session.exec(
            query_productos
        ).first()

        query_compras = select(
            func.count(col(Movimiento.id)),
            func.coalesce(func.sum(Movimiento.precio_total), 0.0),
        ).where(Movimiento.tipo_movimiento == TIPO_MOVIMIENTO.ENTRADA, Movimiento.activo)
        compras_count, compras_total = self.session.exec(query_compras).first()

        query_ventas = select(
            func.count(col(Movimiento.id)),
            func.coalesce(func.sum(Movimiento.precio_total), 0.0),
        ).where(Movimiento.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA, Movimiento.activo)
        ventas_count, ventas_total = self.session.exec(query_ventas).first()

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
