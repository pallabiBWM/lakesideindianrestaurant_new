from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ============= MODELS =============

# Menu Item Models
class MenuItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image: str
    featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image: str
    featured: bool = False

# Cart Models
class CartItem(BaseModel):
    menu_item_id: str
    quantity: int

class Cart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem]
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Wishlist Models
class Wishlist(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    menu_item_ids: List[str]
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Contact Form Models
class ContactForm(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContactFormCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str

# Reservation Form Models
class Reservation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    date: str
    time: str
    guests: int
    special_requests: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReservationCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    date: str
    time: str
    guests: int
    special_requests: Optional[str] = None

# Testimonial Models
class Testimonial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    rating: int
    comment: str
    image: Optional[str] = None

# Gallery Models
class GalleryImage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str
    title: str
    description: Optional[str] = None


# ============= ROUTES =============

@api_router.get("/")
async def root():
    return {"message": "Lakeside Indian Restaurant API"}

# Menu Routes
@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu_items(category: Optional[str] = None, featured: Optional[bool] = None):
    query = {}
    if category:
        query['category'] = category
    if featured is not None:
        query['featured'] = featured
    
    menu_items = await db.menu_items.find(query, {"_id": 0}).to_list(1000)
    
    for item in menu_items:
        if isinstance(item.get('created_at'), str):
            item['created_at'] = datetime.fromisoformat(item['created_at'])
    
    return menu_items

@api_router.get("/menu/{item_id}", response_model=MenuItem)
async def get_menu_item(item_id: str):
    item = await db.menu_items.find_one({"id": item_id}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    if isinstance(item.get('created_at'), str):
        item['created_at'] = datetime.fromisoformat(item['created_at'])
    
    return item

@api_router.post("/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate):
    menu_item = MenuItem(**item.model_dump())
    doc = menu_item.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.menu_items.insert_one(doc)
    return menu_item

@api_router.get("/categories")
async def get_categories():
    categories = await db.menu_items.distinct("category")
    return {"categories": categories}

# Cart Routes
@api_router.get("/cart/{user_id}", response_model=Cart)
async def get_cart(user_id: str):
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    if not cart:
        cart = Cart(user_id=user_id, items=[])
        doc = cart.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.carts.insert_one(doc)
    else:
        if isinstance(cart.get('updated_at'), str):
            cart['updated_at'] = datetime.fromisoformat(cart['updated_at'])
    
    return cart

@api_router.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, item: CartItem):
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    
    if not cart:
        cart = Cart(user_id=user_id, items=[item])
        doc = cart.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.carts.insert_one(doc)
    else:
        items = cart.get('items', [])
        found = False
        for cart_item in items:
            if cart_item['menu_item_id'] == item.menu_item_id:
                cart_item['quantity'] += item.quantity
                found = True
                break
        
        if not found:
            items.append(item.model_dump())
        
        await db.carts.update_one(
            {"user_id": user_id},
            {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
    
    return {"message": "Item added to cart"}

@api_router.delete("/cart/{user_id}/remove/{menu_item_id}")
async def remove_from_cart(user_id: str, menu_item_id: str):
    cart = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    
    if cart:
        items = [item for item in cart.get('items', []) if item['menu_item_id'] != menu_item_id]
        await db.carts.update_one(
            {"user_id": user_id},
            {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
    
    return {"message": "Item removed from cart"}

@api_router.delete("/cart/{user_id}/clear")
async def clear_cart(user_id: str):
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    return {"message": "Cart cleared"}

# Wishlist Routes
@api_router.get("/wishlist/{user_id}", response_model=Wishlist)
async def get_wishlist(user_id: str):
    wishlist = await db.wishlists.find_one({"user_id": user_id}, {"_id": 0})
    if not wishlist:
        wishlist = Wishlist(user_id=user_id, menu_item_ids=[])
        doc = wishlist.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.wishlists.insert_one(doc)
    else:
        if isinstance(wishlist.get('updated_at'), str):
            wishlist['updated_at'] = datetime.fromisoformat(wishlist['updated_at'])
    
    return wishlist

@api_router.post("/wishlist/{user_id}/add/{menu_item_id}")
async def add_to_wishlist(user_id: str, menu_item_id: str):
    wishlist = await db.wishlists.find_one({"user_id": user_id}, {"_id": 0})
    
    if not wishlist:
        wishlist = Wishlist(user_id=user_id, menu_item_ids=[menu_item_id])
        doc = wishlist.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.wishlists.insert_one(doc)
    else:
        menu_item_ids = wishlist.get('menu_item_ids', [])
        if menu_item_id not in menu_item_ids:
            menu_item_ids.append(menu_item_id)
            await db.wishlists.update_one(
                {"user_id": user_id},
                {"$set": {"menu_item_ids": menu_item_ids, "updated_at": datetime.now(timezone.utc).isoformat()}}
            )
    
    return {"message": "Item added to wishlist"}

@api_router.delete("/wishlist/{user_id}/remove/{menu_item_id}")
async def remove_from_wishlist(user_id: str, menu_item_id: str):
    wishlist = await db.wishlists.find_one({"user_id": user_id}, {"_id": 0})
    
    if wishlist:
        menu_item_ids = [item_id for item_id in wishlist.get('menu_item_ids', []) if item_id != menu_item_id]
        await db.wishlists.update_one(
            {"user_id": user_id},
            {"$set": {"menu_item_ids": menu_item_ids, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
    
    return {"message": "Item removed from wishlist"}

# Contact Form Routes
@api_router.post("/contact", response_model=ContactForm)
async def submit_contact_form(form: ContactFormCreate):
    contact = ContactForm(**form.model_dump())
    doc = contact.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.contact_forms.insert_one(doc)
    return contact

# Reservation Routes
@api_router.post("/reservation", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate):
    reservation_obj = Reservation(**reservation.model_dump())
    doc = reservation_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.reservations.insert_one(doc)
    return reservation_obj

# Testimonials Routes
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    testimonials = await db.testimonials.find({}, {"_id": 0}).to_list(100)
    return testimonials

# Gallery Routes
@api_router.get("/gallery", response_model=List[GalleryImage])
async def get_gallery_images():
    images = await db.gallery_images.find({}, {"_id": 0}).to_list(100)
    return images

# Statistics Route
@api_router.get("/statistics")
async def get_statistics():
    return {
        "happy_customers": 5000,
        "dishes_served": 25000,
        "years_experience": 15,
        "team_members": 30
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()