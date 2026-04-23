from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int | None = None

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category_id: int | None = None

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class ProductSimple(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    total: int
    items: list[Product]


class CategoryCreate(BaseModel):
    name: str

class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryWithProducts(BaseModel):
    id: int
    name: str
    products: list[ProductSimple]

    class Config:
        from_attributes = True
