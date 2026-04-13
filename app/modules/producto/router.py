from fastapi import APIRouter, Depends
from app.modules.producto import service
from sqlmodel import Session
from app.core.database import get_session
from app.modules.producto.schemas import ProductoCreate, ProductoUpdate, ProductoRead

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("/", response_model=ProductoRead)
def create_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return service.create_producto(session, data)


@router.get("/", response_model=list[ProductoRead])
def get_productos(
    session: Session = Depends(get_session), incluir_inactivos: bool = False
):
    return service.get_productos(session, incluir_inactivos)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto_id(
    producto_id: int,
    session: Session = Depends(get_session),
    incluir_inactivos: bool = False,
):
    return service.get_producto(session, producto_id, incluir_inactivos)


@router.delete("/{iproducto_id}")
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    return service.delete_producto(session, producto_id)


@router.patch("/{producto_id}")
def update_producto(
    producto_id: int, data: ProductoUpdate, session: Session = Depends(get_session)
):
    return service.update_producto(session, producto_id, data)
