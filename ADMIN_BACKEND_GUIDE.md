# Lakeside Indian Restaurant - Admin Backend Access Guide

## 🔐 Admin Login Credentials

**Username:** `admin`  
**Password:** `admin123`

⚠️ **IMPORTANT:** Please change the password after your first login!

---

## 🌐 How to Access the Backend

### Method 1: Direct API Access (Current Setup)

The backend is currently accessible via API endpoints. You can test and use it through:

#### **1. Using Browser (for GET requests)**

Visit these URLs directly in your browser:

- **API Root:** https://spice-harbor-1.preview.emergentagent.com/api/
- **Get All Dine-in Menu:** https://spice-harbor-1.preview.emergentagent.com/api/menu?menu_type=dine-in
- **Get All Takeaway Menu:** https://spice-harbor-1.preview.emergentagent.com/api/menu?menu_type=takeaway
- **Get Categories:** https://spice-harbor-1.preview.emergentagent.com/api/categories
- **Get Testimonials:** https://spice-harbor-1.preview.emergentagent.com/api/testimonials
- **Get Gallery:** https://spice-harbor-1.preview.emergentagent.com/api/gallery
- **Get Statistics:** https://spice-harbor-1.preview.emergentagent.com/api/statistics
- **Get Settings:** https://spice-harbor-1.preview.emergentagent.com/api/settings

#### **2. Using curl (command line)**

**Login to get access token:**
```bash
curl -X POST https://spice-harbor-1.preview.emergentagent.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response will contain an `access_token`. Use it for all admin operations.

**View all contacts (with token):**
```bash
curl https://spice-harbor-1.preview.emergentagent.com/api/admin/contacts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**View all reservations:**
```bash
curl https://spice-harbor-1.preview.emergentagent.com/api/admin/reservations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Update settings:**
```bash
curl -X PUT https://spice-harbor-1.preview.emergentagent.com/api/admin/settings \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "settings",
    "admin_email": "pallabi.dipa@gmail.com",
    "restaurant_name": "Lakeside Indian Restaurant",
    "restaurant_phone": "+61 3 9749 3400",
    "restaurant_address": "94 Belmore Street Yarrawonga 3730",
    "opening_hours": {
      "monday_thursday": "5:00 PM - 10:00 PM",
      "friday_saturday": "5:00 PM - 10:30 PM",
      "sunday": "5:00 PM - 10:00 PM"
    }
  }'
```

#### **3. Using Postman or Insomnia (Recommended for testing)**

1. Download Postman: https://www.postman.com/downloads/
2. Create a new request
3. Set URL: `https://spice-harbor-1.preview.emergentagent.com/api/admin/login`
4. Method: POST
5. Body: JSON
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
6. Copy the `access_token` from response
7. For protected routes, add header: `Authorization: Bearer YOUR_TOKEN`

---

## 📋 Available Admin API Endpoints

### **Authentication**
- `POST /api/admin/login` - Login and get access token
- `GET /api/admin/verify` - Verify if token is valid

### **Settings Management**
- `GET /api/admin/settings` - Get restaurant settings
- `PUT /api/admin/settings` - Update settings (email, phone, address, hours)

### **Menu Management**
- `GET /api/menu` - Get all menu items (public)
- `GET /api/menu/{item_id}` - Get specific item
- `POST /api/admin/menu` - Create new menu item (admin only)
- `PUT /api/admin/menu/{item_id}` - Update menu item (admin only)
- `DELETE /api/admin/menu/{item_id}` - Delete menu item (admin only)
- `GET /api/categories` - Get menu categories

### **Contact Forms**
- `POST /api/contact` - Submit contact form (public)
- `GET /api/admin/contacts` - View all contact submissions (admin only)

### **Reservations**
- `POST /api/reservation` - Submit reservation (public)
- `GET /api/admin/reservations` - View all reservations (admin only)

### **Testimonials**
- `GET /api/testimonials` - Get testimonials (public)
- `POST /api/admin/testimonials` - Create testimonial (admin only)
- `PUT /api/admin/testimonials/{id}` - Update testimonial (admin only)
- `DELETE /api/admin/testimonials/{id}` - Delete testimonial (admin only)

### **Gallery**
- `GET /api/gallery` - Get gallery images (public)
- `POST /api/admin/gallery` - Add gallery image (admin only)
- `DELETE /api/admin/gallery/{id}` - Delete gallery image (admin only)

---

## 📧 Email Notifications

When customers submit **Contact Forms** or **Reservations**, you will receive email notifications at:

**📩 Email:** pallabi.dipa@gmail.com

### To Enable Email Sending:

Add these to `/app/backend/.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

**For Gmail:**
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate "App Password" for "Mail"
4. Use that app password (not your regular password)

---

## 🛠️ Common Admin Tasks

### 1. **View Contact Form Submissions**

```bash
# Login first
TOKEN=$(curl -s -X POST https://spice-harbor-1.preview.emergentagent.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

# Get contacts
curl https://spice-harbor-1.preview.emergentagent.com/api/admin/contacts \
  -H "Authorization: Bearer $TOKEN"
```

### 2. **View Reservations**

```bash
curl https://spice-harbor-1.preview.emergentagent.com/api/admin/reservations \
  -H "Authorization: Bearer $TOKEN"
```

### 3. **Add New Menu Item**

```bash
curl -X POST https://spice-harbor-1.preview.emergentagent.com/api/admin/menu \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Dish Name",
    "description": "Delicious description",
    "price": 19.99,
    "category": "Main Course",
    "menu_type": "dine-in",
    "image": "https://example.com/image.jpg",
    "featured": false
  }'
```

### 4. **Update Menu Item**

```bash
curl -X PUT https://spice-harbor-1.preview.emergentagent.com/api/admin/menu/ITEM_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "price": 21.99
  }'
```

### 5. **Delete Menu Item**

```bash
curl -X DELETE https://spice-harbor-1.preview.emergentagent.com/api/admin/menu/ITEM_ID \
  -H "Authorization: Bearer $TOKEN"
```

### 6. **Change Admin Email**

```bash
curl -X PUT https://spice-harbor-1.preview.emergentagent.com/api/admin/settings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "settings",
    "admin_email": "newemail@example.com",
    "restaurant_name": "Lakeside Indian Restaurant",
    "restaurant_phone": "+61 3 9749 3400",
    "restaurant_address": "94 Belmore Street Yarrawonga 3730",
    "opening_hours": {
      "monday_thursday": "5:00 PM - 10:00 PM",
      "friday_saturday": "5:00 PM - 10:30 PM",
      "sunday": "5:00 PM - 10:00 PM"
    }
  }'
```

---

## 📊 Current Database Stats

- **Total Menu Items:** 242
  - Dine-in: 121 items
  - Takeaway: 121 items
- **Categories:** 14 categories
- **Testimonials:** 5 customer reviews
- **Gallery Images:** 6 photos

---

## 🔒 Security Notes

1. **Access Token expires after 24 hours** - Login again to get new token
2. **Always use HTTPS** - Your data is encrypted in transit
3. **Change default password** after first login
4. **Keep admin credentials secure** - Don't share with unauthorized users
5. **Regularly backup database** if making major changes

---

## 🆘 Troubleshooting

### "Unauthorized" Error
- Your token expired - login again to get new token
- Check if you're using correct credentials

### "404 Not Found"
- Check the URL is correct
- Ensure you're using `/api/` prefix

### Email Not Sending
- Check SMTP credentials in `.env` file
- Verify Gmail app password is correct
- Emails are currently logged to console if SMTP not configured

---

## 📞 Support

For technical support or questions:
- Check backend logs: `tail -f /var/log/supervisor/backend.err.log`
- Check API status: https://spice-harbor-1.preview.emergentagent.com/api/

---

**Last Updated:** October 27, 2024
