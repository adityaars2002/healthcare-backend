# Healthcare Backend (Django + DRF + PostgreSQL)

JWT-authenticated REST API for users, patients, doctors, and patient-doctor mappings.

## Setup

```bash
python -m venv .venv && .venv/Scripts/activate      # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                                 # then edit DB creds + a real secret key
createdb healthcare                                  # or create the DB in psql/pgAdmin
python manage.py migrate
python manage.py runserver
```

`.env` holds every secret: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`,
`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.

## Endpoints

All `/api/patients/`, `/api/doctors/`, `/api/mappings/` routes require
`Authorization: Bearer <access token>`.

| Method | Path | Notes |
|---|---|---|
| POST | `/api/auth/register/` | `name`, `email`, `password` → user + JWT pair |
| POST | `/api/auth/login/` | `email`, `password` → `access`, `refresh` |
| POST | `/api/auth/refresh/` | `refresh` → new `access` |
| POST/GET | `/api/patients/` | create / list **your own** patients |
| GET/PUT/PATCH/DELETE | `/api/patients/<id>/` | your own patients only (404 otherwise) |
| POST/GET | `/api/doctors/` | create / list all doctors |
| GET/PUT/PATCH/DELETE | `/api/doctors/<id>/` | |
| POST | `/api/mappings/` | `patient`, `doctor` — patient must be yours |
| GET | `/api/mappings/` | all your mappings |
| GET | `/api/mappings/<patient_id>/` | doctors assigned to that patient |
| DELETE | `/api/mappings/<id>/` | remove one mapping |

List responses are paginated (`?page=N`, 20 per page).

## Quick check

```bash
curl -X POST localhost:8000/api/auth/register/ -H "Content-Type: application/json" \
  -d '{"name":"Asha","email":"asha@example.com","password":"Str0ngPass!23"}'

curl -X POST localhost:8000/api/auth/login/ -H "Content-Type: application/json" \
  -d '{"email":"asha@example.com","password":"Str0ngPass!23"}'

curl localhost:8000/api/patients/ -H "Authorization: Bearer <access>"
```

## Tests

```bash
python manage.py test
```

Covers register → login → patient → doctor → mapping, duplicate-assignment rejection,
cross-user isolation, and unauthenticated access. Needs a Postgres user allowed to create
the `test_*` database.

## Design notes

- Custom `User` model keyed on email (`USERNAME_FIELD = "email"`), so the simplejwt login
  view takes `email` + `password` directly.
- Patient queryset is filtered by `created_by`, so another user's records return 404, not 403.
- `GET /api/mappings/<patient_id>/` overrides `retrieve` because the spec keys that route on
  the patient id while `DELETE /api/mappings/<id>/` keys on the mapping id.
- API-only project: no admin, sessions, or CSRF middleware.
