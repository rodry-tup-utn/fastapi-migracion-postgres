from fastapi import APIRouter, Depends
from app.modules.categoria import service
from app.modules.categoria import schemas
from app.core.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=list[schemas.CategoriaBaseRead])
def get_all(session: Session = Depends(get_session), incluir_inactivos: bool = False):

    return service.get_categorias(session)


@router.get("/{id}", response_model=schemas.CategoriaFullRead)
def get_categoria(
    id: int,
    incluir_inactivos: bool = False,
    session: Session = Depends(get_session),
):

    return service.get_categoria(session, id)


@router.post("/", response_model=schemas.CategoriaBaseRead)
def create_categoria(
    data: schemas.CategoriaCreate, session: Session = Depends(get_session)
):
    return service.create_categoria(session, data)


@router.patch("/{id}", response_model=schemas.CategoriaFullRead)
def update_categoria(
    id: int, data: schemas.CategoriaUpdate, session: Session = Depends(get_session)
):
    return service.update_categoria(session, id, data)


@router.delete("/{id}")
def delete_categoria(id: int, session: Session = Depends(get_session)):
    return service.delete_categoria(session, id)
