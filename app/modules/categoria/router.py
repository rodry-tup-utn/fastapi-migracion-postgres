from fastapi import APIRouter, Depends
from app.modules.categoria.service import CategoriaService
from app.modules.categoria import schemas
from app.core.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/categorias", tags=["categorias"])


def get_category_service(session: Session = Depends(get_session)) -> CategoriaService:
    return CategoriaService(session)


@router.get("/", response_model=list[schemas.CategoriaRead])
def get_all(
    incluir_inactivos: bool = False,
    svc: CategoriaService = Depends(get_category_service),
):
    return svc.get_all(incluir_inactivos)


@router.get("/{id}", response_model=schemas.CategoriaFullRead)
def get_categoria(
    id: int,
    incluir_inactivos: bool = False,
    svc: CategoriaService = Depends(get_category_service),
):
    return svc.get_by_id(id, incluir_inactivos)


@router.post("/", response_model=schemas.CategoriaRead)
def create_categoria(
    data: schemas.CategoriaCreate, svc: CategoriaService = Depends(get_category_service)
):
    return svc.create(data)


@router.patch("/{id}", response_model=schemas.CategoriaFullRead)
def update_categoria(
    id: int,
    data: schemas.CategoriaUpdate,
    svc: CategoriaService = Depends(get_category_service),
):
    return svc.update(id, data)


@router.delete("/{id}")
def delete_categoria(id: int, svc: CategoriaService = Depends(get_category_service)):
    return svc.delete(id)
