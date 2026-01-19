from uuid import UUID
from src.application.dtos.update_product import UpdateProductDTO
from src.domain.repositories.product_repository import ProductRepository


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: UUID, dto: UpdateProductDTO) -> None:
        update_fields = dto.model_dump(exclude_unset=True, exclude={"id"})
        await self.product_repository.update_product(product_id, update_fields)
