import reflex as rx
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Dict
import os

# Database setup
DATABASE_URL = "postgresql://coffeedb_owner:JEvnWBFp67xV@ep-still-flower-a54nulqa.us-east-2.aws.neon.tech/coffeedb?sslmode=require"

Base = declarative_base()

class DBProduct(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    description = Column(String)
    image = Column(String)
    rating = Column(JSON)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Product(rx.Base):
    id: int
    title: str
    price: float
    description: str
    image: str
    rating: Dict[str, float]

def product_card(product: Product) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.image(
                src=product.image,
                height="200px",
                width="100%",
                object_fit="contain",
            ),
            rx.heading(
                product.title,
                size="5",
                no_of_lines=2,
                height="3em",
            ),
            rx.text(
                product.description,
                no_of_lines=3,
                color="gray.500",
            ),
            rx.hstack(
                rx.text(
                    f"R{product.price:.2f}",
                    font_weight="bold",
                    font_size="lg",
                ),
                rx.hstack(
                    rx.icon("star", color="yellow.400"),
                    rx.text(f"{product.rating['rate']:.1f}"),
                ),
                width="100%",
                justify="between",  # Changed from "space-between" to "between"
            ),
            rx.button(
                "Add to Cart",
                width="100%",
                bg=rx.color("accent", 5),
                color="white",
            ),
            align="start",
            spacing="3",
            padding="4",
            border_width="1px",
            border_radius="lg",
            bg="rgba(255,255,255,0.05)",
            height="100%",
        )
    )

class State(rx.State):
    """The app state."""
    products: List[Product] = []
    loading: bool = False
    error: str = ""

    async def get_products(self):
        self.loading = True
        try:
            session = SessionLocal()
            db_products = session.query(DBProduct).all()
            self.products = [
                Product(
                    id=p.id,
                    title=p.title,
                    price=p.price,
                    description=p.description,
                    image=p.image,
                    rating=p.rating
                ) for p in db_products
            ]
        except Exception as e:
            self.error = str(e)
        finally:
            session.close()
            self.loading = False

    def sort_by_price_asc(self):
        self.products = sorted(self.products, key=lambda x: x.price)

    def sort_by_price_desc(self):
        self.products = sorted(self.products, key=lambda x: x.price, reverse=True)

    def sort_by_rating(self):
        self.products = sorted(self.products, key=lambda x: x.rating["rate"], reverse=True)

def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4", weight="medium"),
        ),
        href=url,
    )

def navbar_icons_menu_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(text, size="3", weight="medium"),
        ),
        href=url,
    )

def navbar_icons() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Embewu", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_icons_item("Menu", "shopping-basket", "/#"),
                    navbar_icons_item("About Us", "info", "/#"),
                    navbar_icons_item("Contact", "phone", "/#"),
                    spacing="6",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Reflex", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        navbar_icons_menu_item("menu", "shopping-basket", "/#"),
                        navbar_icons_item("About Us", "info", "/#"),
                    navbar_icons_item("Contact", "phone", "/#"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )

def footer_item(text: str, href: str) -> rx.Component:
    return rx.link(rx.text(text, size="3"), href=href)

def footer_items_1() -> rx.Component:
    return rx.flex(
        rx.heading(
            "Operating Time", size="4", weight="bold", as_="h3"
        ),
        footer_item("Mon-Fri", "/#"),
        footer_item("8:00 - 17:00", "/#"),
        spacing="4",
        text_align=["end", "end", "start"],
        flex_direction="column",
    )

def social_link(icon: str, href: str) -> rx.Component:
    return rx.link(rx.icon(icon), href=href)

def socials() -> rx.Component:
    return rx.flex(
        social_link("instagram", "/#"),
        social_link("twitter", "/#"),
        social_link("facebook", "/#"),
        social_link("linkedin", "/#"),
        spacing="3",
        justify="start",
        width="100%",
    )

def footer() -> rx.Component:
    return rx.el.footer(
        rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.image(
                            src="/logo.jpg",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.heading(
                            "Embewu",
                            size="7",
                            weight="bold",
                        ),
                        align_items="center",
                    ),
                    rx.text(
                        "© 2024 Embewu, Inc",
                        size="3",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    spacing="2",  
                    align_items=[
                        "center",
                        "center",
                        "start",
                    ],
                ),
                footer_items_1(),
                justify="center",
                spacing="4", 
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            rx.divider(),
            rx.hstack(
                rx.hstack(
                    footer_item("Privacy Policy", "/#"),
                    footer_item("Terms of Service", "/#"),
                    spacing="2",  
                    align="center",
                    width="100%",
                ),
                socials(),
                justify="between",
                width="100%",
            ),
            spacing="3",  
            width="100%",
            padding_y="2",  
        ),
        width="100%",
    )

def index() -> rx.Component:
    return rx.box(
        navbar_icons(),
        # Search bar and filter buttons
        rx.container(
            rx.hstack(
                rx.input(
                    placeholder="Search...",
                    border_radius="20px",
                    padding="2",
                    width="100%",
                ),
                rx.button(
                    "Special",
                    border_radius="md",
                    bg=rx.color("accent", 5),
                    color="white",
                    padding_x="4",
                    on_click=State.sort_by_rating,
                ),
                rx.button(
                    "Price ↑",
                    border_radius="md",
                    bg=rx.color("accent", 5),
                    color="white",
                    padding_x="4",
                    on_click=State.sort_by_price_asc,
                ),
                rx.button(
                    "Price ↓",
                    border_radius="md",
                    bg=rx.color("accent", 5),
                    color="white",
                    padding_x="4",
                    on_click=State.sort_by_price_desc,
                ),
                rx.button(
                    "Rating",
                    border_radius="md",
                    bg=rx.color("accent", 5),
                    color="white",
                    padding_x="4",
                    on_click=State.sort_by_rating,
                ),
                spacing="4",
                padding_y="4",
            ),
        ),
        # Product grid
        rx.container(
            rx.cond(
                State.loading,
                rx.center(
                    rx.spinner(),
                    padding_y="8em",
                ),
                rx.cond(
                    State.error,
                    rx.text(State.error, color="red"),
                    rx.vstack(
                        # First row
                        rx.hstack(
                            rx.foreach(
                                State.products[:3],  # First 3 products
                                lambda product: product_card(product),
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        # Second row
                        rx.hstack(
                            rx.foreach(
                                State.products[3:6],  # Next 3 products
                                lambda product: product_card(product),
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        # Third row
                        rx.hstack(
                            rx.foreach(
                                State.products[6:9],  # Last 3 products
                                lambda product: product_card(product),
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        width="100%",
                        spacing="4",
                        padding_y="4",
                    ),
                ),
            ),
            padding_y="4",
        ),
        footer(),
        on_mount=State.get_products,
    )
app = rx.App()
app.add_page(index)