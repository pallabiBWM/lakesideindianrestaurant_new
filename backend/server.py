from fastapi import FastAPI, APIRouter, HTTPException, Depends, Body, UploadFile, File
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from auth import verify_password, get_password_hash, create_access_token, verify_token
from email_service import EmailService
import aiofiles
import shutil

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Email service
email_service = EmailService()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = ROOT_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Create the main app without a prefix
app = FastAPI()

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ============= MODELS =============

# Admin Models
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUser(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password_hash: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdminSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = "settings"
    admin_email: str
    restaurant_name: str
    restaurant_phone: str
    restaurant_address: str
    opening_hours: dict
    header_logo: Optional[str] = ""
    footer_logo: Optional[str] = ""
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    happy_customers: Optional[int] = 5000
    dishes_served: Optional[int] = 25000
    years_experience: Optional[int] = 15
    team_members: Optional[int] = 30

# Menu Item Models
class MenuItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    menu_type: str  # 'dine-in' or 'takeaway'
    image: Optional[str] = ""
    featured: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    menu_type: str
    image: Optional[str] = ""
    featured: bool = False

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    menu_type: Optional[str] = None
    image: Optional[str] = None
    featured: Optional[bool] = None

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

class TestimonialCreate(BaseModel):
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

class GalleryImageCreate(BaseModel):
    url: str
    title: str
    description: Optional[str] = None

# Banner Models
class Banner(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image: str
    title: str
    description: str
    button_text: str
    button_link: str
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BannerCreate(BaseModel):
    image: str
    title: str
    description: str
    button_text: str
    button_link: str
    order: int = 0
    active: bool = True

class BannerUpdate(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    button_text: Optional[str] = None
    button_link: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None


# Order Models
class OrderItem(BaseModel):
    menu_item_id: str
    quantity: int

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str = Field(default_factory=lambda: f"ORD-{str(uuid.uuid4())[:8].upper()}")
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    delivery_address: str
    items: List[OrderItem]
    subtotal: float
    tax: float
    delivery_fee: float
    total: float
    payment_method: str
    status: str = "Pending"  # Pending, Confirmed, Preparing, Out for Delivery, Delivered, Cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    delivery_address: str
    items: List[OrderItem]
    subtotal: float
    tax: float
    delivery_fee: float
    total: float
    payment_method: str
    status: str = "Pending"

class OrderUpdate(BaseModel):
    status: Optional[str] = None


# ============= ADMIN ROUTES =============

@api_router.post("/admin/login")
async def admin_login(credentials: AdminLogin):
    # Check if admin exists
    admin = await db.admin_users.find_one({"username": credentials.username}, {"_id": 0})
    
    if not admin or not verify_password(credentials.password, admin['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(data={"sub": admin['username']})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": admin['username']
    }

@api_router.get("/admin/verify")
async def verify_admin(username: str = Depends(verify_token)):
    return {"username": username, "authenticated": True}

@api_router.get("/admin/settings")
async def get_admin_settings(username: str = Depends(verify_token)):
    settings = await db.admin_settings.find_one({"id": "settings"}, {"_id": 0})
    if not settings:
        # Return default settings
        return {
            "id": "settings",
            "admin_email": "pallabi.dipa@gmail.com",
            "restaurant_name": "Lakeside Indian Restaurant",
            "restaurant_phone": "+1 (555) 123-4567",
            "restaurant_address": "123 Lakeside Drive, Waterfront District, City Name, State 12345",
            "opening_hours": {
                "monday_thursday": "11:00 AM - 10:00 PM",
                "friday_saturday": "11:00 AM - 11:00 PM",
                "sunday": "12:00 PM - 9:00 PM"
            }
        }
    return settings

@api_router.put("/admin/settings")
async def update_admin_settings(settings: AdminSettings, username: str = Depends(verify_token)):
    settings_dict = settings.model_dump()
    await db.admin_settings.update_one(
        {"id": "settings"},
        {"$set": settings_dict},
        upsert=True
    )
    return {"message": "Settings updated successfully"}

@api_router.post("/admin/settings/upload-logo")
async def upload_logo(file: UploadFile = File(...), logo_type: str = "header", username: str = Depends(verify_token)):
    """Upload header or footer logo"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp", "image/svg+xml"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Validate logo_type
        if logo_type not in ["header", "footer"]:
            raise HTTPException(status_code=400, detail="logo_type must be 'header' or 'footer'")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"logo_{logo_type}_{uuid.uuid4()}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Return API endpoint URL
        logo_url = f"/api/uploads/{unique_filename}"
        
        return {
            "url": logo_url,
            "filename": unique_filename,
            "logo_type": logo_type
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading logo: {str(e)}")


# ============= PUBLIC ROUTES =============

@api_router.get("/")
async def root():
    return {"message": "Lakeside Indian Restaurant API"}

# Settings Route (Public - for getting contact info)
@api_router.get("/settings")
async def get_public_settings():
    settings = await db.admin_settings.find_one({"id": "settings"}, {"_id": 0})
    if not settings:
        return {
            "restaurant_name": "Lakeside Indian Restaurant",
            "restaurant_phone": "+1 (555) 123-4567",
            "restaurant_address": "123 Lakeside Drive, Waterfront District, City Name, State 12345",
            "admin_email": "pallabi.dipa@gmail.com",
            "header_logo": "",
            "footer_logo": ""
        }
    return {
        "restaurant_name": settings.get("restaurant_name"),
        "restaurant_phone": settings.get("restaurant_phone"),
        "restaurant_address": settings.get("restaurant_address"),
        "admin_email": settings.get("admin_email"),
        "header_logo": settings.get("header_logo", ""),
        "footer_logo": settings.get("footer_logo", "")
    }

# Menu Routes (Public)
@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu_items(
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    menu_type: Optional[str] = None
):
    query = {}
    if category:
        query['category'] = category
    if featured is not None:
        query['featured'] = featured
    if menu_type:
        query['menu_type'] = menu_type
    
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

@api_router.get("/categories")
async def get_categories(menu_type: Optional[str] = None):
    query = {}
    if menu_type:
        query['menu_type'] = menu_type
    categories = await db.menu_items.distinct("category", query)
    return {"categories": categories}

# Admin Menu Routes
@api_router.post("/admin/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate, username: str = Depends(verify_token)):
    menu_item = MenuItem(**item.model_dump())
    doc = menu_item.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.menu_items.insert_one(doc)
    return menu_item

@api_router.put("/admin/menu/{item_id}")
async def update_menu_item(item_id: str, item: MenuItemUpdate, username: str = Depends(verify_token)):
    update_data = {k: v for k, v in item.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    result = await db.menu_items.update_one(
        {"id": item_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    return {"message": "Menu item updated successfully"}

@api_router.delete("/admin/menu/{item_id}")
async def delete_menu_item(item_id: str, username: str = Depends(verify_token)):
    result = await db.menu_items.delete_one({"id": item_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    return {"message": "Menu item deleted successfully"}

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
    
    # Send email notification to admin
    settings = await db.admin_settings.find_one({"id": "settings"}, {"_id": 0})
    admin_email = settings.get('admin_email', 'pallabi.dipa@gmail.com') if settings else 'pallabi.dipa@gmail.com'
    
    contact_data = doc.copy()
    contact_data['created_at'] = contact.created_at.strftime("%Y-%m-%d %H:%M:%S")
    await email_service.send_contact_notification(admin_email, contact_data)
    
    return contact

@api_router.get("/admin/contacts", response_model=List[ContactForm])
async def get_all_contacts(username: str = Depends(verify_token)):
    contacts = await db.contact_forms.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for contact in contacts:
        if isinstance(contact.get('created_at'), str):
            contact['created_at'] = datetime.fromisoformat(contact['created_at'])
    
    return contacts

# Reservation Routes
@api_router.post("/reservation", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate):
    reservation_obj = Reservation(**reservation.model_dump())
    doc = reservation_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.reservations.insert_one(doc)
    
    # Send email notification to admin
    settings = await db.admin_settings.find_one({"id": "settings"}, {"_id": 0})
    admin_email = settings.get('admin_email', 'pallabi.dipa@gmail.com') if settings else 'pallabi.dipa@gmail.com'
    
    reservation_data = doc.copy()
    reservation_data['created_at'] = reservation_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    await email_service.send_reservation_notification(admin_email, reservation_data)
    
    return reservation_obj

@api_router.get("/admin/reservations", response_model=List[Reservation])
async def get_all_reservations(username: str = Depends(verify_token)):
    reservations = await db.reservations.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for reservation in reservations:
        if isinstance(reservation.get('created_at'), str):
            reservation['created_at'] = datetime.fromisoformat(reservation['created_at'])
    
    return reservations

# Testimonials Routes
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    testimonials = await db.testimonials.find({}, {"_id": 0}).to_list(100)
    return testimonials

@api_router.post("/admin/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate, username: str = Depends(verify_token)):
    testimonial_obj = Testimonial(**testimonial.model_dump())
    doc = testimonial_obj.model_dump()
    await db.testimonials.insert_one(doc)
    return testimonial_obj

@api_router.put("/admin/testimonials/{testimonial_id}")
async def update_testimonial(testimonial_id: str, testimonial: TestimonialCreate, username: str = Depends(verify_token)):
    update_data = testimonial.model_dump()
    result = await db.testimonials.update_one(
        {"id": testimonial_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    return {"message": "Testimonial updated successfully"}

@api_router.delete("/admin/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, username: str = Depends(verify_token)):
    result = await db.testimonials.delete_one({"id": testimonial_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    return {"message": "Testimonial deleted successfully"}

# Gallery Routes
@api_router.get("/gallery", response_model=List[GalleryImage])
async def get_gallery_images():
    images = await db.gallery_images.find({}, {"_id": 0}).to_list(100)
    return images

@api_router.post("/admin/gallery", response_model=GalleryImage)
async def create_gallery_image(image: GalleryImageCreate, username: str = Depends(verify_token)):
    gallery_image = GalleryImage(**image.model_dump())
    doc = gallery_image.model_dump()
    await db.gallery_images.insert_one(doc)
    return gallery_image

@api_router.delete("/admin/gallery/{image_id}")
async def delete_gallery_image(image_id: str, username: str = Depends(verify_token)):
    result = await db.gallery_images.delete_one({"id": image_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Gallery image not found")
    
    return {"message": "Gallery image deleted successfully"}

@api_router.post("/admin/gallery/upload")
async def upload_gallery_image(file: UploadFile = File(...), username: str = Depends(verify_token)):
    """Upload a gallery image and return the URL"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Return API endpoint URL instead of static file URL
        image_url = f"/api/uploads/{unique_filename}"
        
        return {
            "url": image_url,
            "filename": unique_filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@api_router.get("/uploads/{filename}")
async def serve_uploaded_file(filename: str):
    """Serve uploaded images through API endpoint"""
    file_path = UPLOADS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine content type based on file extension
    extension = filename.split('.')[-1].lower()
    content_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    content_type = content_types.get(extension, 'application/octet-stream')
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path, media_type=content_type)

# Statistics Route
@api_router.get("/statistics")
async def get_statistics():
    settings = await db.admin_settings.find_one({"id": "settings"}, {"_id": 0})
    if settings:
        return {
            "happy_customers": settings.get("happy_customers", 5000),
            "dishes_served": settings.get("dishes_served", 25000),
            "years_experience": settings.get("years_experience", 15),
            "team_members": settings.get("team_members", 30)
        }
    return {
        "happy_customers": 5000,
        "dishes_served": 25000,
        "years_experience": 15,
        "team_members": 30
    }

# Banner Routes (Public)
@api_router.get("/banners", response_model=List[Banner])
async def get_banners():
    banners = await db.banners.find({"active": True}, {"_id": 0}).sort("order", 1).to_list(100)
    
    for banner in banners:
        if isinstance(banner.get('created_at'), str):
            banner['created_at'] = datetime.fromisoformat(banner['created_at'])
    
    return banners

# Banner Routes (Admin)
@api_router.get("/admin/banners", response_model=List[Banner])
async def get_all_banners(username: str = Depends(verify_token)):
    banners = await db.banners.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    
    for banner in banners:
        if isinstance(banner.get('created_at'), str):
            banner['created_at'] = datetime.fromisoformat(banner['created_at'])
    
    return banners

@api_router.post("/admin/banners", response_model=Banner)
async def create_banner(banner: BannerCreate, username: str = Depends(verify_token)):
    banner_obj = Banner(**banner.model_dump())
    doc = banner_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.banners.insert_one(doc)
    return banner_obj

@api_router.put("/admin/banners/{banner_id}")
async def update_banner(banner_id: str, banner: BannerUpdate, username: str = Depends(verify_token)):
    update_data = {k: v for k, v in banner.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    result = await db.banners.update_one(
        {"id": banner_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    return {"message": "Banner updated successfully"}

@api_router.delete("/admin/banners/{banner_id}")
async def delete_banner(banner_id: str, username: str = Depends(verify_token)):
    result = await db.banners.delete_one({"id": banner_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    return {"message": "Banner deleted successfully"}

@api_router.post("/admin/banners/upload")
async def upload_banner_image(file: UploadFile = File(...), username: str = Depends(verify_token)):
    """Upload a banner image and return the URL"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Return API endpoint URL instead of static file URL
        image_url = f"/api/uploads/{unique_filename}"
        
        return {
            "url": image_url,
            "filename": unique_filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")



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
