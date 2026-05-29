from sqlmodel import Session
from app.modules.producto.schemas import ProductoCreate, ProductoUpdate, StockEstadoRead
from app.modules.producto.model import Producto
from app.modules.producto.repository import ProductoRepository
from app.modules.categoria.repository import CategoriaRepository
from app.core.errors import NotFoundException
from fastapi import HTTPException, status


class ProductoService:
    def __init__(self, session: Session):
        self.repo = ProductoRepository(session)
        self.categoria_repo = CategoriaRepository(session)

    def _get_or_404(self, producto_id: int, incluir_inactivos: bool = False):
        producto = self.repo.get_by_id(producto_id, incluir_inactivos)
        if not producto:
            raise NotFoundException(f"No se encontró producto con el id {producto_id}")
        return producto

    def create(self, data: ProductoCreate) -> Producto:
        producto = Producto.model_validate(data)
        return self.repo.create(producto)

    def get_all(self, incluir_inactivos: bool = False) -> list[Producto]:
        return self.repo.get_all(incluir_inactivos)

    def get_by_id(self, producto_id: int, incluir_inactivos: bool = False) -> Producto:
        producto = self._get_or_404(producto_id)
        return producto

    def delete(self, producto_id: int) -> Producto:
        producto = self._get_or_404(producto_id, True)

        if producto.activo == False:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "La categoria ya se encuentra eliminada"
            )

        producto.activo = False
        return self.repo.save(producto)

    def update(self, producto_id: int, data: ProductoUpdate) -> Producto:
        producto = self._get_or_404(producto_id)

        if data.categoria_id is not None:
            categoria = self.categoria_repo.get_by_id(data.categoria_id)
            if not categoria:
                raise NotFoundException(
                    f"No se encontro una categoria con el id {data.categoria_id}"
                )

        data_dict = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in data_dict.items():
            setattr(producto, key, value)

        return self.repo.save(producto)

    def obtener_estado_stock(self, producto_id: int) -> StockEstadoRead:
        producto = self._get_or_404(producto_id)

        alerta_stock = producto.stock < producto.stock_minimo
        return StockEstadoRead(
            stock=producto.stock,
            bajo_stock_minimo=alerta_stock,
            activo=producto.activo,
        )

    def update_stock(self, producto_id: int, cantidad: int) -> Producto:
        producto = self._get_or_404(producto_id)

        stock_final = producto.stock + cantidad

        if stock_final < 0:
            raise ValueError(
                f"Cantidad insuficiente de {producto.nombre} para realizar la operacion"
            )

        producto.stock = stock_final
        self.repo.session.add(producto)

        return producto
