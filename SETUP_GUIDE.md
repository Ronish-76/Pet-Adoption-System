# Pet Adoption Platform - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or 8.0+
- Node.js (for frontend development)

### 1. Database Setup
```sql
-- Create database
CREATE DATABASE pet_adoption_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional)
CREATE USER 'pet_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON pet_adoption_db.* TO 'pet_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Environment Configuration
Update `.env` file with your database credentials:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Setup Script
```bash
python start_server.py
```

This will:
- Create database migrations
- Run migrations
- Create a superuser (admin/admin123)
- Collect static files
- Start the development server

## 🔧 Manual Setup (Alternative)

If the automatic setup doesn't work:

```bash
# Create migrations
python manage.py makemigrations accounts
python manage.py makemigrations pets
python manage.py makemigrations adoption
python manage.py makemigrations chat

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver 8000
```

## 📱 Frontend Setup

The frontend is static HTML/CSS/JS files located in the `frontend/` directory.

### Serving Frontend
1. **Development**: Open `frontend/landing.html` in your browser
2. **Production**: Serve through a web server (nginx, Apache, etc.)

### Frontend Structure
```
frontend/
├── pages/          # HTML pages
├── js/            # JavaScript files
├── css/           # Stylesheets
└── assets/        # Images and other assets
```

## 🔐 Default Credentials

### Admin Panel
- URL: http://localhost:8000/admin/
- Username: admin
- Password: admin123

### Test User (create manually)
- Username: testuser
- Password: testpass123

## 🌐 API Endpoints

### Authentication
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token

### Pets
- `GET /api/pets/` - List pets
- `GET /api/pets/{id}/` - Pet details
- `GET /api/pets/featured/` - Featured pets

### Accounts
- `POST /api/accounts/register/` - Register
- `GET /api/accounts/profile/` - User profile

### Adoptions
- `GET /api/adoptions/` - User's adoption requests
- `POST /api/adoptions/` - Create adoption request

## 📚 API Documentation

Visit http://localhost:8000/swagger/ for interactive API documentation.

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Migration Errors**
   - Delete migration files and recreate: `find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`
   - Run `python manage.py makemigrations` again

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

4. **CORS Errors**
   - Ensure `django-cors-headers` is installed
   - Check CORS settings in `settings.py`

5. **JWT Token Issues**
   - Check token expiration settings
   - Verify `SECRET_KEY` is consistent

### Development Tips

1. **Use Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Debug Mode**
   - Set `DEBUG=True` in `.env` for development
   - Set `DEBUG=False` for production

3. **Database Reset**
   ```bash
   python manage.py flush
   python manage.py migrate
   ```

## 🚀 Production Deployment

### Security Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Set up proper CORS origins
- [ ] Use environment variables for sensitive data
- [ ] Set up proper logging
- [ ] Configure static file serving
- [ ] Set up database backups

### Recommended Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: MySQL 8.0+
- **Cache**: Redis
- **Process Manager**: Supervisor

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review Django logs
3. Check browser console for frontend errors
4. Verify database connectivity

## 🔄 Updates

To update the project:
1. Pull latest changes
2. Install new requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Restart server