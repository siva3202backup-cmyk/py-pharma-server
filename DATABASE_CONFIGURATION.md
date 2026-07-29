# Local PostgreSQL configuration

1. Install PostgreSQL locally and ensure it is running on port `5432`.
2. Create the database:
   ```sql
   CREATE DATABASE pharmacy_db;
   ```
3. Initialize and seed it from the project root:
   ```bash
   psql -U postgres -d pharmacy_db -f database/pharmacy_extend_schema.sql
   ```
4. Copy `.env.example` to `.env` and set your local password in `DATABASE_URL`:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/pharmacy_db
   ```
5. Replace `JWT_SECRET` with a long random local value. Do not commit `.env`.

The supplied SQL preserves the schema and sample data from the Express.js project. The default seeded administrator is `admin@pharmacy.test` / `Admin@123`; change it for any non-demo use.
