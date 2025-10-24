import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample menu items with images
menu_items = [
    {
        "id": "1",
        "name": "Butter Chicken",
        "description": "Tender chicken pieces in a rich, creamy tomato-based sauce with aromatic spices",
        "price": 16.99,
        "category": "Main Course",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe",
        "featured": True
    },
    {
        "id": "2",
        "name": "Chicken Biryani",
        "description": "Fragrant basmati rice layered with spiced chicken, herbs, and saffron",
        "price": 18.99,
        "category": "Main Course",
        "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
        "featured": True
    },
    {
        "id": "3",
        "name": "South Indian Thali",
        "description": "Traditional platter with variety of curries, rice, sambar, and dessert",
        "price": 22.99,
        "category": "Main Course",
        "image": "https://images.unsplash.com/photo-1625398407796-82650a8c135f",
        "featured": True
    },
    {
        "id": "4",
        "name": "Gulab Jamun",
        "description": "Sweet milk dumplings soaked in rose-flavored sugar syrup",
        "price": 6.99,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969",
        "featured": False
    },
    {
        "id": "5",
        "name": "Paneer Tikka Masala",
        "description": "Grilled cottage cheese cubes in spiced curry sauce",
        "price": 14.99,
        "category": "Main Course",
        "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg",
        "featured": True
    },
    {
        "id": "6",
        "name": "Samosa Platter",
        "description": "Crispy pastry triangles filled with spiced potatoes and peas",
        "price": 7.99,
        "category": "Starters",
        "image": "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg",
        "featured": False
    },
    {
        "id": "7",
        "name": "Dal Makhani",
        "description": "Creamy black lentils slow-cooked with butter and cream",
        "price": 12.99,
        "category": "Main Course",
        "image": "https://images.unsplash.com/photo-1618449840665-9ed506d73a34",
        "featured": False
    },
    {
        "id": "8",
        "name": "Lamb Rogan Josh",
        "description": "Tender lamb cooked in aromatic Kashmiri spices",
        "price": 19.99,
        "category": "Main Course",
        "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc",
        "featured": True
    },
    {
        "id": "9",
        "name": "Chicken Tikka",
        "description": "Marinated chicken pieces grilled to perfection",
        "price": 13.99,
        "category": "Starters",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe",
        "featured": False
    },
    {
        "id": "10",
        "name": "Masala Dosa",
        "description": "Crispy rice crepe filled with spiced potato filling",
        "price": 11.99,
        "category": "Starters",
        "image": "https://images.unsplash.com/photo-1625398407796-82650a8c135f",
        "featured": False
    },
    {
        "id": "11",
        "name": "Mango Lassi",
        "description": "Refreshing yogurt drink blended with sweet mangoes",
        "price": 5.99,
        "category": "Drinks",
        "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969",
        "featured": False
    },
    {
        "id": "12",
        "name": "Naan Bread Basket",
        "description": "Assortment of freshly baked naan breads",
        "price": 6.99,
        "category": "Starters",
        "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg",
        "featured": False
    }
]

# Testimonials
testimonials = [
    {
        "id": "1",
        "name": "Sarah Johnson",
        "rating": 5,
        "comment": "Absolutely amazing food! The butter chicken was the best I've ever had. The ambiance by the lakeside is perfect for a romantic dinner.",
        "image": "https://ui-avatars.com/api/?name=Sarah+Johnson&background=DC2626&color=fff"
    },
    {
        "id": "2",
        "name": "Michael Chen",
        "rating": 5,
        "comment": "Authentic Indian cuisine with a modern twist. The service was impeccable and the presentation of dishes was stunning.",
        "image": "https://ui-avatars.com/api/?name=Michael+Chen&background=DC2626&color=fff"
    },
    {
        "id": "3",
        "name": "Priya Patel",
        "rating": 5,
        "comment": "Being from India, I can say this is truly authentic! The spices are perfectly balanced and the lakeside view adds to the experience.",
        "image": "https://ui-avatars.com/api/?name=Priya+Patel&background=DC2626&color=fff"
    },
    {
        "id": "4",
        "name": "James Wilson",
        "rating": 5,
        "comment": "The biryani was exceptional! Every grain of rice was perfectly cooked. Will definitely be coming back with family.",
        "image": "https://ui-avatars.com/api/?name=James+Wilson&background=DC2626&color=fff"
    },
    {
        "id": "5",
        "name": "Emma Davis",
        "rating": 5,
        "comment": "Great vegetarian options! The paneer tikka masala was divine. Highly recommend for both vegetarians and non-vegetarians.",
        "image": "https://ui-avatars.com/api/?name=Emma+Davis&background=DC2626&color=fff"
    }
]

# Gallery images
gallery_images = [
    {
        "id": "1",
        "url": "https://images.unsplash.com/photo-1667388969250-1c7220bf3f37",
        "title": "Restaurant Interior",
        "description": "Elegant dining atmosphere"
    },
    {
        "id": "2",
        "url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
        "title": "Modern Ambiance",
        "description": "Contemporary restaurant design"
    },
    {
        "id": "3",
        "url": "https://images.unsplash.com/photo-1729394405518-eaf2a0203aa7",
        "title": "Dining Area",
        "description": "Spacious seating arrangement"
    },
    {
        "id": "4",
        "url": "https://images.unsplash.com/photo-1516100882582-96c3a05fe590",
        "title": "Gourmet Plating",
        "description": "Artistic food presentation"
    },
    {
        "id": "5",
        "url": "https://images.unsplash.com/photo-1514326640560-7d063ef2aed5",
        "title": "Fine Dining",
        "description": "Premium dish presentation"
    },
    {
        "id": "6",
        "url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0",
        "title": "Culinary Excellence",
        "description": "Restaurant quality plating"
    }
]

async def seed_database():
    print("Seeding database...")
    
    # Clear existing data
    await db.menu_items.delete_many({})
    await db.testimonials.delete_many({})
    await db.gallery_images.delete_many({})
    
    # Insert menu items
    await db.menu_items.insert_many(menu_items)
    print(f"Inserted {len(menu_items)} menu items")
    
    # Insert testimonials
    await db.testimonials.insert_many(testimonials)
    print(f"Inserted {len(testimonials)} testimonials")
    
    # Insert gallery images
    await db.gallery_images.insert_many(gallery_images)
    print(f"Inserted {len(gallery_images)} gallery images")
    
    print("Database seeded successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
