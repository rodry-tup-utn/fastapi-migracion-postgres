from fastapi import APIRouter, Depends
from app.modules.movimiento.service import MovimientoService
from app.modules.movimiento import schemas
from sqlmodel import Session
from app.core.database import get_session

router = APIRouter(prefix="/movimientos", tags=["movimientos"])


def get_movimiento_service(session: Session = Depends(get_session)) -> MovimientoService:
    return MovimientoService(session)


@router.post("/", response_model=schemas.MovimientoFullRead)
def create_movimiento(
    data: schemas.MovimientoCreate,
    svc: MovimientoService = Depends(get_movimiento_service),
):
    return svc.create(data)


@router.get("/", response_model=list[schemas.MovimientoRead])
def get_movimientos(
    incluir_inactivos: bool = False,
    svc: MovimientoService = Depends(get_movimiento_service),
):
    return svc.get_all(incluir_inactivos)


@router.get("/stats", response_model=schemas.DashboardStats)
def get_movimiento_stats(svc: MovimientoService = Depends(get_movimiento_service)):
    return svc.get_dashboard_stats()


@router.get("/{movimiento_id}", response_model=schemas.MovimientoFullRead)
def get_movimiento(
    movimiento_id: int,
    incluir_inactivos: bool = False,
    svc: MovimientoService = Depends(get_movimiento_service),
):
    return svc.get_by_id(movimiento_id, incluir_inactivos)


@router.delete("/{movimiento_id}", response_model=schemas.MovimientoRead)
def delete_movimiento(
    movimiento_id: int, svc: MovimientoService = Depends(get_movimiento_service)
):
    return svc.delete(movimiento_id)
