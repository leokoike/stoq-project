
build-api:
	@docker compose -f api/compose.yml build

run-api:
	@docker compose -f api/compose.yml up -d

test-api:
	cd api/ && uv run pytest

stop-api:
	@docker compose -f api/compose.yml down -t 0

revision:
	@cd api/ && uv run alembic revision --autogenerate -m "$(m)"

upgrade:
	@cd api/ && uv run alembic upgrade head

downgrade:
	@cd api/ && uv run alembic downgrade -1

seed-products:
	@docker compose -f api/compose.yml exec api uv run python -m src.infrastructure.cli.main seed products

seed-products-clear:
	@docker compose -f api/compose.yml exec api uv run python -m src.infrastructure.cli.main seed products --clear

build-frontend:
	@cd front/product-app && npm install && npm run build

run-frontend:
	@cd front/product-app && npm run dev