from config.stages import get_stage

STAGE = get_stage()

class Endpoints:
    get_products = f"{STAGE}/api/products"
    create_product = f"{STAGE}/api/products"

    def get_product_by_id(self, id):
        return f"{STAGE}/api/products/{id}"

    def update_product(self, id):
        return f"{STAGE}/api/products/{id}"

    def delete_product(self, id):
        return f"{STAGE}/api/products/{id}"