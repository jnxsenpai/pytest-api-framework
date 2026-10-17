import pytest
from services.products.api import Products


class BaseTest():
    @pytest.fixture(autouse=True)
    def _inject_services(self, products_api):
        # self.products_api — тот же объект, что и фикстура products_api
        self.products_api = products_api