# Healthcare Backend API

A RESTful healthcare management backend built with **Django, Django REST Framework, PostgreSQL, and JWT authentication**.

The API provides authentication and CRUD operations for:

* Users
* Patients
* Doctors
* Patient–Doctor mappings

The project also implements authentication, authorization, user-level data isolation, pagination, duplicate mapping prevention, and automated API tests.

---

## Tech Stack

* **Python**
* **Django**
* **Django REST Framework (DRF)**
* **PostgreSQL**
* **Simple JWT**
* **psycopg2**
* **python-dotenv / environment variables**

---

# 1. Features

### Authentication

* User registration
* JWT-based login
* Access token refresh
* Email-based authentication

### Patients

* Create patients
* List only patients created by the authenticated user
* Retrieve a patient's details
* Update patients
* Partially update patients
* Delete patients

### Doctors

* Create doctors
* List all doctors
* Retrieve doctors
* Update doctors
* Partially update doctors
* Delete doctors

### Patient–Doctor Mapping

* Assign a doctor to a patient
* Prevent duplicate doctor assignments
* List the authenticated user's mappings
* Get doctors assigned to a specific patient
* Remove a patient–doctor mapping

### Security

* JWT authentication
* Protected patient, doctor and mapping endpoints
* User-level patient isolation
* Users cannot assign doctors to patients they do not own
* Unauthorized access is rejected
* Cross-user patient access returns `404 Not Found`

### Other

* Pagination — 20 records per page
* PostgreSQL database
* Automated test suite

---

# 2. Project Structure

```text
healthcare-backend/
│
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
│
├── <project_name>/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── <app_name>/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
└── ...
```

---

# 3. Prerequisites

Before running the project, make sure the following are installed:

* Python 3.x
* PostgreSQL
* Git
* pip

Verify Python:

```bash
python --version
```

Verify PostgreSQL:

```bash
psql --version
```

---

# 4. Installation

## Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd healthcare-backend
```

---

## Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Environment Configuration

Create a `.env` file in the project root.

Example:

```env
DJANGO_SECRET_KEY=change-me-to-a-long-random-string
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=healthcare
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Important

For production, replace `DJANGO_SECRET_KEY` with a strong random secret.

Do not commit `.env` to Git.

---

# 6. PostgreSQL Setup

Create a PostgreSQL database named:

```text
healthcare
```

You can create it using `psql`:

```bash
createdb healthcare
```

Or create it through **pgAdmin**:

```text
Servers
→ PostgreSQL
→ Databases
→ Right Click
→ Create
→ Database
```

Database name:

```text
healthcare
```

The PostgreSQL credentials must match the values in `.env`.

For the example configuration:

```text
Database: healthcare
User:     postgres
Password: postgres
Host:     localhost
Port:     5432
```

---

# 7. Run Migrations

After PostgreSQL is running:

```bash
python manage.py migrate
```

---

# 8. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

or:

```text
http://localhost:8000/
```

---

# 9. Authentication

All patient, doctor and mapping endpoints require JWT authentication.

After logging in, copy the `access` token.

For protected requests, send:

```http
Authorization: Bearer <access_token>
```

In Postman:

```text
Authorization
→ Type: Bearer Token
→ Token: <access_token>
```

---

# 10. API Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

---

# Authentication APIs

## 10.1 Register User

### POST

```http
/api/auth/register/
```

Full URL:

```text
http://127.0.0.1:8000/api/auth/register/
```

### Request Body

```json
{
    "name": "Asha Sharma",
    "email": "asha@example.com",
    "password": "Str0ngPass!23"
}
```

### Fields

| Field      | Type   | Required | Description          |
| ---------- | ------ | -------: | -------------------- |
| `name`     | string |      Yes | User's name          |
| `email`    | string |      Yes | User's email address |
| `password` | string |      Yes | User password        |

### Response

The endpoint returns the created user along with a JWT access/refresh pair.

Example:

```json
{
    "user": {
        "id": 1,
        "name": "Asha Sharma",
        "email": "asha@example.com"
    },
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

# 10.2 Login

### POST

```http
/api/auth/login/
```

Full URL:

```text
http://127.0.0.1:8000/api/auth/login/
```

### Request Body

```json
{
    "email": "asha@example.com",
    "password": "Str0ngPass!23"
}
```

### Response

```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

Save the `access` token for authenticated requests.

---

# 10.3 Refresh Access Token

### POST

```http
/api/auth/refresh/
```

Full URL:

```text
http://127.0.0.1:8000/api/auth/refresh/
```

### Request Body

```json
{
    "refresh": "<refresh_token>"
}
```

### Response

```json
{
    "access": "<new_access_token>"
}
```

---

# Patient APIs

All patient endpoints require:

```http
Authorization: Bearer <access_token>
```

---

# 11. Create Patient

### POST

```http
/api/patients/
```

Full URL:

```text
http://127.0.0.1:8000/api/patients/
```

### Request Body

```json
{
    "name": "Asha Sharma",
    "age": 28,
    "gender": "Female",
    "phone": "9876543210",
    "address": "Kolkata, West Bengal",
    "medical_history": "No known medical conditions"
}
```

### Fields

| Field             | Type    | Required | Description            |
| ----------------- | ------- | -------: | ---------------------- |
| `name`            | string  |      Yes | Patient's name         |
| `age`             | integer |      Yes | Patient's age          |
| `gender`          | string  |      Yes | Patient's gender       |
| `phone`           | string  |      Yes | Patient's phone number |
| `address`         | string  |      Yes | Patient's address      |
| `medical_history` | string  |      Yes | Medical history        |

### Do NOT send

```text
id
created_by
created_at
```

`id` and `created_at` are generated by the backend.

`created_by` is automatically set to the currently authenticated user.

### Example Response

```json
{
    "id": 1,
    "name": "Asha Sharma",
    "age": 28,
    "gender": "Female",
    "phone": "9876543210",
    "address": "Kolkata, West Bengal",
    "medical_history": "No known medical conditions",
    "created_by": 1,
    "created_at": "2026-09-06T12:00:00Z"
}
```

---

# 12. List My Patients

Returns only patients created by the authenticated user.

### GET

```http
/api/patients/
```

Full URL:

```text
http://127.0.0.1:8000/api/patients/
```

### Example Response

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Asha Sharma",
            "age": 28,
            "gender": "Female",
            "phone": "9876543210",
            "address": "Kolkata, West Bengal",
            "medical_history": "No known medical conditions",
            "created_by": 1,
            "created_at": "2026-09-06T12:00:00Z"
        }
    ]
}
```

---

# 13. Get Patient

### GET

```http
/api/patients/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/patients/1/
```

The patient must belong to the authenticated user.

If another user tries to access the patient:

```text
404 Not Found
```

---

# 14. Update Patient

### PUT

```http
/api/patients/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/patients/1/
```

### Request Body

```json
{
    "name": "Asha Sharma",
    "age": 29,
    "gender": "Female",
    "phone": "9123456789",
    "address": "New Town, Kolkata",
    "medical_history": "Asthma"
}
```

Do not send:

```text
created_by
created_at
```

---

# 15. Partially Update Patient

### PATCH

```http
/api/patients/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/patients/1/
```

You can update only the fields that need to change.

Example:

```json
{
    "phone": "9123456789"
}
```

---

# 16. Delete Patient

### DELETE

```http
/api/patients/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/patients/1/
```

Expected response:

```text
204 No Content
```

---

# Doctor APIs

All doctor endpoints require:

```http
Authorization: Bearer <access_token>
```

---

# 17. Create Doctor

### POST

```http
/api/doctors/
```

Full URL:

```text
http://127.0.0.1:8000/api/doctors/
```

### Request Body

```json
{
    "name": "Dr. Rajesh Kumar",
    "specialization": "Cardiology",
    "email": "rajesh.kumar@example.com",
    "phone": "9876501234",
    "experience_years": 12
}
```

### Fields

| Field              | Type    | Required | Description            |
| ------------------ | ------- | -------: | ---------------------- |
| `name`             | string  |      Yes | Doctor's name          |
| `specialization`   | string  |      Yes | Medical specialization |
| `email`            | string  |      Yes | Doctor's email         |
| `phone`            | string  |      Yes | Doctor's phone         |
| `experience_years` | integer |      Yes | Years of experience    |

### Do NOT send

```text
id
created_at
```

These are generated by the backend.

### Example Response

```json
{
    "id": 1,
    "name": "Dr. Rajesh Kumar",
    "specialization": "Cardiology",
    "email": "rajesh.kumar@example.com",
    "phone": "9876501234",
    "experience_years": 12,
    "created_at": "2026-09-06T12:10:00Z"
}
```

---

# 18. List Doctors

Returns all doctors.

### GET

```http
/api/doctors/
```

Full URL:

```text
http://127.0.0.1:8000/api/doctors/
```

---

# 19. Get Doctor

### GET

```http
/api/doctors/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/doctors/1/
```

---

# 20. Update Doctor

### PUT

```http
/api/doctors/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/doctors/1/
```

### Request Body

```json
{
    "name": "Dr. Rajesh Kumar",
    "specialization": "Cardiology",
    "email": "rajesh.kumar@example.com",
    "phone": "9876501234",
    "experience_years": 15
}
```

---

# 21. Partially Update Doctor

### PATCH

```http
/api/doctors/<id>/
```

Example:

```json
{
    "experience_years": 15
}
```

---

# 22. Delete Doctor

### DELETE

```http
/api/doctors/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/doctors/1/
```

Expected response:

```text
204 No Content
```

---

# Patient–Doctor Mapping APIs

Mappings connect a patient with a doctor.

All mapping endpoints require:

```http
Authorization: Bearer <access_token>
```

---

# 23. Assign Doctor to Patient

### POST

```http
/api/mappings/
```

Full URL:

```text
http://127.0.0.1:8000/api/mappings/
```

### Request Body

```json
{
    "patient": 1,
    "doctor": 1
}
```

### Fields

| Field     | Type    | Required | Description |
| --------- | ------- | -------: | ----------- |
| `patient` | integer |      Yes | Patient ID  |
| `doctor`  | integer |      Yes | Doctor ID   |

The patient must have been created by the authenticated user.

### Example Response

```json
{
    "id": 1,
    "patient": 1,
    "patient_name": "Asha Sharma",
    "doctor": 1,
    "doctor_name": "Dr. Rajesh Kumar",
    "created_at": "2026-09-06T12:20:00Z"
}
```

---

# 24. List My Mappings

### GET

```http
/api/mappings/
```

Full URL:

```text
http://127.0.0.1:8000/api/mappings/
```

Returns mappings belonging to patients created by the authenticated user.

### Example Response

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "Asha Sharma",
            "doctor": 1,
            "doctor_name": "Dr. Rajesh Kumar",
            "created_at": "2026-09-06T12:20:00Z"
        }
    ]
}
```

---

# 25. Get Doctors Assigned to a Patient

### GET

```http
/api/mappings/<patient_id>/
```

Example:

```text
http://127.0.0.1:8000/api/mappings/1/
```

### Important

For this endpoint:

```text
1 = patient ID
```

It is **not** the mapping ID.

The endpoint returns doctors assigned to that patient.

The patient must belong to the authenticated user.

---

# 26. Delete Mapping

### DELETE

```http
/api/mappings/<id>/
```

Example:

```text
http://127.0.0.1:8000/api/mappings/1/
```

### Important

For DELETE:

```text
1 = mapping ID
```

This is different from:

```text
GET /api/mappings/1/
```

where `1` represents the patient ID.

---

# 27. Pagination

Patient, doctor and mapping list endpoints are paginated.

The default page size is:

```text
20
```

### First page

```http
GET /api/patients/
```

### Second page

```http
GET /api/patients/?page=2
```

The same applies to doctors and mappings:

```text
/api/doctors/?page=2
/api/mappings/?page=2
```

---

# 28. Recommended API Testing Flow

For testing the complete application, use the following order.

## Step 1 — Register

```http
POST /api/auth/register/
```

```json
{
    "name": "Asha Sharma",
    "email": "asha@example.com",
    "password": "Str0ngPass!23"
}
```

---

## Step 2 — Login

```http
POST /api/auth/login/
```

```json
{
    "email": "asha@example.com",
    "password": "Str0ngPass!23"
}
```

Copy the returned:

```text
access
```

token.

---

## Step 3 — Create Patient

```http
POST /api/patients/
```

```json
{
    "name": "Asha Sharma",
    "age": 28,
    "gender": "Female",
    "phone": "9876543210",
    "address": "Kolkata, West Bengal",
    "medical_history": "No known medical conditions"
}
```

Save the returned:

```text
patient ID
```

---

## Step 4 — Create Doctor

```http
POST /api/doctors/
```

```json
{
    "name": "Dr. Rajesh Kumar",
    "specialization": "Cardiology",
    "email": "rajesh.kumar@example.com",
    "phone": "9876501234",
    "experience_years": 12
}
```

Save the returned:

```text
doctor ID
```

---

## Step 5 — Create Mapping

```http
POST /api/mappings/
```

```json
{
    "patient": 1,
    "doctor": 1
}
```

---

## Step 6 — Verify Mapping

```http
GET /api/mappings/
```

---

## Step 7 — Get Patient's Doctors

```http
GET /api/mappings/1/
```

Here `1` is the patient ID.

---

# 29. Authentication Header

For every protected request, use:

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Protected endpoints:

```text
POST   /api/patients/
GET    /api/patients/
GET    /api/patients/<id>/
PUT    /api/patients/<id>/
PATCH  /api/patients/<id>/
DELETE /api/patients/<id>/

POST   /api/doctors/
GET    /api/doctors/
GET    /api/doctors/<id>/
PUT    /api/doctors/<id>/
PATCH  /api/doctors/<id>/
DELETE /api/doctors/<id>/

POST   /api/mappings/
GET    /api/mappings/
GET    /api/mappings/<patient_id>/
DELETE /api/mappings/<id>/
```

---

# 30. Error Responses

The API uses standard HTTP status codes.

Common responses:

| Status | Meaning                                  |
| -----: | ---------------------------------------- |
|  `200` | Successful request                       |
|  `201` | Resource successfully created            |
|  `204` | Resource successfully deleted            |
|  `400` | Invalid request / validation error       |
|  `401` | Authentication required or invalid token |
|  `404` | Resource not found                       |
|  `405` | HTTP method not allowed                  |

### Example validation error

```json
{
    "email": [
        "Enter a valid email address."
    ]
}
```

---

# 31. Security / Authorization Behavior

### Patient ownership

Patients are associated with the user who created them.

A user can only:

* View their own patients
* Update their own patients
* Delete their own patients
* Assign doctors to their own patients

For example:

```text
User A
 └── Patient A

User B
 └── Patient B
```

User B cannot access Patient A.

The API returns:

```text
404 Not Found
```

rather than exposing the existence of another user's patient.

---

# 32. Duplicate Mapping Protection

The same doctor cannot be assigned to the same patient more than once.

Example:

First request:

```json
{
    "patient": 1,
    "doctor": 1
}
```

Successful.

Sending the same request again:

```json
{
    "patient": 1,
    "doctor": 1
}
```

returns a validation error:

```json
{
    "non_field_errors": [
        "This doctor is already assigned to this patient."
    ]
}
```

---

# 33. Testing Unauthenticated Access

Try:

```http
GET /api/patients/
```

without an Authorization header.

Expected:

```text
401 Unauthorized
```

The same applies to:

```text
/api/doctors/
/api/mappings/
```

---

# 34. Running Tests

Run the complete test suite:

```bash
python manage.py test
```

The test suite covers:

* User registration
* User login
* Patient creation
* Doctor creation
* Patient–doctor mapping
* Duplicate mapping rejection
* Cross-user isolation
* Unauthenticated access

### Test database

Django creates a separate test database when running tests.

The PostgreSQL user specified in `.env` must have permission to create test databases.

For the default configuration:

```text
POSTGRES_USER=postgres
```

make sure the `postgres` user has the required database privileges.

---

# 35. Quick API Check with cURL

## Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d "{\"name\":\"Asha\",\"email\":\"asha@example.com\",\"password\":\"Str0ngPass!23\"}"
```

## Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d "{\"email\":\"asha@example.com\",\"password\":\"Str0ngPass!23\"}"
```

Copy the access token from the response.

## Get Patients

```bash
curl http://127.0.0.1:8000/api/patients/ \
-H "Authorization: Bearer <access_token>"
```

---

# 36. Postman

The APIs can be tested using Postman.

Recommended collection structure:

```text
Healthcare Backend
│
├── Authentication
│   ├── Register
│   ├── Login
│   └── Refresh Token
│
├── Patients
│   ├── Create Patient
│   ├── List Patients
│   ├── Get Patient
│   ├── Update Patient
│   ├── Patch Patient
│   └── Delete Patient
│
├── Doctors
│   ├── Create Doctor
│   ├── List Doctors
│   ├── Get Doctor
│   ├── Update Doctor
│   ├── Patch Doctor
│   └── Delete Doctor
│
└── Mappings
    ├── Create Mapping
    ├── List Mappings
    ├── Get Patient Doctors
    └── Delete Mapping
```

For protected requests, configure:

```text
Authorization
Type: Bearer Token
Token: <access_token>
```

---

# 37. API Summary

| Method | Endpoint                      | Authentication | Purpose                  |
| ------ | ----------------------------- | -------------- | ------------------------ |
| POST   | `/api/auth/register/`         | No             | Register user            |
| POST   | `/api/auth/login/`            | No             | Login and get JWT        |
| POST   | `/api/auth/refresh/`          | No             | Refresh access token     |
| POST   | `/api/patients/`              | Yes            | Create patient           |
| GET    | `/api/patients/`              | Yes            | List own patients        |
| GET    | `/api/patients/<id>/`         | Yes            | Get own patient          |
| PUT    | `/api/patients/<id>/`         | Yes            | Update patient           |
| PATCH  | `/api/patients/<id>/`         | Yes            | Partially update patient |
| DELETE | `/api/patients/<id>/`         | Yes            | Delete patient           |
| POST   | `/api/doctors/`               | Yes            | Create doctor            |
| GET    | `/api/doctors/`               | Yes            | List doctors             |
| GET    | `/api/doctors/<id>/`          | Yes            | Get doctor               |
| PUT    | `/api/doctors/<id>/`          | Yes            | Update doctor            |
| PATCH  | `/api/doctors/<id>/`          | Yes            | Partially update doctor  |
| DELETE | `/api/doctors/<id>/`          | Yes            | Delete doctor            |
| POST   | `/api/mappings/`              | Yes            | Assign doctor to patient |
| GET    | `/api/mappings/`              | Yes            | List user's mappings     |
| GET    | `/api/mappings/<patient_id>/` | Yes            | Get doctors for patient  |
| DELETE | `/api/mappings/<id>/`         | Yes            | Delete mapping           |

---

# 38. Design Notes

### Custom User Model

The project uses a custom `User` model with email as the username field:

```python
USERNAME_FIELD = "email"
```

Therefore authentication uses:

```json
{
    "email": "asha@example.com",
    "password": "Str0ngPass!23"
}
```

rather than a username.

### Patient Ownership

Patient records are filtered by:

```text
created_by
```

Therefore users can only access patients they created.

### Mapping Route

The following route uses the **patient ID**:

```text
GET /api/mappings/<patient_id>/
```

while DELETE uses the **mapping ID**:

```text
DELETE /api/mappings/<id>/
```

This distinction is intentional.

### API Only

This project is designed as an API-only backend.

There is no dependency on:

* Django admin
* Session authentication
* CSRF-based API authentication

JWT is used for protected API access.

---

# 39. Important Notes for Reviewers

To test the project successfully:

1. Make sure PostgreSQL is installed and running.
2. Create the `healthcare` database.
3. Configure `.env`.
4. Install Python dependencies.
5. Run migrations.
6. Start Django.
7. Register a user.
8. Login and copy the access token.
9. Use the access token for protected endpoints.
10. Create a patient.
11. Create a doctor.
12. Create a patient–doctor mapping.
13. Test the remaining CRUD and authorization endpoints.

The complete API can be tested without modifying the application code.

---


