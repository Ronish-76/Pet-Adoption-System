# 🐾 MySQL Setup Guide for Pet Adoption Platform

## 📋 Prerequisites

### Option 1: Install MySQL Server

1. **Download MySQL Community Server** from [mysql.com](https://dev.mysql.com/downloads/mysql/)
2. **Install MySQL** with default settings
3. **Set root password** during installation

### Option 2: Use XAMPP/WAMP (Recommended for Windows)

1. **Download XAMPP** from [apachefriends.org](https://www.apachefriends.org/)
2. **Install XAMPP** with MySQL included
3. **Start MySQL service** from XAMPP Control Panel

### Option 3: Use Docker

```bash
docker run --name mysql-pet-adoption -e MYSQL_ROOT_PASSWORD=your_password -e MYSQL_DATABASE=pet_adoption_db -p 3306:3306 -d mysql:8.0
```

## 🔧 Setup Steps

### 1. Start MySQL Service

- **XAMPP**: Open XAMPP Control Panel → Start MySQL
- **Standalone MySQL**: Start MySQL service
- **Docker**: Container should be running

### 2. Create Database

```sql
CREATE DATABASE IF NOT EXISTS pet_adoption_db;
USE pet_adoption_db;
```

### 3. Update .env File

Edit the `.env` file in your project root:

```env
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-key-2024

# MySQL Database Configuration
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Run Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Load Sample Data

```bash
python create_sample_data.py
```

## 🚀 Start the Application

```bash
python manage.py runserver 8000
```

## 🔍 Troubleshooting

### MySQL Connection Issues

1. **Check if MySQL is running**:

   ```bash
   # Windows
   net start mysql

   # Check if port 3306 is open
   netstat -an | findstr 3306
   ```

2. **Test MySQL connection**:

   ```bash
   mysql -u root -p
   ```

3. **Common Issues**:
   - **Access denied**: Check username/password in .env
   - **Connection refused**: MySQL service not running
   - **Database doesn't exist**: Create database first

### Django Database Issues

1. **Check Django settings**:

   ```bash
   python manage.py check
   ```

2. **Test database connection**:

   ```bash
   python manage.py dbshell
   ```

3. **Reset migrations** (if needed):
   ```bash
   python manage.py migrate --fake-initial
   ```

## 📊 Verify Setup

### 1. Check API Endpoints

- Visit: http://localhost:8000/api/pets/
- Should return JSON with pets data

### 2. Check Admin Panel

- Visit: http://localhost:8000/admin/
- Login with superuser credentials

### 3. Check Database

```bash
python manage.py shell
```

```python
from pets.models import Pet
print(f"Total pets: {Pet.objects.count()}")
```

## 🎯 Next Steps

1. **Frontend Integration**: Open `frontend/landing.html` in browser
2. **API Testing**: Use `frontend/test_api.html`
3. **User Registration**: Test user signup/login
4. **Pet Management**: Add/edit pets via admin panel

## 📞 Support

If you encounter issues:

1. Check MySQL service status
2. Verify .env configuration
3. Test database connection
4. Review Django error logs
