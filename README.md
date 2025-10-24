# Lakeside Indian Restaurant Website

A modern, full-stack React-based restaurant website with e-commerce functionality for Lakeside Indian Restaurant.

## 🎨 Features

### **Frontend Pages**
- **Home Page**: Hero carousel, about preview, statistics, featured dishes, gallery preview, contact/reservation links, and customer testimonials
- **About Us**: Restaurant story, philosophy, chef introduction, and cuisine types
- **Menu**: Full menu with category filtering, add to cart, and wishlist functionality
- **Gallery**: Professional image gallery with lightbox feature
- **Contact Us**: Contact form, location map, contact information, and opening hours
- **Reservation**: Table reservation form with date/time selection
- **Cart**: Shopping cart with order summary and checkout (payment integration pending)
- **Wishlist**: Saved favorite dishes

### **Design**
- **Color Theme**: Black (#000000) and Red (#DC2626) - Elegant & Modern
- **Responsive Design**: Mobile-friendly layout
- **Sticky Header**: Transparent on homepage, solid black on scroll
- **Professional Images**: AI-sourced restaurant and food photography
- **Smooth Animations**: Carousel transitions, hover effects

### **E-Commerce Features**
- Add items to cart from menu
- Wishlist functionality
- Cart management (add, remove, clear)
- Order summary with tax and delivery fee calculation
- Real-time cart and wishlist counters in header

## 🛠️ Tech Stack

### **Frontend**
- React 19.0.0
- React Router DOM for navigation
- Axios for API calls
- Tailwind CSS for styling
- Radix UI components
- Lucide React icons

### **Backend**
- FastAPI (Python)
- MongoDB with Motor (async driver)
- Pydantic for data validation
- CORS enabled

### **Database Collections**
- `menu_items` - Restaurant menu items
- `carts` - User shopping carts
- `wishlists` - User wishlists
- `contact_forms` - Contact form submissions
- `reservations` - Table reservations
- `testimonials` - Customer reviews
- `gallery_images` - Gallery photos

## 📂 Project Structure

```
/app/
├── backend/
│   ├── server.py           # FastAPI application with all routes
│   ├── seed_data.py        # Database seeding script
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main application component
│   │   ├── pages/         # All page components
│   │   │   ├── Home.js
│   │   │   ├── About.js
│   │   │   ├── Menu.js
│   │   │   ├── Gallery.js
│   │   │   ├── Contact.js
│   │   │   ├── Reservation.js
│   │   │   ├── Cart.js
│   │   │   └── Wishlist.js
│   │   ├── components/    # Reusable components
│   │   │   ├── Layout.js
│   │   │   ├── Header.js
│   │   │   └── Footer.js
│   │   ├── context/       # React Context for state management
│   │   │   ├── CartContext.js
│   │   │   └── WishlistContext.js
│   │   ├── App.css        # Global styles
│   │   └── index.js       # Application entry point
│   ├── package.json       # Node dependencies
│   └── .env              # Frontend environment variables
└── README.md
```

## 🚀 API Endpoints

### **Menu**
- `GET /api/menu` - Get all menu items (optional: ?category=Main Course&featured=true)
- `GET /api/menu/{item_id}` - Get specific menu item
- `POST /api/menu` - Create new menu item
- `GET /api/categories` - Get all menu categories

### **Cart**
- `GET /api/cart/{user_id}` - Get user's cart
- `POST /api/cart/{user_id}/add` - Add item to cart
- `DELETE /api/cart/{user_id}/remove/{menu_item_id}` - Remove item from cart
- `DELETE /api/cart/{user_id}/clear` - Clear entire cart

### **Wishlist**
- `GET /api/wishlist/{user_id}` - Get user's wishlist
- `POST /api/wishlist/{user_id}/add/{menu_item_id}` - Add item to wishlist
- `DELETE /api/wishlist/{user_id}/remove/{menu_item_id}` - Remove item from wishlist

### **Forms**
- `POST /api/contact` - Submit contact form
- `POST /api/reservation` - Create table reservation

### **Content**
- `GET /api/testimonials` - Get customer testimonials
- `GET /api/gallery` - Get gallery images
- `GET /api/statistics` - Get restaurant statistics

## 🎯 Sample Data

The database is pre-seeded with:
- **12 Menu Items** across categories (Main Course, Starters, Desserts, Drinks)
- **5 Customer Testimonials** with 5-star ratings
- **6 Gallery Images** showcasing restaurant interior and food
- **Restaurant Statistics** (5000+ customers, 25000+ dishes served, etc.)

## 🔧 Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=https://spice-harbor-1.preview.emergentagent.com
WDS_SOCKET_PORT=443
REACT_APP_ENABLE_VISUAL_EDITS=true
ENABLE_HEALTH_CHECK=false
```

## 💻 Running the Application

The application is already running via supervisor:
- **Backend**: http://localhost:8001
- **Frontend**: http://localhost:3000 (proxied through nginx)

To restart services:
```bash
sudo supervisorctl restart all
```

To check service status:
```bash
sudo supervisorctl status
```

## 📦 Adding New Features

### To Add Payment Integration (Stripe):
1. Install Stripe library: `cd /app/backend && pip install stripe && pip freeze > requirements.txt`
2. Add Stripe keys to backend/.env
3. Create payment endpoint in server.py
4. Update Cart.js checkout button to call payment API
5. Implement Stripe Elements in frontend

### To Add Menu Item:
Use the API:
```bash
curl -X POST http://localhost:8001/api/menu \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dish Name",
    "description": "Description",
    "price": 15.99,
    "category": "Main Course",
    "image": "image_url",
    "featured": false
  }'
```

## 🎨 Customization

### Change Color Theme
Edit the colors in:
- `/app/frontend/src/App.css` - Global styles
- Tailwind classes in components (e.g., `bg-red-600`, `text-red-600`)

### Update Logo
Replace the text logo in `/app/frontend/src/components/Header.js` with an image:
```jsx
<img src="/path-to-logo.png" alt="Lakeside Indian Restaurant" />
```

### Add New Page
1. Create page component in `/app/frontend/src/pages/`
2. Add route in `/app/frontend/src/App.js`
3. Add navigation link in `/app/frontend/src/components/Header.js`

## 📝 Notes

- **Payment Integration**: Ready for Stripe integration (currently shows placeholder message)
- **User Authentication**: Currently uses demo user ID stored in localStorage
- **Image URLs**: All images are hosted on Unsplash and Pexels
- **Mobile Responsive**: Fully responsive design with mobile menu

## 🔮 Future Enhancements

- [ ] Stripe payment integration
- [ ] User authentication (login/signup)
- [ ] Order history
- [ ] Email notifications for reservations
- [ ] Online ordering with delivery tracking
- [ ] Admin panel for managing menu items
- [ ] Reviews and ratings system
- [ ] Table availability calendar
- [ ] Multi-language support

## 📄 License

This project is built for Lakeside Indian Restaurant.

---

**Built with ❤️ using React, FastAPI, and MongoDB**
