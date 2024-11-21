import reflex as rx
import sqlmodel
import datetime

from typing import Optional, List


class User(rx.Model, table=True):
    email: str
    role: str = sqlmodel.Field(sqlmodel.Enum(
        choices=["admin", "customer", "provider"], default="customer"))
    description: str


class Provider(rx.Model, table=True):
    name: str
    about: str
    contact: Optional[str] = None
    phone: Optional[str] = None

    # relationships to products
    products: List["Product"] = sqlmodel.Relationship(
        back_populates="provider")


class Category(rx.Model, table=True):
    name: str
    description: Optional[str] = None

    # relationships to products
    products: List["Product"] = sqlmodel.Relationship(
        back_populates="category")


class Product(rx.Model, table=True):
    name: str
    wholesale_price: float
    retail_price: float
    description: str
    provider_id: Optional[int] = sqlmodel.Field(
        default=None, foreign_key="provider.id")
    category_id: Optional[int] = sqlmodel.Field(
        default=None, foreign_key="category.id")

    # relationships to providers
    provider: Optional["Provider"] = sqlmodel.Relationship(
        back_populates="products")
    category: Optional["Category"] = sqlmodel.Relationship(
        back_populates="products")
    cart_items: List["CartItem"] = sqlmodel.Relationship(
        back_populates="product")
    images: List["ProductImage"] = sqlmodel.Relationship(
        back_populates="product")


class ProductImage(rx.Model, table=True):
    product_id: int = sqlmodel.Field(default=None, foreign_key="product.id")
    url: str
    alt_text: Optional[str] = None

    # relationships to products
    product: Product = sqlmodel.Relationship(back_populates="images")


class Cart(rx.Model, table=True):
    user_id: int = sqlmodel.Field(default=None, foreign_key="user.id")

    # Relationships
    user: User = sqlmodel.Relationship(back_populates="carts")
    cart_items: List["CartItem"] = sqlmodel.Relationship(back_populates="cart")


class CartItem(rx.Model, table=True):
    product_id: int = sqlmodel.Field(default=None, foreign_key="product.id")
    cart_id: int = sqlmodel.Field(default=None, foreign_key="cart.id")
    quantity: int

    # Relationships
    product: Product = sqlmodel.Relationship(back_populates="cart_items")
    cart: Cart = sqlmodel.Relationship(back_populates="cart_items")


class CustomerOrder(rx.Model, table=True):
    user_id: int = sqlmodel.Field(default=None, foreign_key="user.id")
    cart_id: int = sqlmodel.Field(default=None, foreign_key="cart.id")
    order_date: datetime.datetime = sqlmodel.Field(
        default=datetime.datetime.now)
    status: str = sqlmodel.Field(default="pending")

    # Relationships
    user: User = sqlmodel.Relationship(back_populates="orders")
    cart: Cart = sqlmodel.Relationship(back_populates="orders")
