# Project Setup Guide

## 1. Installing and Creating a PostgreSQL Database

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Start the PostgreSQL service:
```bash
sudo systemctl start postgresql
```

Access the PostgreSQL prompt:
```bash
sudo -u postgres psql
```

Create a new database:
```sql
CREATE DATABASE brokerage_app;
```

---

## 2. Alembic (Database Migrations)

> **Note:** Alembic initialization and revision generation are not required for now.

Initialize Alembic (optional):
```bash
alembic init alembic
```

Generate a new revision (optional):
```bash
alembic revision --autogenerate -m "Create initial tables"
```

Apply migrations (required):
```bash
alembic upgrade head
```

---

## 3. Running the Application

Navigate to the project directory:
```bash
cd bhive_project
```

Start the application using Uvicorn:
```bash
uvicorn app.main:router --reload
```
