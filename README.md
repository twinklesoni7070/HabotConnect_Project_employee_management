# Employee Management REST API (Django + DRF + JWT)

## Features
- JWT Authentication (Bearer token)
- Employee CRUD APIs
- Filtering by department & role
- Pagination (10 per page)
- Basic tests (pytest)

## Setup
```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter
pip install pytest pytest-django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Auth (JWT)

POST /api/token/ with:

{ "username": "Geetanjali", "password": "@Bipendra" }

Use access token as Bearer token.

Endpoints

POST /api/employees/

GET /api/employees/ (pagination + filtering)

GET /api/employees/{id}/

PUT /api/employees/{id}/

DELETE /api/employees/{id}/

Filters

/api/employees/?department=HR

/api/employees/?role=Developer

Tests
pytest -q
