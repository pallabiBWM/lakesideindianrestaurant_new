import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from auth import get_password_hash

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def init_admin_user():
    """Initialize admin user"""
    print("Initializing admin user...")
    
    # Check if admin already exists
    existing_admin = await db.admin_users.find_one({"username": "admin"})
    
    if existing_admin:
        print("Admin user already exists")
    else:
        admin_user = {
            "id": "admin-1",
            "username": "admin",
            "password_hash": get_password_hash("admin123"),
            "email": "pallabi.dipa@gmail.com"
        }
        await db.admin_users.insert_one(admin_user)
        print("✅ Admin user created (username: admin, password: admin123)")
    
    # Initialize settings
    settings = {
        "id": "settings",
        "admin_email": "pallabi.dipa@gmail.com",
        "restaurant_name": "Lakeside Indian Restaurant",
        "restaurant_phone": "+61 3 9749 3400",
        "restaurant_address": "53 Morang Road, Hawthorn VIC 3122",
        "opening_hours": {
            "monday_thursday": "5:00 PM - 10:00 PM",
            "friday_saturday": "5:00 PM - 10:30 PM",
            "sunday": "5:00 PM - 10:00 PM"
        }
    }
    await db.admin_settings.update_one(
        {"id": "settings"},
        {"$set": settings},
        upsert=True
    )
    print("✅ Admin settings initialized")

async def clear_and_populate_menus():
    """Clear existing menu and populate with PDF data"""
    print("Clearing existing menu items...")
    await db.menu_items.delete_many({})
    
    print("Populating menus from PDFs...")
    
    # DINE-IN MENU ITEMS
    dinein_items = []
    
    # Tandoori Starters - Dine-in
    dinein_items.extend([
        {"id": "d1", "name": "Tandoori Tikka (4 pieces)", "description": "Yogurt-marinated boneless chicken from the tandoor, served with mint sauce", "price": 17.99, "category": "Tandoori Starter", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": True},
        {"id": "d2", "name": "Malai Tikka (4 pieces)", "description": "Creamy, boneless chicken fillets from the tandoor, served with mint sauce", "price": 18.99, "category": "Tandoori Starter", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d3", "name": "Tandoori Prawns (6 pieces)", "description": "Prawns cooked with mild spices & marinated with yoghurt & cooked in tandoor", "price": 18.99, "category": "Tandoori Starter", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641", "featured": False},
    ])
    
    # Fried Entrees - Dine-in
    dinein_items.extend([
        {"id": "d4", "name": "Veg Samosa (2pcs)", "description": "Tasty triangles of mildly spiced mashed potatoes and vegetables", "price": 9.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg", "featured": False},
        {"id": "d5", "name": "Onion Bhaji (4pcs)", "description": "Thinly sliced onions mixed with chickpea flour, golden fried", "price": 11.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950", "featured": False},
        {"id": "d6", "name": "Chicken Pakora (4pcs)", "description": "Tender chicken pieces marinated in spice blend, deep-fried", "price": 15.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84", "featured": False},
        {"id": "d7", "name": "Fish Pakora (4pcs)", "description": "Fresh fish fillets coated in chickpea batter and fried", "price": 18.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
        {"id": "d8", "name": "Meat Samosa (2pcs)", "description": "Pastry triangles filled with spiced beef mince", "price": 11.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950", "featured": False},
        {"id": "d9", "name": "Vegetable Pakora (4pcs)", "description": "Fresh vegetables coated in chickpea batter & golden fried", "price": 12.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950", "featured": False},
        {"id": "d10", "name": "Prawn Pakora (6pcs)", "description": "Fresh prawns dipped in chickpea flour, deep-fried", "price": 17.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641", "featured": False},
        {"id": "d11", "name": "Paneer Pakora (4pcs)", "description": "Cottage cheese stuffed with garlic, mint, potatoes", "price": 13.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d12", "name": "Samosa Chaat", "description": "Samosa topped with onion, chickpeas, mixed chutney", "price": 13.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950", "featured": False},
        {"id": "d13", "name": "Aloo Tikki Chaat", "description": "Crispy potato patty with chickpeas, yogurt and chutneys", "price": 13.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950", "featured": False},
        {"id": "d14", "name": "Veg Manchurian", "description": "Crisp fried vegetable balls in Manchurian sauce", "price": 17.99, "category": "Fried Entree", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
    ])
    
    # Indo Chinese - Dine-in
    dinein_items.extend([
        {"id": "d15", "name": "Chilli Chicken", "description": "Tender chicken, deep fried with capsicum and onions", "price": 23.99, "category": "Indo Chinese", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": True},
        {"id": "d16", "name": "Chilli Prawns", "description": "Prawns cooked with capsicums and onions", "price": 24.99, "category": "Indo Chinese", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641", "featured": False},
        {"id": "d17", "name": "Chilli Paneer", "description": "Cottage cheese stir-fried with capsicum and onions", "price": 21.00, "category": "Indo Chinese", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d18", "name": "Chennai Chilli Fish", "description": "Tender fish pieces with capsicum and onions", "price": 24.99, "category": "Indo Chinese", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
    ])
    
    # Chicken - Dine-in
    dinein_items.extend([
        {"id": "d19", "name": "Butter Chicken", "description": "Tender boneless chicken in creamy tomato-based sauce", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe", "featured": True},
        {"id": "d20", "name": "Mango Chicken", "description": "Tender chicken with mild spices, mango pulp & cream", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d21", "name": "Chicken Korma", "description": "Chicken with exotic spices in mild cream sauce", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d22", "name": "Chicken Jalfrezi", "description": "Pan fired chicken in coconut & mild creamy sauce", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d23", "name": "Chicken Rogan Josh", "description": "Tender chicken in rich blend of aromatic spices", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d24", "name": "Chicken Tikka Masala", "description": "Marinated chicken in chef's famous creamy tikka sauce", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": True},
        {"id": "d25", "name": "Punjabi Chicken", "description": "Chicken in traditional Indian Kadhai style", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d26", "name": "Chicken Madras", "description": "Chicken in blend of 7 spices with coconut cream", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d27", "name": "Chicken Vindaloo", "description": "Chicken in hot, spicy Goan curry", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d28", "name": "Chicken Saag", "description": "Chicken with English spinach and special herbs", "price": 23.99, "category": "Chicken", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
    ])
    
    # Beef - Dine-in
    dinein_items.extend([
        {"id": "d29", "name": "Beef Korma", "description": "Beef with exotic spices in mild cream sauce", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d30", "name": "Beef do Pyaza", "description": "Beef in thick, dry-style gravy with onions", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d31", "name": "Kadhai Beef", "description": "Beef in traditional Indian Kadhai style", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d32", "name": "Beef Aloo", "description": "Tender beef and soft potatoes in home-style curry", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d33", "name": "Beef Madras", "description": "Beef in blend of 7 spices with coconut cream", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d34", "name": "Beef Vindaloo", "description": "Beef in hot, spicy Goan curry", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d35", "name": "Beef Jalfrezi", "description": "Pan fired beef in coconut & mild creamy sauce", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d36", "name": "Beef Saag", "description": "Beef with English spinach and special herbs", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d37", "name": "Beef Masala", "description": "Tender beef in chef's famous creamy sauce", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2", "featured": False},
        {"id": "d38", "name": "Beef Rogan Josh", "description": "Tender beef slow-cooked with aromatic spices", "price": 23.99, "category": "Beef", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
    ])
    
    # Lamb - Dine-in
    dinein_items.extend([
        {"id": "d39", "name": "Lamb Korma", "description": "Tender lamb in mild, creamy sauce", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": True},
        {"id": "d40", "name": "Lamb Rogan Josh", "description": "Tender lamb in rich aromatic spices", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d41", "name": "Lamb Aloo", "description": "Tender lamb and potatoes in home-style curry", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d42", "name": "Lamb Saag", "description": "Lamb with English spinach and special herbs", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d43", "name": "Lamb Do Pyaza", "description": "Lamb in thick gravy with lots of onions", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d44", "name": "Lamb Madras", "description": "Lamb in blend of 7 spices with coconut cream", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d45", "name": "Lamb Vindaloo", "description": "Lamb in hot, spicy Goan curry", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d46", "name": "Kadhai Lamb", "description": "Lamb in traditional Indian Kadhai style", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d47", "name": "Lamb Jalfrezi", "description": "Pan fired lamb in coconut & mild creamy sauce", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d48", "name": "Lamb Masala", "description": "Tender lamb in chef's famous creamy sauce", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
        {"id": "d49", "name": "Goat Curry (with bones)", "description": "Goat cooked with chef's homemade blend", "price": 23.99, "category": "Lamb", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1627366422957-3efa9c6df0fc", "featured": False},
    ])
    
    # Continue in next part...
    print(f"Added {len(dinein_items)} dine-in menu items (part 1)")
    await db.menu_items.insert_many(dinein_items)

async def populate_remaining_dinein_items():
    """Continue populating dine-in menu items"""
    dinein_items_part2 = []
    
    # Seafood - Dine-in
    dinein_items_part2.extend([
        {"id": "d50", "name": "Fish Korma", "description": "Fish in mild, creamy sauce with exotic spices", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
        {"id": "d51", "name": "Fish Masala", "description": "Fresh fish in chef's famous creamy sauce", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
        {"id": "d52", "name": "Goa Fish Curry", "description": "Fresh fillets in flavourful curry with coconut", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": True},
        {"id": "d53", "name": "Fish Vindaloo", "description": "Fish in hot, spicy Goan curry", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
        {"id": "d54", "name": "Saag Prawns", "description": "Prawns with English spinach and special herbs", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641", "featured": False},
        {"id": "d55", "name": "Prawn Masala", "description": "Fresh prawns in chef's famous creamy sauce", "price": 24.99, "category": "Seafood", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641", "featured": False},
    ])
    
    # Vegetarian Curries - Dine-in
    dinein_items_part2.extend([
        {"id": "d56", "name": "Yellow Daal", "description": "Yellow lentils slow-cooked with herbs and spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1618449840665-9ed506d73a34", "featured": False},
        {"id": "d57", "name": "Dal Makhni", "description": "Black lentils and kidney beans in creamy gravy", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1618449840665-9ed506d73a34", "featured": True},
        {"id": "d58", "name": "Sabji Jalfrezi", "description": "Pan fired veggies in coconut & mild creamy sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d59", "name": "Saag Aloo", "description": "Spinach and potatoes in fresh curry sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d60", "name": "Aloo Gobhi", "description": "Cauliflower and potatoes in special herbs", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d61", "name": "Palak Paneer", "description": "Fresh spinach with homemade cottage cheese", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": True},
        {"id": "d62", "name": "Shahi Paneer", "description": "Cottage cheese with ginger, garlic, herbs & spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d63", "name": "Malai Kofta", "description": "Cottage cheese & potato dumplings in creamy sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d64", "name": "Chana Masala", "description": "Aromatic chickpea curry with Indian spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d65", "name": "Paneer Butter Masala", "description": "Paneer cubes in rich creamy tomato sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": True},
        {"id": "d66", "name": "Mixed Vegetables", "description": "Fresh vegetables in onion and tomato sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d67", "name": "Kadhai Paneer", "description": "Cottage cheese in traditional Kadhai style", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d68", "name": "Butter Paneer", "description": "Cottage cheese in creamy tomato-based sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8", "featured": False},
        {"id": "d69", "name": "Vegetable Madras", "description": "Vegetable curry with coconut finish", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d70", "name": "Vegetable Korma", "description": "Fresh vegetables with cashews in cream sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
    ])
    
    # Rice - Dine-in
    dinein_items_part2.extend([
        {"id": "d71", "name": "Basmati Rice", "description": "Premium basmati rice", "price": 5.50, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d72", "name": "Saffron Rice", "description": "Basmati rice with saffron", "price": 5.90, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d73", "name": "Pulao Rice", "description": "Rice cooked with cumin seeds and peas", "price": 6.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d74", "name": "Vegetable Fried Rice", "description": "Fried rice with fresh vegetables", "price": 15.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d75", "name": "Coconut Rice", "description": "Rice cooked with desiccated coconut", "price": 6.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d76", "name": "Jeera Rice", "description": "Rice cooked with cumin seeds", "price": 8.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d77", "name": "Potato Onion Rice", "description": "Rice with caramelised onion and herbed potatoes", "price": 7.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d78", "name": "Kashmiri Rice", "description": "Basmati rice with sweet dry fruits and nuts", "price": 8.99, "category": "Rice", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
    ])
    
    # Biryani - Dine-in
    dinein_items_part2.extend([
        {"id": "d79", "name": "Chicken Biryani", "description": "Fragrant basmati rice with spiced chicken", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": True},
        {"id": "d80", "name": "Lamb Biryani", "description": "Fragrant basmati rice with tender lamb", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d81", "name": "Beef Biryani", "description": "Fragrant basmati rice with spiced beef", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d82", "name": "Goat Biryani", "description": "Fragrant basmati rice with goat (with bones)", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d83", "name": "Vegetable Biryani", "description": "Fragrant basmati rice with mixed vegetables", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
        {"id": "d84", "name": "Prawn Biryani", "description": "Fragrant basmati rice with prawns", "price": 25.99, "category": "Biryani", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0", "featured": False},
    ])
    
    # Breads - Dine-in
    dinein_items_part2.extend([
        {"id": "d85", "name": "Plain Naan", "description": "Leavened bread cooked in tandoor", "price": 5.90, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d86", "name": "Garlic Naan", "description": "Naan bread with touch of garlic", "price": 6.10, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": True},
        {"id": "d87", "name": "Butter Naan", "description": "Plain naan topped with butter", "price": 6.00, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d88", "name": "Cheese Naan", "description": "Naan stuffed with cheese", "price": 6.99, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d89", "name": "Cheese & Garlic Naan", "description": "Filled with cheese & touch of garlic", "price": 7.95, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d90", "name": "Peshwari Naan", "description": "Naan made with dried fruits", "price": 7.00, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d91", "name": "Herb & Garlic Naan", "description": "Naan with garlic and herbs", "price": 6.50, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d92", "name": "Keema and Cheese Naan", "description": "Naan stuffed with minced lamb and cheese", "price": 7.50, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d93", "name": "Cheese and Spinach Naan", "description": "Stuffed with cheese & spinach", "price": 7.50, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d94", "name": "Chef's Special Chilli Naan", "description": "Naan stuffed with potatoes, cheese, hot spices", "price": 7.95, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d95", "name": "Roti", "description": "Wholemeal bread", "price": 4.50, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
        {"id": "d96", "name": "Tandoori Roti", "description": "Wholemeal bread from clay oven", "price": 5.00, "category": "Breads", "menu_type": "dine-in", "image": "https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg", "featured": False},
    ])
    
    # Side Dishes - Dine-in
    dinein_items_part2.extend([
        {"id": "d97", "name": "Cucumber Raita", "description": "Refreshing yogurt with cucumbers and spices", "price": 5.50, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d98", "name": "Papadums (4Pcs)", "description": "Crispy lentil wafers", "price": 4.00, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d99", "name": "Mango Chutney", "description": "Sweet mango preserve", "price": 4.00, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d100", "name": "Mixed Pickles", "description": "Indian mixed pickles", "price": 4.00, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d101", "name": "Hot Mint Chutney", "description": "Spicy mint sauce", "price": 4.00, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
        {"id": "d102", "name": "Indian Salad", "description": "Tomato, cucumber and onions", "price": 9.00, "category": "Side Dishes", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1626804475297-41608ea09aeb", "featured": False},
    ])
    
    # Drinks - Dine-in
    dinein_items_part2.extend([
        {"id": "d103", "name": "Mango Lassi", "description": "Yogurt smoothie with mango", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d104", "name": "Sweet Lassi", "description": "Sweet yogurt drink", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d105", "name": "Salty Lassi", "description": "Salted yogurt drink", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d106", "name": "Soft Drinks", "description": "Coke/Coke Zero/Lemonade/Lemon Squash", "price": 5.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d107", "name": "Juice", "description": "Apple / Orange / Pineapple", "price": 5.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d108", "name": "Indian Masala Tea", "description": "Spiced Indian tea", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d109", "name": "Water", "description": "Soda/Sparkling/Spring/Tonic Water", "price": 5.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d110", "name": "Ginger Beer", "description": "Spicy ginger beverage", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d111", "name": "Ginger Ale", "description": "Sweet ginger beverage", "price": 5.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d112", "name": "Lemon Lime Bitter", "description": "Refreshing citrus drink", "price": 6.00, "category": "Drinks", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
    ])
    
    # Desserts - Dine-in
    dinein_items_part2.extend([
        {"id": "d113", "name": "Gulab Jamun (2pcs)", "description": "Sweet dumplings in rose syrup", "price": 9.00, "category": "Desserts", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": True},
        {"id": "d114", "name": "Plain Ice Cream", "description": "Classic vanilla ice cream", "price": 7.99, "category": "Desserts", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d115", "name": "Pista Kulfi", "description": "Homemade pistachio ice cream", "price": 9.99, "category": "Desserts", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d116", "name": "Gulab Jamun with Ice Cream", "description": "2 Gulab Jamun with ice cream", "price": 11.99, "category": "Desserts", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
        {"id": "d117", "name": "Moong Dal Halwa", "description": "Sweet dessert from yellow lentils", "price": 12.00, "category": "Desserts", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1517244683847-7456b63c5969", "featured": False},
    ])
    
    # Kids Menu - Dine-in
    dinein_items_part2.extend([
        {"id": "d118", "name": "Fish and Chips", "description": "Kids portion fish and chips", "price": 11.99, "category": "Kids Menu", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
        {"id": "d119", "name": "Chicken Nuggets and Chips", "description": "Kids chicken nuggets with chips", "price": 11.99, "category": "Kids Menu", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2fb3ee", "featured": False},
        {"id": "d120", "name": "Kids Curry with Rice", "description": "Butter Chicken or Mango Chicken with rice", "price": 13.99, "category": "Kids Menu", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe", "featured": False},
        {"id": "d121", "name": "Bowl of Chips", "description": "Kids portion chips", "price": 8.99, "category": "Kids Menu", "menu_type": "dine-in", "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0", "featured": False},
    ])
    
    print(f"Added {len(dinein_items_part2)} more dine-in menu items")
    await db.menu_items.insert_many(dinein_items_part2)

async def populate_takeaway_items():
    """Populate takeaway menu items - Same items as dine-in"""
    print("Populating takeaway menu (using same items as dine-in)...")
    
    # Get all dine-in items
    dinein_items = await db.menu_items.find({"menu_type": "dine-in"}, {"_id": 0}).to_list(1000)
    
    # Create takeaway versions
    takeaway_items = []
    for item in dinein_items:
        takeaway_item = item.copy()
        takeaway_item["id"] = "t" + item["id"][1:]  # Replace 'd' with 't'
        takeaway_item["menu_type"] = "takeaway"
        takeaway_items.append(takeaway_item)
    
    await db.menu_items.insert_many(takeaway_items)
    print(f"✅ Added {len(takeaway_items)} takeaway menu items")

async def main():
    print("=" * 60)
    print("INITIALIZING LAKESIDE INDIAN RESTAURANT")
    print("=" * 60)
    
    await init_admin_user()
    await clear_and_populate_menus()
    await populate_remaining_dinein_items()
    await populate_takeaway_items()
    
    print("\n" + "=" * 60)
    print("✅ INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\nAdmin Login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: pallabi.dipa@gmail.com")
    print("\nTotal menu items created:")
    total_count = await db.menu_items.count_documents({})
    dinein_count = await db.menu_items.count_documents({"menu_type": "dine-in"})
    takeaway_count = await db.menu_items.count_documents({"menu_type": "takeaway"})
    print(f"  Dine-in: {dinein_count}")
    print(f"  Takeaway: {takeaway_count}")
    print(f"  Total: {total_count}")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
