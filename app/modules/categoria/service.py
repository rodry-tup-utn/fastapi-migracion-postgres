from sqlmodel import Session
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate
from app.modules.categoria.model import Categoria
from app.modules.categoria.repository import CategoriaRepository
from app.core.errors import NotFoundException
from fastapi import HTTPException, status


class CategoriaService:
    def __init__(self, session: Session):
        self.repo = CategoriaRepository(session)

    def _get_or_404(self, categoria_id: int, incluir_inactivos: bool = False):
        categoria = self.repo.get_by_id(categoria_id, incluir_inactivos)
        if not categoria:
            raise NotFoundException(
                f"No se encontro una categoria con el id {categoria_id}"
            )
        return categoria

    def create(self, data: CategoriaCreate) -> Categoria:
        categoria = Categoria.model_validate(data)
        return self.repo.create(categoria)

    def get_all(self, incluir_inactivos: bool = False) -> list[Categoria]:
        return self.repo.get_all(incluir_inactivos)

    def get_by_id(
        self, categoria_id: int, incluir_inactivos: bool = False
    ) -> Categoria:
        categoria = self._get_or_404(categoria_id, incluir_inactivos)

        return categoria

    def update(self, categoria_id: int, data: CategoriaUpdate) -> Categoria:
        categoria = self._get_or_404(categoria_id)

        data_dict = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in data_dict.items():
            setattr(categoria, key, value)

        return self.repo.save(categoria)

    def delete(self, categoria_id: int) -> Categoria:
        categoria = self._get_or_404(categoria_id, True)

        if categoria.activo == False:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "La categoria ya se encuentra eliminada"
            )

        categoria.activo = False
        return self.repo.save(categoria)
