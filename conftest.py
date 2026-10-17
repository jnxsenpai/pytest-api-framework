import pytest
from services.products.api import Products

@pytest.fixture(scope="session")
def products() -> Products:
    """Один экземпляр API-клиента на весь прогон."""
    return Products()

@pytest.fixture
def created_product(products):
    product = products.create_product()
    yield product
    products.delete_product(product.id)