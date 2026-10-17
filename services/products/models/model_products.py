from pydantic import BaseModel, Field, field_validator


class ProductItem(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    description: str
    category: str = Field(min_length=1)
    price: float = Field(ge=0)
    rating: float = Field(ge=0, le=5)
    reviews_count: int = Field(ge=0)
    stock: int = Field(ge=0)
    image_url: str = Field(min_length=1)

    @field_validator("name", "category", "image_url")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value must not be blank")
        return value


class MetaData(BaseModel):
    page: int = Field(ge=1)
    per_page: int = Field(ge=1, le=100)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class ProductsResponse(BaseModel):
    data: list[ProductItem]
    meta: MetaData


class ProductCreateResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    category: str = Field(min_length=1)
    stock: int | None = Field(None, ge=0)
    description: str | None = None
    image_url: str | None = None
    rating: float | None = Field(None, ge=0, le=5)
    reviews_count: int | None = Field(None, ge=0)

    @field_validator("name", "category")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value must not be blank")
        return value