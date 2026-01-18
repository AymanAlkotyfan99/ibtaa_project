# AETHER Marketplace - Frontend Pages Documentation

## Overview
Complete frontend implementation for the AETHER premium marketplace ecosystem with multi-role support (Admin, Merchant, Customer).

## Frontend Pages

### Public Pages (No Authentication Required)
1. **index.html** - Landing page with hero section, features overview, and role descriptions
   - Navigation links to login, register, and dashboard
   - Displays marketplace benefits and features
   - Animated hero section with Three.js WebGL background

2. **login.html** - Authentication page for existing users
   - Email/password login form
   - JWT token-based authentication
   - Redirects to dashboard on successful login
   - Link to registration page for new users

3. **register.html** - Account creation page
   - Role selection (Customer or Merchant)
   - Email and password entry with confirmation
   - Merchant-specific field (business name) shown conditionally
   - API integration for user registration

### Authenticated Pages (Require Login)

#### Universal Pages
4. **dashboard.html** - Main command center (role-specific content)
   - Admin Dashboard: Subscription approvals, user management, plan management
   - Merchant Dashboard: Store status, asset inventory, subscription management
   - Customer Dashboard: Product browsing, order history
   - Navigation bar with user role and logout button

#### Customer Pages
5. **marketplace.html** - Product browsing and discovery interface
   - Filter products by search, merchant, and sort options
   - Pagination support
   - Product cards with merchant information and pricing
   - "Acquire" (place order) functionality
   - Accessible only by customers

#### Merchant Pages
6. **add-product.html** - Asset creation form
   - Input fields for name, description, price, category
   - Image upload support
   - Active/inactive toggle
   - Subscription validation (redirects if not subscribed)
   - Accessible only by subscribed merchants

#### Admin Pages
7. **admin-users.html** - User management interface
   - Search and filter users by email, role, and status
   - View user list with roles and join dates
   - Edit user role and activation status
   - Pagination support
   - Accessible only by admins

8. **admin-plans.html** - Subscription plan management
   - Create new subscription plans
   - Edit existing plans (price, duration, description)
   - Manage plan status (active/inactive)
   - View all configured plans
   - Accessible only by admins

## Design Features

### Consistent Design System
- **Color Scheme**: 
  - Primary accent: Cyan (#00f2ea)
  - Secondary accent: Pink/Red (#ff0050)
  - Background: Black (#050505)
  - Text: White with transparency variations

- **Typography**:
  - Headings: Space Grotesk (bold, modern)
  - Body: Outfit (readable, elegant)

- **Components**:
  - Glassmorphism cards with blur effects
  - Custom cursor with tracking
  - Magnetic button effects
  - Animated reveals on scroll
  - Three.js WebGL particle background

### Animations & Interactions
- GSAP timeline animations for page reveals
- Scroll trigger animations (reveal-up, reveal-left, reveal-scale)
- Custom cursor tracking
- Magnetic button hover effects
- Smooth page transitions
- Navbar scroll effects

## Backend API Integration

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - JWT token generation
- `GET /api/auth/me/` - Get current user info
- `POST /api/auth/refresh/` - Refresh JWT token

### Marketplace Endpoints
- `GET /api/customer/products/` - Browse products (customers)
- `GET /api/merchant/products/` - View own products (merchants)
- `POST /api/merchant/products/` - Create product (merchants)
- `GET /api/customer/orders/` - View customer orders
- `POST /api/customer/orders/` - Place order
- `GET /api/merchant/orders/` - View received orders (merchants)

### Subscription Endpoints
- `GET /api/plans/` - Get available subscription plans
- `POST /api/merchant/subscriptions/` - Submit subscription with payment proof
- `GET /api/admin/subscriptions/` - View pending approvals (admins)
- `PATCH /api/admin/subscriptions/{id}/` - Approve/reject subscription (admins)

### Admin Endpoints
- `GET /api/admin/settings/` - Get admin settings and plans
- `PATCH /api/admin/settings/` - Update admin settings
- `GET /api/admin/users/` - List all users (with filters)
- `PATCH /api/admin/users/{id}/` - Update user role/status

## Session Management
- JWT tokens stored in localStorage
- Token validation on page load
- Automatic redirect to login on token expiration
- Logout functionality clears all stored credentials

## Security Features
- Role-based access control (RBAC)
- Frontend guards prevent unauthorized navigation
- Backend permission checks on all endpoints
- Subscription status enforcement
- Payment proof verification workflow

## Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Responsive typography and spacing
- Mobile navbar with collapsible menu
- Touch-friendly interactive elements

## File Structure Summary
```
legendary_frontend/
├── index.html              # Landing page
├── login.html              # Login page
├── register.html           # Registration page
├── dashboard.html          # Main dashboard (role-specific)
├── marketplace.html        # Product browsing (customers)
├── add-product.html        # Product creation (merchants)
├── admin-users.html        # User management (admins)
├── admin-plans.html        # Plan management (admins)
├── style.css               # Global styling
└── script.js               # Shared animations and utilities
```

## Notes
- All pages share the same style.css for consistent branding
- script.js provides shared functionality (cursor, animations, Three.js)
- Each page has inline JavaScript for page-specific API calls
- Design maintains the legendary theme with premium marketplace aesthetics
- No changes to existing styling or animations
