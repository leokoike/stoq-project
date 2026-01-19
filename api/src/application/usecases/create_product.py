from src.application.dtos.create_product import CreateProductDTO
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, dto: CreateProductDTO) -> Product:
        product = Product(
            id=None,
            **dto.model_dump(),
        )
        return await self.product_repository.create_product(product)
