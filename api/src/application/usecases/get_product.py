from uuid import UUID
from src.application.exceptions.exceptions import NoResultFoundException
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: UUID) -> Product:
        product = await self.product_repository.get_product_by_id(product_id)
        if not product:
            raise NoResultFoundException("Product not found")
        return product
