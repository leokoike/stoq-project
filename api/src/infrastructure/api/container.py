from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.application.usecases.get_product import GetProductUseCase
from src.application.usecases.list_products import ListProductsUseCase
from src.application.usecases.create_product import CreateProductUseCase
from src.application.usecases.update_product import UpdateProductUseCase
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.product_repository import (
    SQLAlchemyProductRepository,
)


async def get_session(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[AsyncSession, None]:
    return session


async def get_product_repository(
    session: AsyncSession = Depends(get_session),
) -> ProductRepository:
    return SQLAlchemyProductRepository(session)


async def list_products_usecase(
    product_repository: ProductRepository = Depends(get_product_repository),
) -> ListProductsUseCase:
    return ListProductsUseCase(product_repository)


async def create_product_usecase(
    product_repository: ProductRepository = Depends(get_product_repository),
) -> CreateProductUseCase:
    return CreateProductUseCase(product_repository)


async def update_product_usecase(
    product_repository: ProductRepository = Depends(get_product_repository),
) -> UpdateProductUseCase:
    return UpdateProductUseCase(product_repository)


async def get_product_usecase(
    product_repository: ProductRepository = Depends(get_product_repository),
) -> GetProductUseCase:
    return GetProductUseCase(product_repository)
