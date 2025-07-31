# 🐾 MySQL Workbench Guide - Pet Adoption Platform

## 📋 **Step-by-Step Instructions**

### **1. Open MySQL Workbench**

- Launch MySQL Workbench on your computer
- If not installed, download from: https://dev.mysql.com/downloads/workbench/

### **2. Connect to Your Database**

- Click **"Database"** → **"Connect to Database"**
- Or click the **"+"** icon to create a new connection

### **Connection Settings:**

```
Hostname: localhost (or 127.0.0.1)
Port: 3306
Username: root (or your MySQL username)
Password: (your MySQL password)
Database: pet_adoption_db (or your database name)
```

### **3. Test Connection**

- Click **"Test Connection"** to verify it works
- Click **"OK"** to connect

### **4. Open SQL Editor**

- Click **"File"** → **"New Query Tab"**
- Or press **Ctrl+T**

### **5. Copy and Paste Queries**

- Open the file `mysql_workbench_queries.sql`
- Copy individual queries and paste them into the SQL editor
- Press **Ctrl+Enter** to execute each query

---

## 🔍 **Quick Queries to Start With**

### **View All Users:**

```sql
SELECT
    u.id, u.username, u.email, u.first_name, u.last_name,
    up.is_shelter, up.shelter_name
FROM auth_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
ORDER BY u.id;
```

### **View Only Shelter Users:**

```sql
SELECT
    u.username, u.email, up.shelter_name, up.shelter_description
FROM auth_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE up.is_shelter = 1
ORDER BY u.id;
```

### **View All Pets:**

```sql
SELECT
    p.name, p.pet_type, p.breed, p.age, p.status,
    u.username as owner
FROM pets_pet p
LEFT JOIN auth_user u ON p.owner_id = u.id
ORDER BY p.id;
```

### **View Adoption Requests:**

```sql
SELECT
    ar.status, ar.reason,
    u.username as requester,
    p.name as pet_name
FROM adoption_adoptionrequest ar
LEFT JOIN auth_user u ON ar.user_id = u.id
LEFT JOIN pets_pet p ON ar.pet_id = p.id
ORDER BY ar.id;
```

---

## 📊 **Database Structure**

### **Main Tables:**

- `auth_user` - All users (regular + shelters)
- `accounts_userprofile` - User profiles (shelter info)
- `pets_pet` - All pets in the system
- `adoption_adoptionrequest` - Adoption requests
- `chat_message` - Chat messages between users

### **Key Relationships:**

- `auth_user.id` → `accounts_userprofile.user_id`
- `auth_user.id` → `pets_pet.owner_id`
- `auth_user.id` → `adoption_adoptionrequest.user_id`
- `pets_pet.id` → `adoption_adoptionrequest.pet_id`

---

## 🎯 **What You'll See**

### **Users Table:**

- **10 total users** (5 regular + 5 shelters)
- **Shelter users:** testshelter, newshelter, testshelter2, finaltest, Harry
- **Regular users:** admin, john_doe, jane_smith, mike_wilson, ronish

### **Pets Table:**

- **5 total pets** (3 dogs + 2 cats)
- **Available:** Buddy (dog), Whiskers (cat)
- **Pending:** Max (dog), Luna (cat)
- **Adopted:** Charlie (dog)

### **Adoption Requests:**

- **4 total requests** (3 pending + 1 approved)
- **Pending:** john_doe → Buddy, admin → Luna, ronish → Max
- **Approved:** jane_smith → Whiskers

---

## ⚠️ **Troubleshooting**

### **If Connection Fails:**

1. **Check MySQL Service:**

   ```bash
   # Windows
   services.msc
   # Look for "MySQL" service and start it
   ```

2. **Check Database Name:**

   ```sql
   SHOW DATABASES;
   ```

3. **Check Table Names:**
   ```sql
   USE your_database_name;
   SHOW TABLES;
   ```

### **If Tables Don't Exist:**

- Make sure Django migrations are applied:
  ```bash
  python manage.py migrate
  ```

### **If Data is Empty:**

- Check if you're connected to the right database
- Verify the database has data by running the Python checker:
  ```bash
  python check_database_status.py
  ```

---

## 🚀 **Quick Start Commands**

### **1. View All Data:**

```sql
-- Copy this entire block and run it
SELECT 'Users' as table_name, COUNT(*) as count FROM auth_user
UNION ALL
SELECT 'Pets' as table_name, COUNT(*) as count FROM pets_pet
UNION ALL
SELECT 'Adoption Requests' as table_name, COUNT(*) as count FROM adoption_adoptionrequest;
```

### **2. View Shelter Users:**

```sql
SELECT username, email, shelter_name, shelter_description
FROM auth_user u
JOIN accounts_userprofile up ON u.id = up.user_id
WHERE up.is_shelter = 1;
```

### **3. View Available Pets:**

```sql
SELECT name, pet_type, breed, age, status
FROM pets_pet
WHERE status = 'available';
```

---

## 📝 **Notes**

- **Database Type:** Currently using SQLite (not MySQL)
- **File Location:** `pet_adoption.db` in your project folder
- **To Switch to MySQL:** Update `settings.py` database configuration
- **Backup:** Always backup your database before making changes

**Happy Database Exploring! 🐾**
