# Pharmacy FastAPI Backend

Local-only conversion of the supplied Express.js pharmacy backend. No Docker or Jenkins files are included.

## Requirements
- Python 3.14 recommended (3.12 or newer supported)
- PostgreSQL 16 or newer

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
```
Configure PostgreSQL using `DATABASE_CONFIGURATION.md`, then run:
```bash
uvicorn main:app --host 127.0.0.1 --port 5000 --reload
```

- API: http://localhost:5000
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc
- Health: http://localhost:5000/api/health

## Angular integration
The default CORS origin is `http://localhost:4200`. Send authenticated requests with:
```http
Authorization: Bearer <JWT>
Content-Type: application/json
```
The `/api` paths and JSON field conventions are retained for frontend compatibility.

## Verification
```bash
python -m compileall app main.py
pytest -q
```

## Route coverage
Authentication, categories, brands, products (including filters/related/admin CRUD), profile, cart, wishlist, reviews, coupons, orders, payments, reports, and admin dashboard are implemented. Swagger schemas are generated from Pydantic request models.
