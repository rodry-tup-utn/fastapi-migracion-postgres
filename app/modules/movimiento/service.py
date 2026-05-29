from sqlmodel import Session
from app.modules.movimiento.model import Movimiento, TIPO_MOVIMIENTO
from app.core.errors import NotFoundException
from app.modules.movimiento import schemas
from app.modules.movimiento.repository import MovimientoRepository
from app.modules.producto.service import ProductoService


class MovimientoService:
    def __init__(self, session: Session):
        self.repo = MovimientoRepository(session)
        self.producto_service = ProductoService(session)

    def create(self, data: schemas.MovimientoCreate) -> Movimiento:
        factor = -1 if data.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA else 1

        producto = self.producto_service.update_stock(
            data.producto_id, data.cantidad * factor
        )

        if data.precio_unitario is None:
            data.precio_unitario = producto.precio

        precio_total = data.cantidad * data.precio_unitario

        movimiento_data = data.model_dump()
        movimiento_data["precio_total"] = precio_total

        movimiento = Movimiento.model_validate(movimiento_data)

        return self.repo.create(movimiento)

    def get_all(self, incluir_inactivos: bool = False) -> list[Movimiento]:
        return self.repo.get_all(incluir_inactivos)

    def get_by_id(self, id: int, incluir_inactivos: bool = False) -> Movimiento:
        movimiento = self.repo.get_by_id(id, incluir_inactivos)
        if not movimiento:
            raise NotFoundException(f"No se encontro movimiento con el id {id}")
        return movimiento

    def delete(self, id: int) -> Movimiento:
        movimiento = self.repo.get_by_id(id)
        if not movimiento:
            raise NotFoundException(f"No se encontro movimiento con el id {id}")

        factor = 1 if movimiento.tipo_movimiento == TIPO_MOVIMIENTO.SALIDA else -1

        self.producto_service.update_stock(
            movimiento.producto_id, movimiento.cantidad * factor
        )
        movimiento.activo = False

        return self.repo.save(movimiento)

    def get_dashboard_stats(self) -> schemas.DashboardStats:
        return self.repo.get_dashboard_stats()
