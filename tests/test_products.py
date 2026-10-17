import math

import allure
import pytest

from config.base_test import BaseTest


class TestProducts(BaseTest):

    @allure.title("Get products with default parameters")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_products(self):
        response = self.products_api.get_products()

        assert response.meta.page == 1
        assert response.meta.per_page == 20
        assert len(response.data) <= response.meta.per_page

    @allure.title("Get products - validate pagination metadata")
    @pytest.mark.regression
    def test_get_products_pagination_metadata(self):
        response = self.products_api.get_products()

        expected_total_pages = (
            math.ceil(
                response.meta.total / response.meta.per_page
            )
            if response.meta.total > 0
            else 0
        )

        assert response.meta.total_pages == expected_total_pages
        assert len(response.data) <= response.meta.per_page

    @allure.title("Get products with different limits")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "limit",
        [1, 10, 20, 100],
        ids=[
            "limit_1",
            "limit_10",
            "limit_20",
            "limit_100",
        ]
    )
    def test_get_products_with_limit(self, limit):
        response = self.products_api.get_products(
            limit=limit
        )

        assert response.meta.per_page == limit
        assert len(response.data) <= limit

    @allure.title("Get products - pagination")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "page, limit",
        [
            (1, 10),
            (2, 10),
            (1, 20),
            (2, 20),
        ],
        ids=[
            "page_1_limit_10",
            "page_2_limit_10",
            "page_1_limit_20",
            "page_2_limit_20",
        ]
    )
    def test_get_products_with_pagination(self, page, limit):
        response = self.products_api.get_products(
            page=page,
            limit=limit
        )

        assert response.meta.page == page
        assert response.meta.per_page == limit
        assert len(response.data) <= limit

    @allure.title("Get products - non-existing category")
    @pytest.mark.regression
    def test_get_products_non_existing_category(self):
        response = self.products_api.get_products(
            category="NonExistingCategory123"
        )

        assert response.data == []

    @allure.title("Get products - search and category filters")
    @pytest.mark.regression
    def test_get_products_search_and_category(self):
        category = "Electronics"
        search = "mouse"

        response = self.products_api.get_products(
            category=category,
            search=search
        )

        for product in response.data:
            assert product.category == category

            assert (
                search.lower() in product.name.lower()
                or search.lower() in product.description.lower()
            )

    @allure.title("Get products - pagination with category filter")
    @pytest.mark.regression
    def test_get_products_pagination_with_filter(self):
        response = self.products_api.get_products(
            page=2,
            limit=10,
            category="Electronics"
        )

        assert response.meta.page == 2
        assert response.meta.per_page == 10

        for product in response.data:
            assert product.category == "Electronics"

    @allure.title("Get products - minimum price filter")
    @pytest.mark.regression
    def test_get_products_min_price(self):
        min_price = 100

        response = self.products_api.get_products(
            min_price=min_price
        )

        for product in response.data:
            assert product.price >= min_price

    @allure.title("Get products - maximum price filter")
    @pytest.mark.regression
    def test_get_products_max_price(self):
        max_price = 100

        response = self.products_api.get_products(
            max_price=max_price
        )

        for product in response.data:
            assert product.price <= max_price

    @allure.title("Get products - price range filter")
    @pytest.mark.regression
    def test_get_products_price_range(self):
        min_price = 50
        max_price = 200

        response = self.products_api.get_products(
            min_price=min_price,
            max_price=max_price
        )

        for product in response.data:
            assert min_price <= product.price <= max_price

    @allure.title("Get products - exact price filter")
    @pytest.mark.regression
    def test_get_products_exact_price(self):
        price = 100

        response = self.products_api.get_products(
            min_price=price,
            max_price=price
        )

        for product in response.data:
            assert product.price == price

    @allure.title("Get products - sort by price ascending")
    @pytest.mark.regression
    def test_get_products_sort_price_asc(self):
        response = self.products_api.get_products(
            sort="price_asc"
        )

        prices = [
            product.price
            for product in response.data
        ]

        assert prices == sorted(prices)

    @allure.title("Get products - sort by price descending")
    @pytest.mark.regression
    def test_get_products_sort_price_desc(self):
        response = self.products_api.get_products(
            sort="price_desc"
        )

        prices = [
            product.price
            for product in response.data
        ]

        assert prices == sorted(
            prices,
            reverse=True
        )

    @allure.title("Get products - sort by rating")
    @pytest.mark.regression
    def test_get_products_sort_rating(self):
        response = self.products_api.get_products(
            sort="rating"
        )

        ratings = [
            product.rating
            for product in response.data
        ]

        assert ratings == sorted(
            ratings,
            reverse=True
        )

    @allure.title("Get products - combined filters")
    @pytest.mark.regression
    def test_get_products_combined_filters(self):
        response = self.products_api.get_products(
            category="Electronics",
            min_price=10,
            max_price=500,
            sort="price_asc",
            page=1,
            limit=20
        )

        prices = []

        for product in response.data:
            assert product.category == "Electronics"
            assert 10 <= product.price <= 500

            prices.append(product.price)

        assert prices == sorted(prices)
        assert len(response.data) <= 20

    @allure.title("Create new product")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "overrides",
    [
        pytest.param(
            {"name": "Required only", "price": 10.5, "category": "Electronics"},
            id="only-required-fields",
        ),
        pytest.param(
            {
                "name": "Full product",
                "price": 99.99,
                "category": "Electronics",
                "stock": 30,
                "description": "RGB mechanical gaming keyboard",
                "image_url": "https://via.placeholder.com/300",
                "rating": 4.8,
                "reviews_count": 45,
            },
            id="all-fields",
        ),
    ],
)
    def test_create_product(self, overrides):
        response = self.products_api.create_product(**overrides)
        for key, value in overrides.items():
            assert getattr(response, key) == value, (
                f"Field '{key}' mismatch: expected {value}, got {getattr(response, key)}"
            )

    @allure.title("Get product by id")
    @pytest.mark.regression
    def test_get_product_by_id(self, created_product):
        fetched = self.products_api.get_product_by_id(created_product.id)
        assert fetched.id == created_product.id