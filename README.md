# 🛒 Multi-Tenant E-Commerce Platform

A Shopify-like marketplace built with Django that allows users to create and manage their own online stores with custom domains.

## ✨ Features

- 🏪 **Multi-Store Marketplace** - Users can create unlimited stores
- 🎨 **Theme Customization** - Custom colors, fonts, and logos
- 🌐 **Custom Domain Support** - Each store can have its own domain
- 📦 **Product Management** - Full CRUD for products and categories
- 📊 **Store Dashboard** - Analytics, orders, and inventory management
- 🔒 **Domain Separation** - Customer site and admin panel are separate
- 💳 **Shopping Cart & Checkout** - Complete e-commerce functionality

## 🚀 Live Demo

**Deployed URL**: Coming soon!

## 📸 Screenshots

- Marketplace homepage
- Store customization
- Product management dashboard

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (dev), PostgreSQL (production)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Deployment**: Render.com / PythonAnywhere

## 📦 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ecom-platform.git
cd ecom-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to Render

```bash
git init
git add .
git commit -m "Initial commit"
git push
```

Then connect your repo on Render.com!

## 📝 Usage

### For Store Owners:

1. **Create Account**: Register on the platform
2. **Create Store**: Click "Create Your Store"
3. **Customize**: Go to Dashboard → Customize Store
4. **Add Products**: Dashboard → Products → Add Product
5. **Manage Orders**: View and update order status

### For Customers:

1. **Browse Stores**: Visit marketplace homepage
2. **Shop Products**: Click on any store
3. **Add to Cart**: Select products and checkout
4. **Track Orders**: View order history

## 🔐 Admin Access

```
URL: /admin/
Default Username: admin
Default Password: admin123 (change immediately!)
```

## 🎨 Customization

Each store can customize:
- Primary & secondary colors
- Background & text colors
- Font family
- Logo
- Layout width (boxed/full)

## 📂 Project Structure

```
ecom/
├── shop/              # Main shop app
├── dashboard/         # Store owner dashboard
├── myshop/           # Project settings
├── templates/        # HTML templates
├── static/           # Static files
├── media/            # Uploaded files
└── requirements.txt  # Dependencies
```

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📄 License

MIT License

## 👨‍💻 Author

Your Name

## 🙏 Acknowledgments

- Django documentation
- Bootstrap team
- Shopify for inspiration
