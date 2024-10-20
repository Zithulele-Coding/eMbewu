import reflex as rx
import sqlmodel

from typing import Optional, List


class User(rx.Model, table=True):
    email: str
    role: str = sqlmodel.Field(sqlmodel.Enum(
        choices=["admin", "customer", "provider"], default="customer"))


class Product(rx.Model, table=True):
    name: str
    wholesale_price: float
    retail_price: float
    description: str


class Provider(rx.Model, table=True):
    name: str
    about: str
    contact: Optional[str] = None
    phone: Optional[str] = None

    # relationships to products
    products: List[Product] = rx.Relationship(back_populates="provider")
