from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from app.core.database import engine
from app.modules.categoria.model import Categoria
from app.modules.producto.model import Producto
from app.modules.movimiento.model import Movimiento
from app.modules.producto.router import router as producto_router
from app.modules.categoria.router import router as categoria_router
from app.modules.movimiento.router import router as movimiento_router
from app.core.errors import NotFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, description="Api Basica de Productos y Categorias")


@app.exception_handler(NotFoundException)
def not_found_handler(request, e):
    return JSONResponse(status_code=404, content={"detail": str(e)})


@app.exception_handler(ValueError)
def value_error_handler(request, e):
    return JSONResponse(status_code=400, content={"detail": str(e)})


app.include_router(producto_router)
app.include_router(categoria_router)
app.include_router(movimiento_router)
