from fastapi import APIRouter, Depends
from app.modules.producto.service import ProductoService
from sqlmodel import Session
from app.core.database import get_session
from app.modules.producto.schemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoRead,
    StockEstadoRead,
)

router = APIRouter(prefix="/productos", tags=["productos"])


def get_product_service(session: Session = Depends(get_session)) -> ProductoService:
    return ProductoService(session)


@router.post("/", response_model=ProductoRead)
def create_producto(
    data: ProductoCreate, svc: ProductoService = Depends(get_product_service)
):
    return svc.create(data)


@router.get("/", response_model=list[ProductoRead])
def get_productos(
    incluir_inactivos: bool = False, svc: ProductoService = Depends(get_product_service)
):
    return svc.get_all(incluir_inactivos)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto_id(
    producto_id: int,
    incluir_inactivos: bool = False,
    svc: ProductoService = Depends(get_product_service),
):
    return svc.get_by_id(producto_id, incluir_inactivos)


@router.delete("/{producto_id}", response_model=ProductoRead)
def delete_producto(
    producto_id: int, svc: ProductoService = Depends(get_product_service)
):
    return svc.delete(producto_id)


@router.patch("/{producto_id}", response_model=ProductoRead)
def update_producto(
    producto_id: int,
    data: ProductoUpdate,
    svc: ProductoService = Depends(get_product_service),
):
    return svc.update(producto_id, data)


@router.get("/estado-stock/{producto_id}", response_model=StockEstadoRead)
def obtener_estado_stock(
    producto_id: int, svc: ProductoService = Depends(get_product_service)
):
    return svc.obtener_estado_stock(producto_id)
