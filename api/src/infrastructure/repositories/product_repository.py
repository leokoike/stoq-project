from typing import Any
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.exceptions.exceptions import (
    DatabaseException,
    NoResultFoundException,
)
from src.adapters.convert_db_model import convert_db_model_to_entity
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.database.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product_by_id(self, product_id: UUID) -> Product | None:
        result = await self.session.get(ProductModel, product_id)
        if result:
            return convert_db_model_to_entity(result)
        return None

    async def count_products(self, filter_name: str | None) -> int:
        try:
            query = select(func.count()).select_from(ProductModel)
            if filter_name:
                query = query.where(ProductModel.name.ilike(f"%{filter_name}%"))
            result = await self.session.execute(query)
            return result.scalar_one()
        except Exception as e:
            raise DatabaseException(str(e))

    async def list_products(
        self, page: int, size: int, filter_name: str | None
    ) -> list[Product]:
        try:
            offset = (page - 1) * size
            query = select(ProductModel).offset(offset).limit(size)
            if filter_name:
                query = query.where(ProductModel.name.ilike(f"%{filter_name}%"))
            result = await self.session.execute(query)
            return [
                convert_db_model_to_entity(product)
                for product in result.scalars().all()
            ]
        except Exception as e:
            raise DatabaseException(str(e))

    async def create_product(self, product_data: Product) -> Product:
        try:
            new_product = ProductModel(**product_data.model_dump(exclude={"id"}))
            self.session.add(new_product)
            await self.session.flush()
            await self.session.refresh(new_product)
            return convert_db_model_to_entity(new_product)
        except Exception as e:
            raise DatabaseException(str(e))

    async def update_product(
        self, product_id: UUID, update_fields: dict[str, Any]
    ) -> None:
        try:
            existing_product = await self.session.get(ProductModel, product_id)
            if existing_product:
                for key, value in update_fields.items():
                    setattr(existing_product, key, value)
                self.session.add(existing_product)
                await self.session.flush()
            else:
                raise NoResultFoundException("Product not found")
        except NoResultFoundException:
            raise
        except Exception as e:
            raise DatabaseException(str(e))
