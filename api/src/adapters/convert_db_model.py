from src.domain.entities.product import Product
from src.infrastructure.database.models import ProductModel


def convert_db_model_to_entity(product_model: ProductModel) -> Product:
    return Product(
        id=product_model.id,
        name=product_model.name,
        ean=product_model.ean,
        description=product_model.description,
        inserted_at=product_model.inserted_at,
        price=product_model.price,
        active=product_model.active,
        selling_place=product_model.selling_place,
        picture=product_model.picture,
    )
