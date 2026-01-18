# AETHER Marketplace - User Journey Maps

## User Registration & Login Flow

```
┌─────────────────────────────────────────────────────────┐
│  START: User Arrives at index.html                      │
├─────────────────────────────────────────────────────────┤
│  Landing Page Features:                                 │
│  • Hero section with "Start Trading" button             │
│  • Feature overview cards                               │
│  • Role descriptions (Admin, Merchant, Customer)        │
│  • Navigation: Home, About, Features, Roles             │
│  • CTA buttons linking to register.html or login.html   │
└──────────┬──────────────────────────────────────────────┘
           │
           ├─────────────────────────┬────────────────────┐
           │                         │                    │
           v                         v                    v
    register.html              login.html            dashboard.html
    (New User)              (Existing User)       (If already logged in)
     │                          │                         │
     ├─ Select Role             ├─ Enter Email           └─ Redirects based
     │  ├─ Customer             │  Enter Password            on role
     │  └─ Merchant             │                        
     │                          │ POST /api/auth/login/   
     ├─ Enter Email             │                        
     ├─ Enter Password          │ Response:              
     ├─ Confirm Password        │ ├─ access_token        
     │                          │ ├─ refresh_token       
     ├─ (Merchant Only)         │ └─ user data           
     │  └─ Business Name        │                        
     │                          │ localStorage.setItem()  
     │ POST /api/auth/register/ │                        
     │                          └─────────────┬──────────┘
     │ Response:                              │
     ├─ Success                              │
     │  └─ Show success message              │
     │  └─ Redirect to login.html            │
     │                                        v
     └─ Error                            dashboard.html
        └─ Show validation errors        (Logged In User)
                                         │
                                         ├─ Admin Dashboard
                                         │  ├─ Subscription Approvals
                                         │  ├─ User Management → admin-users.html
                                         │  └─ Plan Management → admin-plans.html
                                         │
                                         ├─ Merchant Dashboard
                                         │  ├─ Store Status (subscription check)
                                         │  ├─ Asset Inventory
                                         │  ├─ New Asset button → add-product.html
                                         │  └─ View subscription plans
                                         │
                                         └─ Customer Dashboard
                                            ├─ Product Grid (loaded from API)
                                            ├─ Browse button → marketplace.html
                                            └─ Order History
```

## Customer User Journey

```
┌───────────────────────────────────────────────────────┐
│  Customer Logged In - dashboard.html                  │
├───────────────────────────────────────────────────────┤
│  Customer sees:                                       │
│  • Product grid (from active merchants)              │
│  • Order history table                               │
│  • Browse button linking to marketplace.html         │
└───────────────────────┬───────────────────────────────┘
                        │
                        v
            marketplace.html
            ┌─────────────────────────────┐
            │  Full Product Marketplace   │
            ├─────────────────────────────┤
            │  Features:                  │
            │  • Search by product name   │
            │  • Filter by merchant       │
            │  • Sort (price, newest)     │
            │  • Pagination               │
            │  • Product cards with:      │
            │    - Product image          │
            │    - Name & merchant info   │
            │    - Price                  │
            │    - View & Acquire buttons │
            └────────┬────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
         v                      v
    View Product          Place Order
    (Detail Modal)        (Acquire)
    │                     │
    └─ Confirmation       │ POST /api/customer/orders/
                          │ (product_id)
                          │
                          v
                     Order Placed!
                     │
                     └─ View in Order History
                        (dashboard.html)
```

## Merchant User Journey

```
┌───────────────────────────────────────────────────────┐
│  Merchant Logged In - dashboard.html                  │
├───────────────────────────────────────────────────────┤
│  Merchant sees:                                       │
│  • Store Status card                                 │
│  • Asset Inventory table                             │
│  • Subscription status badge                         │
└───────────┬─────────────────────────────────────────┘
            │
       ┌────┴───────────────────────────┐
       │                                │
NOT SUBSCRIBED                  SUBSCRIBED
       │                                │
       v                                v
Show "View Plans"            Show "+ New Asset"
Button                       Button (Enabled)
│                                │
├─ "View Plans" clicked      ├─ Click "+ New Asset"
│  └─ Show available plans       │
│     ├─ Plan name, price        └─ Navigate to
│     ├─ Duration                   add-product.html
│     └─ "Select Plan" button        │
│        │                           ├─ Asset Name
│        v                           ├─ Description
│    Modal: Upload               ├─ Price
│    Payment Proof               ├─ Category
│    ├─ Select plan              ├─ Image upload
│    ├─ Upload image             ├─ Active toggle
│    ├─ Add notes                │
│    └─ Submit                   v
│       │                    POST /api/merchant/
│       │                    products/
│       v                    │
│    Admin Review            v
│    (subscription_mgmt)   Asset Created!
│    ├─ Pending              │
│    ├─ View proof image      └─ Visible in
│    └─ Approve/Reject          inventory
│       │
│       v
│    On Approval:
│    ├─ subscription_status = approved
│    ├─ Merchant notified
│    └─ Can now create products
│
│    On Rejection:
│       └─ Try another plan
│
└─ Asset Inventory
   ├─ View own products
   ├─ Edit/Delete products
   └─ View asset status
```

## Admin User Journey

```
┌───────────────────────────────────────────────────────┐
│  Admin Logged In - dashboard.html                     │
├───────────────────────────────────────────────────────┤
│  Admin sees:                                          │
│  • Subscription Approvals card                        │
│  • User Management card                               │
│  • Plan Management card                               │
└───────────┬──────────────────────────────────────────┘
            │
     ┌──────┼──────┬────────────┐
     │      │      │            │
     v      v      v            v
Approvals Users  Plans      (Other Admin
                             Functions)
│      │      │
│      │      └─ admin-plans.html
│      │         │
│      │         ├─ Create new plan
│      │         ├─ Name, price, duration
│      │         ├─ Max products limit
│      │         └─ Save/Update
│      │
│      └─ admin-users.html
│         │
│         ├─ Search users by email
│         ├─ Filter by role
│         ├─ Filter by status (active/inactive)
│         ├─ View user list
│         │  ├─ Email
│         │  ├─ Role badge
│         │  ├─ Status badge
│         │  ├─ Join date
│         │  └─ Actions (Edit, Toggle)
│         │
│         ├─ Edit User Modal
│         │  ├─ Change role
│         │  ├─ Toggle active status
│         │  └─ Save changes
│         │
│         └─ User Management Complete
│
└─ Subscription Approvals Section
   │
   ├─ Show pending subscriptions table
   │  ├─ Merchant email
   │  ├─ Business name
   │  ├─ Selected plan
   │  ├─ Submission date
   │  └─ Actions (Approve/Reject)
   │
   ├─ Review Payment Proof
   │  └─ View uploaded image
   │
   ├─ Approve Subscription
   │  │ PATCH /api/admin/subscriptions/{id}/
   │  │ {status: "APPROVED"}
   │  │
   │  v
   │ ✓ Subscription Activated
   │   ├─ Merchant can now list products
   │   ├─ Appears in customer marketplace
   │   └─ Notification sent to merchant
   │
   └─ Reject Subscription
      │ PATCH /api/admin/subscriptions/{id}/
      │ {status: "REJECTED", 
      │  rejection_reason: "..."}
      │
      v
     ✗ Subscription Rejected
       ├─ Merchant notified
       ├─ Merchant can resubmit
       └─ Cannot list products
```

## Complete API Call Flow

```
AUTHENTICATION
├─ POST /api/auth/register/
│  └─ Request: {email, password, role, [business_name]}
│     Response: {id, email, role, created_at}
│
├─ POST /api/auth/login/
│  └─ Request: {email, password}
│     Response: {access_token, refresh_token}
│
├─ GET /api/auth/me/
│  └─ Headers: Authorization: Bearer {token}
│     Response: {id, email, role, is_subscribed, subscription_end}
│
└─ POST /api/auth/refresh/
   └─ Request: {refresh_token}
      Response: {access_token}

SUBSCRIPTION MANAGEMENT
├─ GET /api/plans/
│  └─ Response: [{id, name, price, duration_days, description}]
│
├─ POST /api/merchant/subscriptions/
│  └─ Request: {plan, proof_image, notes} (FormData)
│     Response: {id, plan, status: "PENDING", created_at}
│
├─ GET /api/admin/subscriptions/
│  └─ Response: [{id, merchant_email, plan_name, status, submitted_at}]
│
└─ PATCH /api/admin/subscriptions/{id}/
   └─ Request: {status: "APPROVED"} or 
      {status: "REJECTED", rejection_reason: "..."}
      Response: {id, status, start_date, end_date}

PRODUCTS
├─ GET /api/customer/products/
│  └─ Params: ?page=1, ?search=..., ?merchant=..., ?ordering=...
│     Response: {count, next, previous, results: [{id, name, price, merchant_name}]}
│
├─ GET /api/merchant/products/
│  └─ Returns: Merchant's own products
│
└─ POST /api/merchant/products/
   └─ Request: {name, description, price, category, image, is_active} (FormData)
      Response: {id, name, price, is_active, created_at}

ORDERS
├─ POST /api/customer/orders/
│  └─ Request: {product_id}
│     Response: {id, customer_id, merchant_id, status, items, created_at}
│
├─ GET /api/customer/orders/
│  └─ Response: [{id, merchant_name, status, items, created_at}]
│
└─ GET /api/merchant/orders/
   └─ Response: [{id, customer_email, status, items, created_at}]

USER MANAGEMENT (ADMIN)
├─ GET /api/admin/users/
│  └─ Params: ?search=..., ?role=..., ?is_active=...
│     Response: {count, next, previous, results: [{id, email, role, is_active, date_joined}]}
│
└─ PATCH /api/admin/users/{id}/
   └─ Request: {role: "MERCHANT"} or {is_active: false}
      Response: {id, email, role, is_active}
```

## Page Navigation Tree

```
index.html (Public Landing)
├── Header Navigation
│   ├─ Home (anchor #home)
│   ├─ About (anchor #about)
│   ├─ Features (anchor #features)
│   ├─ Roles (anchor #roles)
│   ├─ Dashboard (→ dashboard.html)
│   └─ Login (→ login.html)
│
├── Hero Section CTA
│   ├─ "Start Trading" (→ register.html)
│   └─ "Learn More" (anchor #about)
│
└── Roles Section CTA
    └─ "Create Your Account" (→ register.html)

login.html (Public Auth)
├── Navbar (→ index.html, register.html)
└── Login Form
    ├─ Submit (POST /api/auth/login/)
    └─ "Request Access" (→ register.html)

register.html (Public Auth)
├── Navbar (→ index.html, login.html)
└── Register Form
    ├─ Submit (POST /api/auth/register/)
    └─ "Already have credentials?" (→ login.html)

dashboard.html (Protected - Role-Based)
├── Navbar (→ index.html, marketplace.html, logout)
│
├── Admin Dashboard (if role == ADMIN)
│   ├─ "Review Queue" (shows approvalsSection)
│   ├─ "Access Users" (→ admin-users.html)
│   └─ "Manage Plans" (→ admin-plans.html)
│
├── Merchant Dashboard (if role == MERCHANT)
│   ├─ Store Status Card
│   │   ├─ "View Plans" (shows merchantPlansSection)
│   │   └─ Select Plan (→ uploadProofModal)
│   ├─ Asset Inventory
│   │   ├─ "+ New Asset" (→ add-product.html)
│   │   └─ Products Table
│   └─ Subscription Plans Section (hidden initially)
│       └─ Plan Cards with "Select Plan" buttons
│
└── Customer Dashboard (if role == CUSTOMER)
    ├─ Product Grid
    │   └─ "Acquire" (POST /api/customer/orders/)
    └─ Order History Table

marketplace.html (Protected - Customers)
├── Navbar (→ index.html, dashboard.html, logout)
├── Search & Filters
│   ├─ Search input (real-time)
│   ├─ Merchant dropdown filter
│   ├─ Sort dropdown
│   └─ Apply Filters button
├── Product Grid
│   ├─ Product Cards with "View" and "Acquire" buttons
│   └─ Pagination
└── Marketplace Navigation

add-product.html (Protected - Subscribed Merchants)
├── Navbar (→ index.html, dashboard.html, logout)
├── Product Form
│   ├─ Name, Description, Price, Category
│   ├─ Image upload
│   ├─ Active toggle
│   └─ Submit buttons (Create Asset, Cancel)
└── Form Validation & Error Display

admin-users.html (Protected - Admins Only)
├── Navbar (→ index.html, dashboard.html, logout)
├── Search & Filters
│   ├─ Search users by email
│   ├─ Role filter dropdown
│   ├─ Status filter dropdown
│   └─ Apply Filters button
├── Users Table
│   ├─ Display all users with pagination
│   ├─ Edit button (→ editUserModal)
│   └─ Toggle Active button
└── Edit User Modal
    ├─ Email (read-only)
    ├─ Role dropdown
    ├─ Active checkbox
    └─ Update button

admin-plans.html (Protected - Admins Only)
├── Navbar (→ index.html, dashboard.html, logout)
├── Plans List
│   ├─ Display all subscription plans
│   ├─ Create new plan button (→ newPlanModal)
│   └─ Edit existing plans
├── Plan Form
│   ├─ Name, Price, Duration, Description
│   ├─ Max products limit
│   └─ Save button
└── Plans Management
```

---

## Summary of All Pages & Their Functions

| Page | Route | Access | Purpose | Key Features |
|------|-------|--------|---------|--------------|
| index.html | / | Public | Landing page | Hero, features, roles, CTA |
| login.html | /login.html | Public | User authentication | JWT login form |
| register.html | /register.html | Public | User registration | Role selection, form |
| dashboard.html | /dashboard.html | Protected | Universal dashboard | Role-specific content |
| marketplace.html | /marketplace.html | Customer | Product discovery | Search, filter, order |
| add-product.html | /add-product.html | Merchant | Product creation | Form with validation |
| admin-users.html | /admin-users.html | Admin | User management | CRUD operations |
| admin-plans.html | /admin-plans.html | Admin | Plan management | Create/edit plans |

---

## Color & Animation Consistency

All pages maintain:
- **Primary Colors**: Cyan accent (#00f2ea), Pink accent (#ff0050), Black background (#050505)
- **Fonts**: Space Grotesk (headings), Outfit (body)
- **Animations**: GSAP reveal-up, reveal-left, reveal-scale, scroll triggers
- **Components**: Glassmorphism cards, custom cursor, magnetic buttons
- **Background**: Three.js particle animation on every page
