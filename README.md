# 🧪 VaxCare – Vaccination Management System (Django REST Framework)

**VaxCare** is a **Vaccination Management System** built with **Django REST Framework (DRF)**.  
It provides separate features for **Patients, Doctors, and Admins**.  

---

## 🚀 Features

### 🔐 Authentication & User Management (`auth_app`)
- Custom User Model (extended from `AbstractUser`)
- User Roles: **Patient**, **Doctor**, **Admin**
- User Registration with role-based validations:
  - Patients → **NID is mandatory**  
  - Doctors → **Specialization, contact details, and profile picture required**
- JWT Authentication (via **Djoser + SimpleJWT**)
- User profile view & update
- Password change endpoint
- Role-based permissions:
  - `IsPatient`, `IsDoctor`, `IsAdmin`

---

### 💉 Vaccine Management (`vaccine_app`)
- **Vaccine Model**: Name, description, and created_by (Doctor/Admin)  
- **Vaccination Schedule**: Create schedule with date, time, and location  
- **Dose Booking**:
  - Patients can book doses for themselves  
  - Second dose is automatically calculated (default: 28 days later)  
- **Campaigns**:
  - Create campaigns with multiple vaccines  
  - Configurable dose interval days  
  - Only Doctors can create campaigns  
- **Campaign Booking**: Patients can book campaigns  
- **Campaign Reviews**:
  - Patients can review only the campaigns they booked  
  - One review per patient per campaign  

---

### API Documentation
- **Swagger UI** → `/swagger/`  
- **Redoc UI** → `/redoc/`  

---

## 🛠️ Tech Stack
- **Backend**: Django, Django REST Framework  
- **Authentication**: Djoser + JWT (SimpleJWT)  
- **Database**: PostgreSQL / SQLite (configurable)  
- **API Docs**: drf-yasg (Swagger & Redoc)  

---


---

## 🔑 API Endpoints

### Auth (`/auth/`)
- `POST /auth/users/` → Register  
- `POST /auth/jwt/create/` → Login (JWT)  
- `POST /auth/jwt/refresh/` → Refresh token  
- `GET /auth/profile/` → Get/Update profile  
- `POST /auth/change-password/` → Change password  
- `GET /auth/doctors/` → List doctors  

### Vaccines & Campaigns (`/api/`)
- `GET /api/vaccines/` → List vaccines  
- `POST /api/vaccines/` → Add vaccine (Doctor only)  
- `GET /api/schedules/` → List schedules  
- `POST /api/schedules/` → Create schedule (Doctor only)  
- `POST /api/dose-bookings/` → Book dose (Patient only)  
- `GET /api/campaigns/` → List campaigns  
- `POST /api/campaigns/` → Create campaign (Doctor only)  
- `POST /api/campaigns-booking/` → Book campaign (Patient only)  
- `POST /api/campaign-reviews/` → Review campaign (Patient only)  

### Interactive API docs available via Swagger UI at:

- `http://localhost:8000/swagger/`

### Alternative documentation using Redoc at:

- `http://localhost:8000/redoc/`
---

## ⚙️ Installation & Setup

1. **Clone repository**
```
bash
git clone https://github.com/yourusername/vaxcare.git
cd vaxcare
```
## Create & activate virtual environment

```python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

## Install dependencies

```
pip install -r requirements.txt
```

## Run migrations

```
python manage.py migrations

python manage.py migrate
```

## Create superuser

```
python manage.py createsuperuser
```

## Run the server

```
python manage.py runserver
```