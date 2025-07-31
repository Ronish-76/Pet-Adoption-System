# ✅ Software Requirements Specification (SRS)

**Project Title**: _Pet Adoption and Management System_
**Prepared For**: Academic / Capstone Project or Real-World Deployment
**Tech Stack**: Django + Django REST Framework (Backend), React or Next.js (Frontend), PostgreSQL or MySQL (DB), JWT Auth, Figma (UI/UX)

---

## 1. **Introduction**

### 1.1 Purpose

This system provides a digital platform for **pet seekers** to browse adoptable pets and submit adoption requests, while allowing **shelters/admins** to manage pets and track adoptions efficiently.

### 1.2 Scope

- Pet listings with filters and search
- Adoption request form & status tracking
- Authentication system (User, Admin)
- Admin dashboard for managing pets and approvals
- REST API for integration with frontend
- Mobile-responsive UI

### 1.3 Definitions

| Term    | Meaning                                  |
| ------- | ---------------------------------------- |
| Adopter | A registered user who browses and adopts |
| Shelter | Admin account managing pet listings      |
| Pet     | An animal available for adoption         |

---

## 2. **Overall Description**

### 2.1 Product Perspective

The system is a **web-based, responsive platform** built with a clear separation of concerns:

- REST API (backend)
- Responsive UI (frontend)
- Auth-protected admin views

### 2.2 User Classes & Characteristics

| User Role | Capabilities                                             |
| --------- | -------------------------------------------------------- |
| Guest     | View pet listings                                        |
| Adopter   | Register/login, adopt a pet, view request status         |
| Admin     | Login, manage pets, view/approve adoptions, manage users |

### 2.3 Assumptions & Dependencies

- Requires internet access
- Admin approval is required to finalize adoption
- Pets will be listed manually by shelters

---

## 3. **Functional Requirements**

### 🐾 User Module

- Register new account
- Login with JWT authentication
- View/edit user profile
- Submit & view adoption requests

### 🐾 Pet Module

- View all pets (grid/list view)
- Filter pets by species, location, availability
- View detailed info for each pet

### 🐾 Admin Module

- Add/edit/delete pets
- View list of adopters
- View/approve/reject adoption requests
- Dashboard with basic analytics

### 🐾 Adoption Module

- Form with fields: adopter info, reason, pet selected
- Auto notification after admin action
- Status: Pending, Approved, Rejected

### 🐾 System Module

- Email notifications for adoption updates (optional)
- Swagger/Redoc API documentation
- Protected endpoints with permission classes

---

## 4. **Non-Functional Requirements**

| Category        | Specification                                     |
| --------------- | ------------------------------------------------- |
| Security        | JWT-based auth, role-based permissions            |
| Usability       | Mobile-friendly design, clean UX                  |
| Scalability     | RESTful structure supports future expansion       |
| Maintainability | Modular Django apps, reusable frontend components |
| Documentation   | Swagger + README + OpenAPI format                 |

---

## 5. **System Models**

### 5.1 Entity Relationship Diagram (Simplified)

```
User --< AdoptionRequest >-- Pet
Pet --< AddedBy >-- Admin
```

### 5.2 Major Routes/Endpoints (MVP)

| URL                     | Method  | Description                     |
| ----------------------- | ------- | ------------------------------- |
| `/api/register/`        | POST    | Register a new user             |
| `/api/login/`           | POST    | Login, returns JWT tokens       |
| `/api/pets/`            | GET     | View all pets                   |
| `/api/pets/{id}/`       | GET     | View single pet                 |
| `/api/adoptions/`       | POST    | Submit adoption request         |
| `/api/adoptions/`       | GET     | User’s adoption requests        |
| `/api/admin/pets/`      | CRUD    | Admin pet management            |
| `/api/admin/adoptions/` | GET     | Admin view of adoption requests |
| `/api/profile/`         | GET/PUT | View/update profile info        |

---

# 👤 User Stories (Brief Format)

### 🧍 As a **Guest**

- I want to **view pets** without logging in
- So that I can decide whether to register

### 👨‍🦱 As an **Adopter**

- I want to **create an account and login**
- So that I can adopt pets
- I want to **view pet details**
- So I can choose the right pet
- I want to **submit an adoption request**
- So that I can start the process
- I want to **track my adoption status**
- So I know if my request is approved

### 👩‍💼 As an **Admin (Shelter Staff)**

- I want to **login securely**
- So I can manage the platform
- I want to **add/edit/delete pet profiles**
- So I can keep listings updated
- I want to **view adoption requests**
- So I can review and approve/reject them

---

# ✅ Deliverables for MVP

- Figma UI for all user roles (guest, adopter, admin)
- Django backend with JWT authentication
- REST API for all modules (pets, users, adoptions)
- Fully responsive frontend (React or Next.js)
- Admin interface with pet/adoption management
- Basic test coverage
- README, Swagger docs, and Postman collection

---

### 10. Recommended Enhancements & Production Readiness

These features and configurations enhance the core MVP for better usability, security, or future deployment, though not strictly required for a minimal local setup.

- **Chat Module**:

  - **Detail**: Implemented a `chat` app with `Message` model, serializer, viewset, and URL configuration for direct messaging between users/shelters.
  - **Benefit**: Adds a communication feature that enhances user experience.

- **Enhanced Admin Interface (`django-jazzmin`)**:

  - **Detail**: Integrated `django-jazzmin` for a modern, responsive, and user-friendly Django administration panel.
  - **Benefit**: Greatly improves the administrative experience for managing pets, users, and requests.

- **Comprehensive `REST_FRAMEWORK` and `SIMPLE_JWT` Settings**:

  - **Detail**: Configured `REST_FRAMEWORK` with default pagination and more detailed `SIMPLE_JWT` settings (e.g., token lifetimes, refresh token rotation).
  - **Benefit**: Provides a more robust and secure API foundation, ready for production use and advanced authentication flows.

- **Production-Oriented Dependencies**:
  - **Detail**: Included `psycopg2-binary` (PostgreSQL adapter), `gunicorn` (production WSGI server), `whitenoise` (static files serving for production), and `python-dotenv` (environment variable management).
  - **Benefit**: Essential for deploying the application to a production server reliably.

---
