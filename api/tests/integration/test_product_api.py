import pytest
from httpx import AsyncClient
from uuid import UUID


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_success(client: AsyncClient, sample_product):
    """Test creating a product successfully"""
    # Arrange
    payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
    }

    # Act
    response = await client.post("/api/v1/products", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["ean"] == payload["ean"]
    assert data["price"] == payload["price"]
    assert data["description"] == payload["description"]
    assert data["active"] == payload["active"]
    assert data["selling_place"] == payload["selling_place"]
    assert "id" in data
    assert UUID(data["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_picture(client: AsyncClient, sample_product):
    """Test creating a product with picture (base64)"""
    # Arrange
    picture_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
        "picture": picture_base64,
    }

    # Act
    response = await client.post("/api/v1/products", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["picture"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_invalid_ean(client: AsyncClient, sample_product):
    """Test creating a product with invalid EAN"""
    # Arrange
    payload = {
        "name": sample_product["name"],
        "ean": "12345",  # Invalid: not 13 digits
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
    }

    # Act
    response = await client.post("/api/v1/products", json=payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_invalid_selling_place(
    client: AsyncClient, sample_product
):
    """Test creating a product with invalid selling place"""
    # Arrange
    payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": "invalid_place",
    }

    # Act
    response = await client.post("/api/v1/products", json=payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_missing_required_fields(client: AsyncClient):
    """Test creating a product with missing required fields"""
    # Arrange
    payload = {
        "name": "Test Product",
    }

    # Act
    response = await client.post("/api/v1/products", json=payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_success(client: AsyncClient, sample_product):
    """Test getting an existing product"""
    # Arrange - Create a product first
    create_payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    # Act
    response = await client.get(f"/api/v1/products/{product_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == create_payload["name"]
    assert data["ean"] == create_payload["ean"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_not_found(client: AsyncClient):
    """Test getting a non-existent product"""
    # Arrange
    non_existent_id = "00000000-0000-0000-0000-000000000000"

    # Act
    response = await client.get(f"/api/v1/products/{non_existent_id}")

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_invalid_uuid(client: AsyncClient):
    """Test getting a product with invalid UUID format"""
    # Arrange
    invalid_id = "not-a-uuid"

    # Act
    response = await client.get(f"/api/v1/products/{invalid_id}")

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_list_products_empty(client: AsyncClient):
    """Test listing products when database is empty"""
    # Act
    response = await client.get("/api/v1/products")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 20


@pytest.mark.asyncio(loop_scope="session")
async def test_list_products_with_data(client: AsyncClient, sample_product):
    """Test listing products with existing data"""
    # Arrange - Create multiple products
    for i in range(3):
        payload = {
            "name": f"{sample_product['name']}_{i}",
            "ean": f"123456789000{i}",
            "price": 10.0 + i,
            "description": f"Description {i}",
            "active": True,
            "selling_place": "store",
        }
        await client.post("/api/v1/products", json=payload)

    # Act
    response = await client.get("/api/v1/products")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["size"] == 20


@pytest.mark.asyncio(loop_scope="session")
async def test_list_products_pagination(client: AsyncClient, sample_product):
    """Test listing products with pagination"""
    # Arrange - Create 5 products
    for i in range(5):
        payload = {
            "name": f"{sample_product['name']}_{i}",
            "ean": f"123456789000{i}",
            "price": 10.0 + i,
            "description": f"Description {i}",
            "active": True,
            "selling_place": "event",
        }
        await client.post("/api/v1/products", json=payload)

    # Act
    response = await client.get("/api/v1/products?page=1&size=2")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["size"] == 2

    # Act - Get second page
    response = await client.get("/api/v1/products?page=2&size=2")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page"] == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_list_products_filter_by_name(client: AsyncClient, sample_product):
    """Test filtering products by name"""
    # Arrange - Create products with different names
    await client.post(
        "/api/v1/products",
        json={
            "name": "Apple Product",
            "ean": "1234567890001",
            "price": 10.0,
            "description": "Apple description",
            "active": True,
            "selling_place": "store",
        },
    )
    await client.post(
        "/api/v1/products",
        json={
            "name": "Banana Product",
            "ean": "1234567890002",
            "price": 20.0,
            "description": "Banana description",
            "active": True,
            "selling_place": "store",
        },
    )
    await client.post(
        "/api/v1/products",
        json={
            "name": "Apple Juice",
            "ean": "1234567890003",
            "price": 15.0,
            "description": "Juice description",
            "active": True,
            "selling_place": "event",
        },
    )

    # Act
    response = await client.get("/api/v1/products?name=Apple")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for item in data["items"]:
        assert "Apple" in item["name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_list_products_custom_page_size(client: AsyncClient, sample_product):
    """Test listing products with custom page size"""
    # Arrange - Create 25 products
    for i in range(25):
        payload = {
            "name": f"{sample_product['name']}_{i}",
            "ean": f"123456789{i:04d}",
            "price": 10.0 + i,
            "description": f"Description {i}",
            "active": True,
            "selling_place": "store",
        }
        await client.post("/api/v1/products", json=payload)

    # Act
    response = await client.get("/api/v1/products?size=10")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["size"] == 10


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_success(client: AsyncClient, sample_product):
    """Test updating a product successfully"""
    # Arrange - Create a product first
    create_payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    # Act - Update the product
    update_payload = {
        "name": "Updated Product Name",
        "price": 29.99,
        "active": False,
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    response = await client.get(f"/api/v1/products/{product_id}")
    data = response.json()
    assert data["name"] == "Updated Product Name"
    assert data["price"] == 29.99
    assert data["active"] is False
    assert data["ean"] == create_payload["ean"]  # Unchanged fields remain


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_partial_update(client: AsyncClient, sample_product):
    """Test partial update of a product"""
    # Arrange - Create a product first
    create_payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": True,
        "selling_place": "store",
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    # Act - Update only the description
    update_payload = {
        "description": "New description only",
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    response = await client.get(f"/api/v1/products/{product_id}")
    data = response.json()
    assert data["description"] == "New description only"
    assert data["name"] == create_payload["name"]  # Unchanged
    assert data["price"] == create_payload["price"]  # Unchanged


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_not_found(client: AsyncClient):
    """Test updating a non-existent product"""
    # Arrange
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    update_payload = {
        "name": "Updated Name",
    }

    # Act
    response = await client.put(
        f"/api/v1/products/{non_existent_id}", json=update_payload
    )

    # Assert
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_invalid_ean(client: AsyncClient, sample_product):
    """Test updating a product with invalid EAN"""
    # Arrange - Create a product first
    create_payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": sample_product["selling_place"],
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    # Act - Update with invalid EAN
    update_payload = {
        "ean": "invalid",
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_change_selling_place(client: AsyncClient, sample_product):
    """Test updating product selling place"""
    # Arrange - Create a product first
    create_payload = {
        "name": sample_product["name"],
        "ean": sample_product["ean"],
        "price": sample_product["price"],
        "description": sample_product["description"],
        "active": sample_product["active"],
        "selling_place": "store",
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    product_id = create_response.json()["id"]

    # Act - Update selling place
    update_payload = {
        "selling_place": "event",
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    response = await client.get(f"/api/v1/products/{product_id}")
    data = response.json()
    assert data["selling_place"] == "event"


@pytest.mark.asyncio(loop_scope="session")
async def test_complete_crud_workflow(client: AsyncClient, sample_product):
    """Test complete CRUD workflow: Create -> Read -> Update -> Read"""
    # Create
    create_payload = {
        "name": "Workflow Test Product",
        "ean": "9876543210123",
        "price": 100.0,
        "description": "Testing complete workflow",
        "active": True,
        "selling_place": "store",
    }
    create_response = await client.post("/api/v1/products", json=create_payload)
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    # Read
    get_response = await client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Workflow Test Product"

    # Update
    update_payload = {
        "name": "Updated Workflow Product",
        "price": 150.0,
    }
    update_response = await client.put(
        f"/api/v1/products/{product_id}", json=update_payload
    )
    assert update_response.status_code == 200

    # Read again to verify update
    final_get_response = await client.get(f"/api/v1/products/{product_id}")
    assert final_get_response.status_code == 200
    final_data = final_get_response.json()
    assert final_data["name"] == "Updated Workflow Product"
    assert final_data["price"] == 150.0


@pytest.mark.asyncio(loop_scope="session")
async def test_list_after_create_update(client: AsyncClient, sample_product):
    """Test list reflects changes after create and update operations"""
    # Create products
    product_ids = []
    for i in range(3):
        create_payload = {
            "name": f"Product {i}",
            "ean": f"111111111111{i}",
            "price": 50.0 + i,
            "description": f"Description {i}",
            "active": True,
            "selling_place": "event",
        }
        response = await client.post("/api/v1/products", json=create_payload)
        product_ids.append(response.json()["id"])

    # List all products
    list_response = await client.get("/api/v1/products")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 3

    # Update one product to be inactive
    await client.put(f"/api/v1/products/{product_ids[0]}", json={"active": False})

    # Verify in list
    list_response = await client.get("/api/v1/products")
    products = list_response.json()["items"]
    updated_product = next(p for p in products if p["id"] == product_ids[0])
    assert updated_product["active"] is False
