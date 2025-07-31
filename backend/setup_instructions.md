# MySQL Database Setup Instructions

## Prerequisites
1. Install MySQL Server on your system
2. Install Python 3.8+
3. Install pip

## Setup Steps

### 1. Install MySQL Server
- Download and install MySQL from https://dev.mysql.com/downloads/mysql/
- Remember your root password during installation

### 2. Create Database
```sql
-- Open MySQL Command Line or MySQL Workbench
-- Run the database_setup.sql file:
source database_setup.sql;
```

### 3. Update Environment Variables
Edit the `.env` file and update your MySQL credentials:
```
DB_PASSWORD=your_actual_mysql_root_password
```

### 4. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 5. Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Django Server
```bash
python manage.py runserver
```

## API Endpoints
- GET `/api/pets/` - Get all pets
- POST `/api/pets/create/` - Create new pet
- GET `/api/adoptions/` - Get all adoption requests
- POST `/api/adoptions/create/` - Create adoption request
- PUT `/api/adoptions/<id>/update/` - Update adoption status

## Database Tables
- `pets` - Pet information
- `shelters` - Shelter information
- `users` - User accounts
- `adoption_requests` - Adoption applications

## Troubleshooting
1. If you get MySQL connection errors, check your credentials in `.env`
2. Make sure MySQL service is running
3. Verify database `pet_adoption_db` exists
4. Check if port 3306 is available