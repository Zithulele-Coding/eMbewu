from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from eMbewu import Base, DBProduct  # Import your models

# Database connection
DATABASE_URL = "postgresql://coffeedb_owner:JEvnWBFp67xV@ep-still-flower-a54nulqa.us-east-2.aws.neon.tech/coffeedb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_database():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    
    # Sample products
    products = [
    {
        "title": "Ethiopian Coffee",
        "price": 159.99,
        "description": "Premium Ethiopian coffee beans, medium roast with fruity notes and floral undertones. Perfect for pour-over brewing.",
        "image": "/coffee1.jpg",
        "rating": {"rate": 4.8, "count": 120}
    },
    {
        "title": "Colombian Coffee",
        "price": 149.99,
        "description": "Single-origin Colombian coffee, dark roast with rich chocolate notes and caramel sweetness. Ideal for espresso.",
        "image": "/coffee2.jpg",
        "rating": {"rate": 4.6, "count": 95}
    },
    {
        "title": "Brazilian Santos",
        "price": 139.99,
        "description": "Smooth Brazilian Santos beans, medium roast featuring nutty flavors and a subtle citrus finish. Great for everyday brewing.",
        "image": "/coffee3.jpg",
        "rating": {"rate": 4.7, "count": 108}
    },
    {
        "title": "Kenyan AA",
        "price": 169.99,
        "description": "Premium Kenyan AA beans, medium-light roast with bright acidity and wine-like characteristics. Perfect for cold brew.",
        "image": "/coffee4.jpg",
        "rating": {"rate": 4.9, "count": 85}
    },
    {
        "title": "Guatemala Antigua",
        "price": 154.99,
        "description": "Guatemala Antigua coffee, medium roast with complex spicy and smoky notes. Excellent for French press.",
        "image": "/coffee5.jpg",
        "rating": {"rate": 4.5, "count": 75}
    },
    {
        "title": "Costa Rican Tarrazu",
        "price": 144.99,
        "description": "Costa Rican Tarrazu beans, medium roast with honey sweetness and bright citrus notes. Great for drip coffee.",
        "image": "/coffee6.jpg",
        "rating": {"rate": 4.7, "count": 92}
    },
    {
        "title": "Sumatra Mandheling",
        "price": 164.99,
        "description": "Indonesian Sumatra Mandheling, dark roast with earthy, full-bodied flavor and low acidity. Perfect for espresso blends.",
        "image": "/coffee7.jpg",
        "rating": {"rate": 4.6, "count": 88}
    },
        {
        "title": "Yemen Mocha",
        "price": 179.99,
        "description": "Rare Yemen Mocha beans, light roast with distinctive wine and berry notes. A premium coffee experience.",
        "image": "/coffee8.jpg",
        "rating": {"rate": 4.8, "count": 65}
    }
    ]

    for product_data in products:
        product = DBProduct(**product_data)
        session.add(product)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    seed_database()