from uuid import UUID
from fastapi import APIRouter, Depends

from src.application.usecases.get_product import GetProductUseCase
from src.application.dtos.update_product import UpdateProductDTO
from src.application.usecases.update_product import UpdateProductUseCase
from src.application.dtos.create_product import CreateProductDTO
from src.application.usecases.create_product import CreateProductUseCase
from src.application.usecases.list_products import ListProductsUseCase
from src.infrastructure.api.container import (
    create_product_usecase,
    list_products_usecase,
    update_product_usecase,
    get_product_usecase,
)

router = APIRouter()


@router.get("/products/{product_id}")
async def get_product(
    product_id: UUID,
    get_product_usecase: GetProductUseCase = Depends(get_product_usecase),
):
    return await get_product_usecase.execute(product_id)


@router.get("/products")
async def list_products(
    page: int = 1,
    size: int = 20,
    name: str | None = None,
    list_products_usecase: ListProductsUseCase = Depends(list_products_usecase),
):
    return await list_products_usecase.execute(page=page, size=size, filter_name=name)


@router.post("/products")
async def create_product(
    dto: CreateProductDTO,
    create_product_usecase: CreateProductUseCase = Depends(create_product_usecase),
):
    return await create_product_usecase.execute(dto)


@router.put("/products/{product_id}")
async def update_product(
    product_id: UUID,
    update_data: UpdateProductDTO,
    update_product_usecase: UpdateProductUseCase = Depends(update_product_usecase),
):
    return await update_product_usecase.execute(product_id, update_data)
