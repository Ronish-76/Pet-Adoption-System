# 🐾 Pet Adoption Platform - API Documentation

## 📋 Overview

This API provides comprehensive functionality for a pet adoption platform, including user management, pet listings, adoption requests, and messaging.

**Base URL**: `http://localhost:8000/api/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login

```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Refresh Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### Authorization Header

For authenticated requests, include the JWT token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

---

## 👤 User Management (`/api/accounts/`)

### Register User

```http
POST /api/accounts/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "password2": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
        "phone_number": "+1234567890",
        "city": "New York",
        "state": "NY",
        "bio": "I love animals!"
    }
}
```

### Login User

```http
POST /api/accounts/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}
```

### Get User Profile

```http
GET /api/accounts/profile/
Authorization: Bearer <token>
```

### Update User Profile

```http
PUT /api/accounts/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "profile": {
        "phone_number": "+1234567890",
        "city": "Los Angeles",
        "state": "CA"
    }
}
```

### Change Password

```http
PUT /api/accounts/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
    "old_password": "current_password",
    "new_password": "new_secure_password"
}
```

### Get User Info

```http
GET /api/accounts/user-info/
Authorization: Bearer <token>
```

### Logout

```http
POST /api/accounts/logout/
Authorization: Bearer <token>
Content-Type: application/json

{
    "refresh_token": "your_refresh_token"
}
```

---

## 🐕 Pet Management (`/api/pets/`)

### List All Pets

```http
GET /api/pets/
```

**Query Parameters:**

- `search`: Search in name, breed, or description
- `pet_type`: Filter by pet type (dog, cat, bird, fish, rabbit, other)
- `gender`: Filter by gender (male, female, unknown)
- `status`: Filter by status (available, adopted, pending)
- `min_age`: Minimum age filter
- `max_age`: Maximum age filter
- `ordering`: Order by (name, age, created_at)

### Get Featured Pets

```http
GET /api/pets/featured/
```

### Get Pet Details

```http
GET /api/pets/{pet_id}/
```

### Create Pet (Admin Only)

```http
POST /api/pets/create/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
    "name": "Buddy",
    "pet_type": "dog",
    "breed": "Golden Retriever",
    "age": 3,
    "gender": "male",
    "description": "Friendly and energetic dog",
    "image": <file>
}
```

### Update Pet (Admin Only)

```http
PUT /api/pets/{pet_id}/update/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
    "name": "Buddy",
    "pet_type": "dog",
    "breed": "Golden Retriever",
    "age": 4,
    "gender": "male",
    "description": "Updated description",
    "image": <file>
}
```

### Delete Pet (Admin Only)

```http
DELETE /api/pets/{pet_id}/delete/
Authorization: Bearer <token>
```

### Advanced Pet Search

```http
POST /api/pets/search/
Authorization: Bearer <token>
Content-Type: application/json

{
    "search": "golden retriever",
    "pet_type": "dog",
    "gender": "male",
    "min_age": 1,
    "max_age": 5,
    "ordering": "age"
}
```

### Get Pet Statistics (Admin Only)

```http
GET /api/pets/statistics/
Authorization: Bearer <token>
```

---

## 🏠 Adoption Management (`/api/adoptions/`)

### List User's Adoption Requests

```http
GET /api/adoptions/
Authorization: Bearer <token>
```

**Query Parameters:**

- `status`: Filter by status (pending, approved, rejected)
- `ordering`: Order by (created)

### Get Adoption Request Details

```http
GET /api/adoptions/{request_id}/
Authorization: Bearer <token>
```

### Create Adoption Request

```http
POST /api/adoptions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "pet_id": 1,
    "reason": "I have a large backyard and experience with dogs. I can provide a loving home."
}
```

### Get User's Adoption History

```http
GET /api/adoptions/history/
Authorization: Bearer <token>
```

### Admin: List All Adoption Requests

```http
GET /api/adoptions/admin/
Authorization: Bearer <token>
```

### Admin: Update Adoption Request Status

```http
PUT /api/adoptions/admin/{request_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "approved"
}
```

### Admin: Get Adoption Statistics

```http
GET /api/adoptions/admin/statistics/
Authorization: Bearer <token>
```

### Admin: Bulk Update Adoption Requests

```http
POST /api/adoptions/admin/bulk-update/
Authorization: Bearer <token>
Content-Type: application/json

{
    "adoption_ids": [1, 2, 3],
    "status": "approved"
}
```

---

## 💬 Chat System (`/api/chat/`)

### List Messages with User

```http
GET /api/chat/messages/?user_id=2
Authorization: Bearer <token>
```

### Send Message

```http
POST /api/chat/messages/
Authorization: Bearer <token>
Content-Type: application/json

{
    "receiver_id": 2,
    "content": "Hello! I'm interested in adopting your pet."
}
```

### List Conversations

```http
GET /api/chat/conversations/
Authorization: Bearer <token>
```

### List Chat Users

```http
GET /api/chat/users/
Authorization: Bearer <token>
```

### Get Unread Message Count

```http
GET /api/chat/unread-count/
Authorization: Bearer <token>
```

### Mark Messages as Read

```http
POST /api/chat/mark-read/
Authorization: Bearer <token>
Content-Type: application/json

{
    "sender_id": 2
}
```

### Delete Message

```http
DELETE /api/chat/messages/{message_id}/delete/
Authorization: Bearer <token>
```

### Get Chat Statistics

```http
GET /api/chat/statistics/
Authorization: Bearer <token>
```

---

## 📊 Response Formats

### Success Response

```json
{
  "message": "Operation successful",
  "data": {
    // Response data
  }
}
```

### Error Response

```json
{
  "error": "Error message",
  "details": {
    // Additional error details
  }
}
```

### Pagination Response

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/pets/?page=2",
  "previous": null,
  "results": [
    // Items
  ]
}
```

---

## 🔧 Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## 📝 Data Models

### Pet

```json
{
  "id": 1,
  "name": "Buddy",
  "pet_type": "dog",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "male",
  "description": "Friendly and energetic dog",
  "status": "available",
  "image": "http://localhost:8000/media/pets/buddy.jpg",
  "image_url": "http://localhost:8000/media/pets/buddy.jpg",
  "owner": {
    "id": 1,
    "username": "shelter_admin",
    "first_name": "Admin",
    "last_name": "User"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Adoption Request

```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "pet": {
    "id": 1,
    "name": "Buddy",
    "pet_type": "dog",
    "breed": "Golden Retriever",
    "age": 3,
    "image": "http://localhost:8000/media/pets/buddy.jpg"
  },
  "reason": "I have a large backyard and experience with dogs.",
  "status": "pending",
  "status_display": "Pending",
  "created": "2024-01-15T11:00:00Z"
}
```

### Message

```json
{
  "id": 1,
  "sender": {
    "id": 2,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "receiver": {
    "id": 1,
    "username": "shelter_admin",
    "first_name": "Admin",
    "last_name": "User"
  },
  "content": "Hello! I'm interested in adopting your pet.",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

---

## 🚀 Getting Started

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**

   ```bash
   python manage.py runserver
   ```

5. **Access API Documentation**
   - Swagger UI: `http://localhost:8000/swagger/`
   - ReDoc: `http://localhost:8000/redoc/`

---

## 🔒 Security Notes

- All sensitive endpoints require authentication
- JWT tokens expire after 60 minutes (access) and 1 day (refresh)
- File uploads are restricted to image files
- Input validation is performed on all endpoints
- Rate limiting is recommended for production

---

## 📞 Support

For API support or questions, please contact the development team or refer to the Swagger documentation at `/swagger/`.
