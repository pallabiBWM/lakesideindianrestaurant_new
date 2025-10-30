import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

async def update_takeaway_menu():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🔄 Deleting existing takeaway menu items...")
    # Delete all existing takeaway menu items
    result = await db.menu_items.delete_many({"menu_type": "takeaway"})
    print(f"✅ Deleted {result.deleted_count} existing takeaway menu items")
    
    print("\n📝 Adding new takeaway menu items...")
    
    # New takeaway menu items from the PDF
    takeaway_items = [
        # FRIED ENTREE
        {"name": "Veg Samosa (2pcs)", "description": "Tasty triangles of mildly spiced mashed potatoes and vegetables wrapped in a crispy home-made pastry served with fresh tamarind chutney", "price": 9.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Onion Bhaji (4pcs)", "description": "Thinly sliced onions mixed with chickpea flour, fresh herbs and spices, golden fried served with tamarind sauce", "price": 11.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Chicken Pakora (4pcs)", "description": "Tender chicken pieces marinated in our traditional spice blend, dipped in chickpea flour and deep-fried until golden and served with mint sauce", "price": 15.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Veg Manchurian", "description": "Indian Chinese appetizer where crisp fried vegetable balls are dunked in slightly sweet and homemade Manchurian sauce", "price": 17.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Fish Pakora (4pcs)", "description": "Fresh fish fillets gently marinated with herbs and spices, coated in a chickpea batter and fried to perfection", "price": 18.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Meat Samosa (2pcs)", "description": "Handmade pastry triangles filled with spiced beef mince and fresh herbs, deep-fried until crisp and served with mint sauce", "price": 11.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Vegetable Pakora (4pcs)", "description": "Fresh vegetables & spices delicately coated in chickpea batter & golden fried served with fresh tamarind chutney", "price": 12.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Prawn Pakora (6pcs)", "description": "Fresh prawns marinated with our traditional spice blend, dipped in chickpea flour, deep-fried until golden and served with mint sauce", "price": 17.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Samosa Chaat", "description": "Classic Indian Street food samosa topped with onion, chickpeas, mixed chutney, topped with coriander and filled with mouth-watering spices", "price": 13.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Paneer Pakora (4pcs)", "description": "Homemade cottage cheese stuffed with garlic, mint, potatoes dipped in chickpea batter, deep fired and served with tamarind sauce", "price": 13.99, "category": "Fried Entree", "menu_type": "takeaway"},
        {"name": "Aloo Tikki Chaat", "description": "A crispy homemade potato patty flavoured with spices, topped with chickpeas, yogurt and homemade chutneys", "price": 13.99, "category": "Fried Entree", "menu_type": "takeaway"},
        
        # TANDOORI STARTER
        {"name": "Tandoori Tikka (4 pieces)", "description": "Yogurt-marinated boneless chicken from the tandoor, served with mint sauce", "price": 17.99, "category": "Tandoori Starter", "menu_type": "takeaway"},
        {"name": "Malai Tikka (4 pieces)", "description": "Creamy, boneless chicken fillets from the tandoor, served with mint sauce", "price": 18.99, "category": "Tandoori Starter", "menu_type": "takeaway"},
        {"name": "Tandoori Prawns (6 pieces)", "description": "Prawns cooked with mild spices & marinated with yoghurt & cooked in tandoor (clay oven) served with fresh mint sauce", "price": 18.99, "category": "Tandoori Starter", "menu_type": "takeaway"},
        
        # INDO CHINESE
        {"name": "Chennai Chilli Fish", "description": "Tender fish pieces, deep fried and cooked with capsicum and onions, with our homemade sauce", "price": 24.99, "category": "Indo Chinese", "menu_type": "takeaway"},
        {"name": "Chilli Chicken", "description": "Tender chicken pieces, deep fried and cooked with capsicum and onions, with our homemade sauce", "price": 23.99, "category": "Indo Chinese", "menu_type": "takeaway"},
        {"name": "Chilli Prawns", "description": "Prawns cooked with capsicums and onions, with our homemade sauce", "price": 24.99, "category": "Indo Chinese", "menu_type": "takeaway"},
        {"name": "Chilli Paneer", "description": "Homemade cottage cheese stir-fried with capsicum, onions, and our signature sauce", "price": 21.00, "category": "Indo Chinese", "menu_type": "takeaway"},
        
        # VEGETARIAN CURRIES
        {"name": "Yellow Daal", "description": "Yellow lentils slow-cooked with Indian herbs and spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Dal Makhni", "description": "Black lentils and red kidney beans cooked in Indian gravy, fresh cream, selected herbs and spices and tempered with butter", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Sabji Jalfrezi", "description": "Pan fired veggies cooked in coconut & mild creamy sauce with capsicum & onions", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Saag Aloo", "description": "Spinach and potatoes cooked in a fresh curry sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Aloo Gobhi", "description": "Fresh cauliflower and potatoes cooked in chef's special herbs and spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Palak Paneer", "description": "Fresh leafy spinach with home made cottage cheese", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Shahi Paneer", "description": "Cottage cheese cooked with ginger, garlic, herbs & spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Malai Kofta", "description": "Home-made cottage cheese & potato dumplings cooked in a rich creamy sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Chana Masala", "description": "An Aromatic Indian chickpea curry, simmered in tomato-onion gravy with Indian herbs and spices", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Paneer Butter Masala", "description": "An all-time favourite paneer cubes cooked in clay oven simmered in rich creamy tomato sauce with capsicum & onion", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Mixed Vegetables", "description": "Fresh seasonal vegetables in an onion and tomato sauce, with ginger, garlic, and roasted cumin", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Kadhai Paneer", "description": "Cubes of homemade cottage cheese cooked with fresh onions, herbs, & mild aromatic spices in traditional Indian Kadhai style", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Butter Paneer", "description": "Cubes of homemade cottage cheese cooked with creamy tomato-based sauce, mild spices and butter", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Vegetable Madras", "description": "A flavorful vegetable curry with mustard seeds, curry leaves, and a creamy coconut finish", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        {"name": "Vegetable Korma", "description": "Fresh vegetables cooked with exotic herbs and spices, cashews in mild cream sauce", "price": 21.00, "category": "Vegetarian Curries", "menu_type": "takeaway"},
        
        # CHICKEN
        {"name": "Butter Chicken", "description": "Tender boneless pieces of chicken cooked with creamy tomato-based sauce, mild spices and butter", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Mango Chicken", "description": "Tender chicken prepared with mild spices with mango pulp & cream", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Korma", "description": "Chicken cooked with exotic spices and herbs, in mild cream sauce", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Jalfrezi", "description": "Pan fired chicken pieces cooked in coconut & mild creamy sauce with capsicum & onion", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Rogan Josh", "description": "Tender chicken simmered in a rich, slow-cooked blend of onions, tomatoes, mild aromatic spices, and herbs, creating a deep and flavourful curry", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Tikka Masala", "description": "Marinated chicken pieces, partially cooked in a clay oven with capsicum and onion, then finished in our chef's famous creamy tikka sauce", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Punjabi Chicken", "description": "Chicken cooked with fresh onions, herbs, and mild aromatic spices in traditional Indian Kadhai style", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Madras", "description": "Chicken cooked in a blend of 7 spices, bursts of mustard seeds, curry leaves and coconut cream", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Vindaloo", "description": "Chicken pieces cooked in hot, spicy Goan curry made with authentic herbs & spices", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        {"name": "Chicken Saag", "description": "A famous north Indian dish cooked with English spinach with a special blend of our chef's special herbs & spices", "price": 23.99, "category": "Chicken", "menu_type": "takeaway"},
        
        # BEEF
        {"name": "Beef Korma", "description": "Beef cooked with exotic spices & herbs in mild cream sauce", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef do Pyaza", "description": "Beef pieces cooked in a thick, dry-style gravy with lots of onions and a tasty mix of spices and herbs", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Kadhai Beef", "description": "Beef cooked with fresh onions, herbs, and mild aromatic spices in traditional Indian Kadhai style", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Aloo", "description": "Tender beef and soft potatoes gently cooked in a home-style curry with herbs and spices", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Madras", "description": "Beef cooked in a blend of 7 spices, bursts of mustard seeds, curry leaves and coconut cream", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Vindaloo", "description": "Beef pieces cooked in hot, spicy Goan curry made with authentic herbs & spices", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Jalfrezi", "description": "Pan fired beef pieces cooked in coconut & mild creamy sauce with capsicum & onion", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Saag", "description": "A famous north Indian dish cooked with English spinach with a special blend of our chef's special herbs & spices", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Masala", "description": "Tender Beef pieces, cooked with capsicum and onion, then finished in our chef's famous creamy sauce", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        {"name": "Beef Rogan Josh", "description": "Tender beef slow-cooked in a rich blend of onions, tomatoes, and mild aromatic spices", "price": 23.99, "category": "Beef", "menu_type": "takeaway"},
        
        # LAMB
        {"name": "Lamb Korma", "description": "Tender lamb in a mild, creamy sauce with exotic spices", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Rogan Josh", "description": "Tender lamb simmered in a rich, slow-cooked blend of onions, tomatoes, mild aromatic spices, and herbs, creating a deep and flavourful curry", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Aloo", "description": "Tender Lamb and soft potatoes gently cooked in a home-style curry with herbs and spices", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Saag", "description": "A famous north Indian dish cooked with English spinach with a special blend of our chef's special herbs & spices", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Do Pyaza", "description": "Lamb pieces cooked in a thick, dry-style gravy with lots of onions and a tasty mix of spices and herbs", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Madras", "description": "Lamb cooked in a blend of 7 spices, bursts of mustard seeds, curry leaves and coconut cream", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Vindaloo", "description": "Lamb pieces cooked in hot, spicy Goan curry made with authentic herbs & spices", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Kadhai Lamb", "description": "Lamb cooked with fresh onions, herbs, and mild aromatic spices in traditional Indian Kadhai style", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Jalfrezi", "description": "Pan fired lamb pieces cooked in coconut & mild creamy sauce with capsicum & onion", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Lamb Masala", "description": "Tender lamb pieces, cooked with capsicum and onion, then finished in our chef's famous creamy sauce", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        {"name": "Goat Curry (with bones)", "description": "North Indian dish cooked with chef's homemade blend of herbs and spices", "price": 23.99, "category": "Lamb", "menu_type": "takeaway"},
        
        # SEA FOOD
        {"name": "Fish Korma", "description": "Fish in a mild, creamy sauce with exotic spices", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        {"name": "Fish Masala", "description": "Fresh fish pieces, cooked with capsicum and onion, then finished in our chef's famous creamy sauce", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        {"name": "Goa Fish Curry", "description": "Fresh fillets cooked in a flavourful curry sauce finished with a touch of coconut", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        {"name": "Fish Vindaloo", "description": "Fish pieces cooked in hot, spicy Goan curry made with authentic herbs & spices", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        {"name": "Saag Prawns", "description": "A famous North Indian dish cooked with English spinach and a special blend of herbs and spices", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        {"name": "Prawn Masala", "description": "Fresh prawns, cooked with capsicum and onion, then finished in our chef's famous creamy sauce", "price": 24.99, "category": "Sea Food", "menu_type": "takeaway"},
        
        # BIRYANI
        {"name": "Chicken Biryani", "description": "Fragrant rice dish made with basmati rice, tender chicken, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        {"name": "Lamb Biryani", "description": "Fragrant rice dish made with basmati rice, tender lamb, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        {"name": "Beef Biryani", "description": "Fragrant rice dish made with basmati rice, tender beef, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        {"name": "Goat Biryani (with bones)", "description": "Fragrant rice dish made with basmati rice, tender goat with bones, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        {"name": "Vegetable Biryani", "description": "Fragrant rice dish made with basmati rice, fresh vegetables, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        {"name": "Prawn Biryani", "description": "Fragrant rice dish made with basmati rice, tender prawns, and a blend of aromatic spices, slow-cooked to perfection", "price": 25.99, "category": "Biryani", "menu_type": "takeaway"},
        
        # RICE
        {"name": "Basmati Rice", "description": "Steamed basmati rice", "price": 5.50, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Saffron Rice", "description": "Basmati rice with Saffron", "price": 5.90, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Pulao Rice", "description": "Rice cooked with cumin seeds and peas", "price": 6.99, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Vegetable Fried Rice", "description": "Fried rice cooked with fresh vegetables", "price": 15.99, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Potato Onion Rice", "description": "Basmati rice cooked with caramelised onion and herbed sliced potatoes", "price": 7.99, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Coconut Rice", "description": "Rice cooked with desiccated coconut", "price": 6.99, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Jeera Rice", "description": "Rice cooked with cumin seeds", "price": 8.99, "category": "Rice", "menu_type": "takeaway"},
        {"name": "Kashmiri Rice", "description": "Basmati Rice sauted with sweet dry fruits, nuts and creamy sauce", "price": 8.99, "category": "Rice", "menu_type": "takeaway"},
        
        # BREAD
        {"name": "Roti / Butter Roti", "description": "Wholemeal Bread", "price": 4.50, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Tandoori Roti", "description": "Wholemeal Bread from our clay oven", "price": 5.00, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Cheese Naan", "description": "Naan stuffed with cheese", "price": 6.99, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Plain Naan", "description": "Leavened bread cooked in tandoor", "price": 5.90, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Garlic Naan", "description": "Naan bread with a touch of garlic", "price": 6.10, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Peshwari Naan", "description": "Naan made with dried fruits", "price": 7.00, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Butter Naan", "description": "Plain naan topped with butter", "price": 6.00, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Chef's Special Chilli Naan", "description": "Naan stuffed with potatoes, cheese, onions, hot spices & chilli Cheese", "price": 7.95, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Cheese & Garlic Naan", "description": "Filled with cheese & touch of garlic", "price": 7.95, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Herb & Garlic Naan", "description": "Naan with touch of garlic and herbs", "price": 6.50, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Keema and Cheese Naan", "description": "Naan stuffed with minced lamb and cheese", "price": 7.50, "category": "Bread", "menu_type": "takeaway"},
        {"name": "Cheese and Spinach Naan", "description": "Stuffed with cheese & spinach", "price": 7.50, "category": "Bread", "menu_type": "takeaway"},
        
        # SIDE DISHES
        {"name": "Cucumber Raita", "description": "A refreshing Indian side of yogurt blended with cucumbers and spices", "price": 5.50, "category": "Side Dishes", "menu_type": "takeaway"},
        {"name": "Mango Chutney", "description": "Sweet mango chutney", "price": 4.00, "category": "Side Dishes", "menu_type": "takeaway"},
        {"name": "Mixed Pickles", "description": "Indian mixed pickles", "price": 4.00, "category": "Side Dishes", "menu_type": "takeaway"},
        {"name": "Papadums (4Pcs)", "description": "Crispy papadums", "price": 4.00, "category": "Side Dishes", "menu_type": "takeaway"},
        {"name": "Hot Mint Chutney", "description": "Spicy mint chutney", "price": 4.00, "category": "Side Dishes", "menu_type": "takeaway"},
        {"name": "Indian Salad", "description": "Tomato, Cucumber and Onions", "price": 9.00, "category": "Side Dishes", "menu_type": "takeaway"},
        
        # DRINKS
        {"name": "Mango Lassi", "description": "A smoothie blended with yogurt and mango", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Sweet Lassi", "description": "Sweet yogurt drink", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Salty Lassi", "description": "Salty yogurt drink", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Soft Drinks", "description": "Coke/Coke 0/Lemonade/Lemon Squash", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Juice", "description": "Apple / Orange / Pineapple", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Indian Masala Tea", "description": "Traditional Indian spiced tea", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Lemon Lime Bitter", "description": "Refreshing lemon lime bitter", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Ginger Beer", "description": "Ginger beer", "price": 6.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Ginger Ale", "description": "Ginger ale", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Soda Water", "description": "Soda water", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Sparkling Water", "description": "Sparkling water", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Spring Water", "description": "Spring water", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        {"name": "Tonic Water", "description": "Tonic water", "price": 5.00, "category": "Drinks", "menu_type": "takeaway"},
        
        # DESSERTS
        {"name": "Gulab Jamun (2pcs)", "description": "Sweet dumpling, fried and soaked in rose flavoured sugar syrup", "price": 9.00, "category": "Desserts", "menu_type": "takeaway"},
        {"name": "Plain Ice Cream", "description": "Vanilla ice cream", "price": 7.99, "category": "Desserts", "menu_type": "takeaway"},
        {"name": "Pista Kulfi", "description": "Homemade Indian style ice cream made with pistachios", "price": 9.99, "category": "Desserts", "menu_type": "takeaway"},
        {"name": "Gulab Jamun with Ice Cream", "description": "2 pieces of Gulab Jamun Served with plain ice-cream", "price": 11.99, "category": "Desserts", "menu_type": "takeaway"},
        {"name": "Moong Dal Halwa", "description": "Sweet Indian Dessert made from yellow lentils, butter and sugar", "price": 12.00, "category": "Desserts", "menu_type": "takeaway"},
        
        # KIDS MENU
        {"name": "Fish and Chips", "description": "Kids portion of fish and chips", "price": 11.99, "category": "Kids Menu", "menu_type": "takeaway"},
        {"name": "Chicken Nuggets and Chips", "description": "Kids portion of chicken nuggets and chips", "price": 11.99, "category": "Kids Menu", "menu_type": "takeaway"},
        {"name": "Butter Chicken with Rice (Kids)", "description": "Small portion of butter chicken & rice, mild and sweet flavour", "price": 13.99, "category": "Kids Menu", "menu_type": "takeaway"},
        {"name": "Mango Chicken with Rice (Kids)", "description": "Small portion of mango chicken & rice, mild and sweet flavour", "price": 13.99, "category": "Kids Menu", "menu_type": "takeaway"},
        {"name": "Bowl of Chips", "description": "Kids portion of chips", "price": 8.99, "category": "Kids Menu", "menu_type": "takeaway"},
    ]
    
    # Add IDs to each item
    for item in takeaway_items:
        item['id'] = str(uuid.uuid4())
    
    # Insert all items
    result = await db.menu_items.insert_many(takeaway_items)
    print(f"✅ Added {len(result.inserted_ids)} new takeaway menu items")
    
    print("\n📊 Summary by category:")
    categories = {}
    for item in takeaway_items:
        cat = item['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count} items")
    
    print("\n✨ Takeaway menu update complete!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_takeaway_menu())
