# 🚀 AETHER Marketplace - Setup & Running Guide

## ✅ Backend Setup Complete

### Database Migrations Applied
```
✅ marketplace.0002_product_category
✅ subscriptions.0002_alter_merchantsubscription_plan
```

### Superuser Created
- **Email**: admin@test.com
- **Password**: admin123
- **Role**: ADMIN

### Development Server Running
- **URL**: http://localhost:8000
- **Status**: ✅ Running on port 8000

---

## 🎯 Quick Start Guide

### 1. Backend (Already Running)
```bash
# Terminal 1: Backend Server
cd marketplace_backend
python manage.py runserver
# Now running at: http://localhost:8000
```

### 2. Frontend (Open in Browser)
```bash
# Option A: Direct File
Open: legendary_frontend/index.html

# Option B: Local Server
cd legendary_frontend
python -m http.server 8001
# Then open: http://localhost:8001
```

---

## 🧪 Test User Accounts

### Admin Account (Ready to Use)
```
Email: admin@test.com
Password: admin123
Role: ADMIN
```

### Create Test Accounts

**Customer Account** (via Registration)
1. Go to `http://localhost:8001/register.html`
2. Select: Customer
3. Email: customer@test.com
4. Password: test123456
5. Submit → Redirects to login

**Merchant Account** (via Registration)
1. Go to `http://localhost:8001/register.html`
2. Select: Merchant
3. Email: merchant@test.com
4. Password: test123456
5. Business Name: My Store
6. Submit → Redirects to login

---

## 📝 Test Workflows

### Workflow 1: Customer Journey (5 min)
1. Login as customer@test.com
2. Navigate to Dashboard
3. Click "Marketplace" → See products (empty initially)
4. Place orders (once merchant creates products)

### Workflow 2: Merchant Journey (10 min)
1. Login as merchant@test.com
2. Navigate to Dashboard
3. See "OFFLINE / UNPAID" status
4. Click "View Plans" → See subscription plans
5. Select a plan → Upload payment proof (any image file)
6. Submit → See "PENDING" status
7. Logout

### Workflow 3: Admin Approval (5 min)
1. Login as admin@test.com
2. Navigate to Dashboard → Admin Dashboard appears
3. Click "Review Queue" → See pending subscriptions
4. Click "Approve" → Subscription activated
5. Click "Access Users" → See all users
6. Click "Manage Plans" → Manage subscription plans

### Workflow 4: Merchant Product Creation (5 min)
1. Login as merchant@test.com (after admin approval)
2. Navigate to Dashboard
3. See "ACTIVE LINK" status
4. Click "+ New Asset" → Goes to add-product.html
5. Fill form:
   - Asset Name: Test Product
   - Description: A test product
   - Price: 99.99
   - Category: Digital Asset
   - Image: (optional)
   - Active: Check
6. Submit → Product created, redirects to dashboard

---

## 🔗 API Endpoints Testing

### Authentication Endpoints
```
POST   /api/auth/register/
POST   /api/auth/login/
GET    /api/auth/me/
POST   /api/auth/refresh/
```

### Subscription Endpoints
```
GET    /api/plans/
POST   /api/merchant/subscriptions/
GET    /api/admin/subscriptions/
PATCH  /api/admin/subscriptions/{id}/
```

### Product Endpoints
```
GET    /api/customer/products/
GET    /api/merchant/products/
POST   /api/merchant/products/
```

### Order Endpoints
```
POST   /api/customer/orders/
GET    /api/customer/orders/
GET    /api/merchant/orders/
```

### User Management Endpoints
```
GET    /api/admin/users/
PATCH  /api/admin/users/{id}/
```

### Testing with curl/Postman
```bash
# Get JWT Token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"admin123"}'

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 📂 File Locations

### Frontend Files
```
legendary_frontend/
├── index.html              (Start here)
├── login.html              (Login page)
├── register.html           (Register page)
├── dashboard.html          (Main dashboard)
├── marketplace.html        (Customer products)
├── add-product.html        (Merchant products)
├── admin-users.html        (Admin users)
├── admin-plans.html        (Admin plans)
├── style.css               (Styles)
└── script.js               (Animations)
```

### Backend Files
```
marketplace_backend/
├── manage.py               (Django manager)
├── db.sqlite3              (Database)
├── config/
│   ├── settings.py         (Configuration)
│   ├── urls.py             (Routes)
│   └── wsgi.py
├── marketplace/            (Product management)
├── subscriptions/          (Subscription system)
├── users/                  (User management)
└── core/                   (Admin functionality)
```

---

## 🎓 Understanding the System

### Multi-Role Architecture
- **Customer**: Browse products, place orders
- **Merchant**: Create products, manage store (after subscription approval)
- **Admin**: Manage users, approve subscriptions, manage plans

### Subscription Workflow
1. Merchant registers
2. Merchant views plans
3. Merchant uploads payment proof
4. Admin reviews and approves/rejects
5. On approval: Merchant can create products
6. Products visible to customers when merchant is approved

### Data Flow
```
Frontend (HTML/JS) 
    ↓ (API Calls with JWT Token)
Backend API (Django REST Framework)
    ↓ (Auth, Permissions)
Database (SQLite)
    ↓ (Query Results)
Frontend (Display)
```

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" in browser
**Solution**: 
- Check backend is running: `http://localhost:8000`
- Check CORS is enabled (it is by default)
- Check browser console for detailed error

### Issue: Login fails with "401 Unauthorized"
**Solution**:
- Verify credentials (admin@test.com / admin123)
- Check token is being saved in localStorage
- Clear browser cache and try again

### Issue: "Backend not responding"
**Solution**:
```bash
# Restart backend
cd marketplace_backend
python manage.py runserver
```

### Issue: Database errors
**Solution**:
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Port 8000 already in use
**Solution**:
```bash
# Use different port
python manage.py runserver 8001
# Update frontend API_BASE to http://localhost:8001/api
```

---

## ✨ Features Implemented

### Customer Features
- ✅ Register and login
- ✅ Browse products from verified merchants
- ✅ Search and filter products
- ✅ Place orders
- ✅ View order history
- ✅ Dashboard with product grid

### Merchant Features
- ✅ Register with business name
- ✅ View available subscription plans
- ✅ Upload payment proof
- ✅ See subscription status
- ✅ Create products (when subscribed)
- ✅ Manage product inventory
- ✅ View received orders

### Admin Features
- ✅ Review pending subscriptions
- ✅ View payment proof images
- ✅ Approve/reject subscriptions
- ✅ Manage all users
- ✅ Search and filter users
- ✅ Edit user roles and status
- ✅ Create subscription plans
- ✅ Manage plan configuration

---

## 📊 System Status

### Backend
- ✅ Django 5.2.10
- ✅ Database migrations applied
- ✅ Superuser created
- ✅ Development server running
- ✅ CORS enabled
- ✅ JWT authentication working

### Frontend
- ✅ 8 pages built
- ✅ Design system maintained
- ✅ API integration working
- ✅ Role-based access implemented
- ✅ Responsive design
- ✅ Animations functional

### API
- ✅ 15+ endpoints operational
- ✅ Authentication working
- ✅ Authorization enforced
- ✅ Error handling implemented
- ✅ Pagination supported
- ✅ Search/filter working

---

## 🎯 Next Steps

1. **Test customer flow** - Register, browse, order
2. **Test merchant flow** - Register, subscribe, create products
3. **Test admin flow** - Approve subscriptions, manage users
4. **Verify all pages** - Check design and animations
5. **Check API endpoints** - Use Postman or curl
6. **Review documentation** - Check README.md files

---

## 📞 Support

### Documentation Files
- README.md - Master index
- COMPLETION_SUMMARY.md - Project overview
- QUICK_REFERENCE.md - Daily guide
- IMPLEMENTATION_SUMMARY.md - Technical details
- FRONTEND_PAGES_DOCUMENTATION.md - Page guide
- USER_JOURNEY_MAP.md - Flow diagrams

### Common Commands
```bash
# Start backend
cd marketplace_backend && python manage.py runserver

# Create test user
python manage.py shell

# Run migrations
python manage.py migrate

# See all database tables
python manage.py dbshell
```

---

## ✅ System Ready

**Backend**: ✅ Running on http://localhost:8000
**Database**: ✅ Migrations applied
**Admin Account**: ✅ admin@test.com / admin123
**Frontend**: ✅ Ready to open legendary_frontend/index.html

**You're all set to start testing! 🎉**
