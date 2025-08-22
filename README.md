# Flask Users (Dosha) Backend


A minimal Flask API with SQLAlchemy and Flask‑Migrate that stores users with a protected (hashed) password and a dosha test result.


## Features
- **Users table** with columns: `id`, `user` (unique), `password_hash` (stored), `dosha`, timestamps
- **Password hashing** using Werkzeug (PBKDF2‑SHA256)
- CRUD endpoints under `/api/users`
- Alembic/Flask‑Migrate migration creating the `users` table
- Pytest test suite
- SQLite by default; switch to Postgres/MySQL by setting `DATABASE_URL`


## Quickstart


### 1) Clone & create venv
```bash
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate