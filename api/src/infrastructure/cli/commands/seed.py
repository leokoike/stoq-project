import asyncio
import typer
from sqlalchemy import select
from src.infrastructure.database.connection import async_session_maker
from src.infrastructure.database.models import ProductModel
from src.domain.entities.product import SellingPlaceEnum
from src.utils.logs import get_logger

logger = get_logger(__name__)
app = typer.Typer(help="Database seeding commands")


async def seed_products():
    """Seed the database with initial product data"""
    async with async_session_maker() as session:
        # Check if data already exists
        result = await session.execute(select(ProductModel).limit(1))
        existing = result.scalar_one_or_none()

        if existing:
            logger.info("Database already contains products. Skipping seed.")
            return

        # Sample products to seed
        products = [
            ProductModel(
                name="Wireless Bluetooth Headphones",
                ean="1234567890123",
                price=79.99,
                description="High-quality wireless headphones with noise cancellation",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Laptop Stand Adjustable",
                ean="2345678901234",
                price=45.50,
                description="Ergonomic laptop stand with adjustable height",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="USB-C Hub Multiport",
                ean="3456789012345",
                price=29.99,
                description="7-in-1 USB-C hub with HDMI, USB ports, and SD card reader",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Mechanical Keyboard RGB",
                ean="4567890123456",
                price=129.99,
                description="Gaming mechanical keyboard with RGB backlighting",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Wireless Mouse Ergonomic",
                ean="5678901234567",
                price=39.99,
                description="Ergonomic wireless mouse with adjustable DPI",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Webcam HD 1080p",
                ean="6789012345678",
                price=59.99,
                description="HD webcam with built-in microphone for video calls",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Phone Case Protective",
                ean="7890123456789",
                price=19.99,
                description="Protective phone case with shock absorption",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Portable SSD 1TB",
                ean="8901234567890",
                price=149.99,
                description="Fast portable SSD with 1TB storage capacity",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Desk Lamp LED",
                ean="9012345678901",
                price=34.99,
                description="LED desk lamp with adjustable brightness and color temperature",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Monitor 27 inch 4K",
                ean="0123456789012",
                price=399.99,
                description="27-inch 4K UHD monitor with HDR support",
                active=False,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Graphics Tablet Drawing",
                ean="1112223334445",
                price=89.99,
                description="Professional graphics tablet for digital art",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Smartphone Stand Holder",
                ean="2223334445556",
                price=15.99,
                description="Adjustable smartphone stand for desk",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="External Battery Pack",
                ean="3334445556667",
                price=49.99,
                description="20000mAh portable battery pack with fast charging",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Smart Watch Fitness",
                ean="4445556667778",
                price=199.99,
                description="Smart watch with fitness tracking and heart rate monitor",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Cable Organizer Set",
                ean="5556667778889",
                price=12.99,
                description="Set of cable organizers for desk management",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Bluetooth Speaker Portable",
                ean="6667778889990",
                price=69.99,
                description="Waterproof portable speaker with 12-hour battery life",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Microphone USB Streaming",
                ean="7778889990001",
                price=99.99,
                description="Professional USB microphone for streaming and podcasting",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Gaming Chair Ergonomic",
                ean="8889990001112",
                price=249.99,
                description="Ergonomic gaming chair with lumbar support and adjustable armrests",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Screen Protector Tempered Glass",
                ean="9990001112223",
                price=9.99,
                description="Tempered glass screen protector with oleophobic coating",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Cooling Pad Laptop",
                ean="0001112223334",
                price=27.99,
                description="Laptop cooling pad with dual fans and adjustable height",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Wireless Charger Fast",
                ean="1113334445557",
                price=24.99,
                description="15W fast wireless charger compatible with Qi devices",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="HDMI Cable 4K 6ft",
                ean="2224445556668",
                price=14.99,
                description="High-speed HDMI cable supporting 4K@60Hz and HDR",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Memory Card 128GB",
                ean="3335556667779",
                price=19.99,
                description="MicroSD card 128GB with adapter for cameras and phones",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Webcam Cover Slider",
                ean="4446667778880",
                price=6.99,
                description="Privacy webcam cover slider pack of 3",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Document Scanner Portable",
                ean="5557778889991",
                price=179.99,
                description="Portable document scanner with automatic document feeder",
                active=False,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Ring Light LED",
                ean="6668889990002",
                price=39.99,
                description="10-inch LED ring light with tripod for photography and video",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Mouse Pad Extended",
                ean="7779990001113",
                price=18.99,
                description="Extended mouse pad XXL size with stitched edges",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Surge Protector 8 Outlet",
                ean="8880001112224",
                price=32.99,
                description="8-outlet surge protector with 4 USB ports and 6ft cord",
                active=True,
                selling_place=SellingPlaceEnum.STORE,
                picture=None,
            ),
            ProductModel(
                name="Presentation Pointer",
                ean="9991112223335",
                price=22.99,
                description="Wireless presenter with laser pointer and remote control",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
            ProductModel(
                name="Tablet Stylus Pen",
                ean="0002223334446",
                price=29.99,
                description="Active stylus pen with palm rejection for tablets",
                active=True,
                selling_place=SellingPlaceEnum.EVENT,
                picture=None,
            ),
        ]

        session.add_all(products)
        await session.commit()

        logger.info(f"Successfully seeded {len(products)} products into the database")
        return len(products)


async def clear_products():
    """Clear all products from the database"""
    async with async_session_maker() as session:
        result = await session.execute(select(ProductModel))
        products = result.scalars().all()
        count = len(products)

        for product in products:
            await session.delete(product)

        await session.commit()
        logger.info(f"Cleared {count} products from the database")
        return count


@app.command()
def products(
    clear: bool = typer.Option(
        False, "--clear", help="Clear existing products before seeding"
    ),
):
    """
    Seed the database with sample products.

    Use --clear flag to clear existing products first.
    """

    async def run():
        try:
            if clear:
                typer.echo("Clearing existing products...")
                count = await clear_products()
                typer.secho(f"✓ Cleared {count} products", fg=typer.colors.YELLOW)

            typer.echo("Seeding products...")
            count = await seed_products()

            if count:
                typer.secho(
                    f"✓ Successfully seeded {count} products!", fg=typer.colors.GREEN
                )
            else:
                typer.secho(
                    "⚠ Products already exist. Use --clear to reset.",
                    fg=typer.colors.YELLOW,
                )
        except Exception as e:
            typer.secho(f"✗ Error seeding products: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    asyncio.run(run())


@app.command()
def clear():
    """Clear all products from the database"""

    async def run():
        try:
            confirm = typer.confirm("Are you sure you want to clear all products?")
            if not confirm:
                typer.echo("Cancelled")
                raise typer.Abort()

            typer.echo("Clearing products...")
            count = await clear_products()
            typer.secho(f"✓ Cleared {count} products", fg=typer.colors.GREEN)
        except typer.Abort:
            raise
        except Exception as e:
            typer.secho(
                f"✗ Error clearing products: {e}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(code=1)

    asyncio.run(run())
