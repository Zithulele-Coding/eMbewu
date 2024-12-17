import reflex as rx
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Dict
import os

# Database setup
DB_HOST = "vaneck.app"
DB_PORT = 5432
DB_USER = "zicoder"
DB_NAME = "embewu"
DB_PASSWORD = "molo_unjani?"

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
                    navbar_icons_item("Menu", "shopping-basket", "/"),
                    navbar_icons_item("About Us", "info", "/about"),
                    navbar_icons_item("Contact", "phone", "/contact"),
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
                        navbar_icons_menu_item("menu", "shopping-basket", "/"),
                        navbar_icons_item("About Us", "info", "/about"),
                    navbar_icons_item("Contact", "phone", "/contact"),
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

def about() -> rx.Component:
    return rx.box(
        navbar_icons(),
        
        rx.box(
            # Hero Section
            rx.section(
                rx.vstack(
                    rx.heading("About Embewu", size="8", text_align="center"),
                    rx.text(
                        "Your Neighborhood Coffee Haven",
                        color="gray.500",
                        text_align="center",
                        font_size="xl",
                    ),
                    spacing="4",
                    padding_y="8",
                ),
                padding_x="12px",
                background_color="var(--gray-2)",
            ),
            
            rx.divider(),
            
            # Our Story Section
            rx.section(
                rx.vstack(
                    rx.heading("Our Story", size="6"),
                    rx.text(
                        "Founded with a passion for exceptional coffee and community connection, "
                        "Embewu has grown from a small family dream into a beloved neighborhood destination. "
                        "We take pride in sourcing our beans directly from sustainable farms across Africa, "
                        "ensuring both outstanding quality and fair compensation for farmers.",
                        color="gray.600",
                    ),
                    rx.text(
                        "Each cup is carefully prepared by our trained baristas who share our dedication "
                        "to the perfect brew. We believe in creating not just great coffee, but memorable experiences "
                        "that bring people together.",
                        color="gray.600",
                    ),
                    spacing="4",
                    align_items="start",
                ),
                padding_x="12px",
                padding_y="8",
                background_color="var(--gray-2)",
            ),
        ),
        
        footer()
    )

class ContactState(rx.State):
    name: str = ""
    email: str = ""
    message: str = ""
    success: bool = False
    name_error: str = ""
    email_error: str = ""
    message_error: str = ""

    def submit_form(self):
        self.name_error = ""
        self.email_error = ""
        self.message_error = ""
        is_valid = True

        if not self.name:
            self.name_error = "Name is required"
            is_valid = False
        if not self.email:
            self.email_error = "Email is required"
            is_valid = False
        elif "@" not in self.email:
            self.email_error = "Invalid email format"
            is_valid = False
        if not self.message:
            self.message_error = "Message is required"
            is_valid = False

        if is_valid:
            self.success = True
            self.name = ""
            self.email = ""
            self.message = ""
        else:
            self.success = False


def contact() -> rx.Component:
    return rx.box(
        navbar_icons(),
        rx.center(
            rx.vstack(
                rx.heading("Contact Us", size="4"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Your Name",
                            value=ContactState.name,
                            on_change=ContactState.set_name,
                        ),
                        rx.text(ContactState.name_error, color="red", font_size="0.8em"),
                        
                        rx.input(
                            placeholder="Your Email",
                            type_="email",
                            value=ContactState.email,
                            on_change=ContactState.set_email,
                        ),
                        rx.text(ContactState.email_error, color="red", font_size="0.8em"),
                        
                        rx.text_area(
                            placeholder="Your Message",
                            value=ContactState.message,
                            on_change=ContactState.set_message,
                            min_height="150px",
                        ),
                        rx.text(ContactState.message_error, color="red", font_size="0.8em"),
                        
                        rx.button(
                            "Send Message",
                            type_="submit",
                            bg=rx.color("accent", 5),  
                            color="white",
                            width="100%",
                            _hover={"bg": rx.color("accent", 6)},
                        ),
                        
                        rx.cond(
                            ContactState.success,
                            rx.text("Message sent successfully!", color="green.500"),
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=ContactState.submit_form,
                    width="100%",
                ),
                spacing="6",
                padding="8",
                border_radius="lg",
                box_shadow="lg",
                bg="white",
                width=["100%", "80%", "400px"],  
                margin_y="8",
            ),
            height="calc(100vh - 180px)",
        ),
        
        footer(),
        min_height="100vh",
        bg="var(--gray-1)",  
    )
app = rx.App()
app.add_page(index)
app.add_page(about)
app.add_page(contact)