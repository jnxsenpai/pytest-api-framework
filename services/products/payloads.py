from faker import Faker
faker = Faker()

class Payloads:

    def create_product(
            self,
            name: str | None = None,
            price: float | None = None,
            category: str | None = None,
            stock: int | None = None,
            description: str | None = None,
            image_url: str | None = None,
            rating: float | None = None,
            reviews_count: int | None = None,
    ) -> dict:
        """
                Собирает тело запроса для POST /api/products.
                Обязательные поля (name, price, category) генерируются через Faker,
                если не переданы. Опциональные поля добавляются только если не None.
                """
        payload = {
            "name": name or faker.random_company_product(),
            "price": price if price is not None else faker.pyfloat(min_value=1, max_value=1000, right_digits=2),
            "category": category or faker.company_category(),
        }

        optional = {
            "stock": stock,
            "description": description,
            "image_url": image_url,
            "rating": rating,
            "reviews_count": reviews_count,
        }

        # добавляем только те опциональные поля, которые явно переданы
        payload.update({k: v for k, v in optional.items() if v is not None})
        return payload