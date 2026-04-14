from fastapi import APIRouter, Depends
from app.modules.movimiento import service
from app.modules.movimiento import schemas
from sqlmodel import Session
from app.core.database import get_session

router = APIRouter(prefix="/movimientos", tags=["movimientos"])


@router.post("/", response_model=schemas.MovimientoFullRead)
def create_movimiento(
    data: schemas.MovimientoCreate, session: Session = Depends(get_session)
):
    return service.create_movimiento(session, data)


@router.get("/", response_model=list[schemas.MovimientoRead])
def get_all(session: Session = Depends(get_session), incluir_inactivos: bool = False):
    return service.get_all(session, incluir_inactivos)


@router.get("/{movimiento_id}", response_model=schemas.MovimientoFullRead)
def get_by_id(
    movimiento_id: int,
    session: Session = Depends(get_session),
    incluir_inactivos: bool = False,
):
    return service.get_by_id(session, movimiento_id, incluir_inactivos)


@router.delete("/{movimiento_id}", response_model=schemas.MovimientoRead)
def delete(movimiento_id: int, session: Session = Depends(get_session)):
    return service.delete(session, movimiento_id)
