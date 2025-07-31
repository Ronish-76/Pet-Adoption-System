# Reset Database and Start Fresh

## 1. Clear MySQL Database
Run this in MySQL Workbench or command line:
```sql
USE pet_adoption_db;

DELETE FROM adoption_requests;
DELETE FROM favorites;
DELETE FROM notifications;
DELETE FROM pet_medical_info;
DELETE FROM pets;

ALTER TABLE adoption_requests AUTO_INCREMENT = 1;
ALTER TABLE favorites AUTO_INCREMENT = 1;
ALTER TABLE notifications AUTO_INCREMENT = 1;
ALTER TABLE pet_medical_info AUTO_INCREMENT = 1;
ALTER TABLE pets AUTO_INCREMENT = 1;
```

## 2. Clear Browser Data
Open browser console (F12) and run:
```javascript
localStorage.clear();
sessionStorage.clear();
console.log('Browser data cleared!');
```

## 3. Restart Django Server
```bash
cd backend
python manage.py runserver
```

## 4. Verify Clean State
- Visit pets page - should show "No pets posted yet"
- Visit adoptions page - should show no adoption requests
- Shelter dashboard should be empty

All data cleared - ready to start fresh!