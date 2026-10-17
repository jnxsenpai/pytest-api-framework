import allure
import requests
from urllib3.util import url

from utils.helper import Helper
from config.headers import Headers
from services.products.payloads import Payloads
from services.products.endpoints import Endpoints
from services.products.models.model_products import ProductsResponse, ProductItem, ProductCreateResponse

@allure.epic("Company")
@allure.feature("Products")
class Products(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    @allure.step("Get all products")
    def get_products(
        self,
        page: int = 1,
        limit: int = 20,
        category: str | None = None,
        search: str | None = None,
        sort: str = "newest",
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> ProductsResponse:

        params = {
            "page": page,
            "limit": limit,
            "sort": sort,
        }

        if category is not None:
            params["category"] = category

        if search is not None:
            params["search"] = search

        if min_price is not None:
            params["min_price"] = min_price

        if max_price is not None:
            params["max_price"] = max_price

        response = requests.get(
            url=self.endpoints.get_products,
            headers=self.headers.headers,
            params=params
        )

        return self.validate_response(
            response=response,
            model=ProductsResponse,
            expected_status_code=200
        )

    @allure.step("Get product by id")
    def get_product_by_id(self, id: int) ->  ProductItem:
        response = requests.get(
            url=self.endpoints.get_product_by_id(id),
            headers=self.headers.headers
        )

        return self.validate_response(
            response=response,
            model= ProductItem,
            expected_status_code=200
        )

    @allure.step("Create product")
    def create_product(
        self,
        expected_status_code: int = 201,
        **kwargs
    ) -> ProductCreateResponse:
        url = self.endpoints.create_product
        payload = self.payloads.create_product(**kwargs)

        response = requests.post(
            url=url,
            headers=self.headers.headers,
            json=payload
        )

        return self.validate_response(
            response=response,
            model= ProductCreateResponse,
            expected_status_code=expected_status_code
        )




