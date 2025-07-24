#!/bin/bash
set -e

echo "Waiting for PostgreSQL to start..."
sleep 5

# Step 1: Create the database if it does not exist
echo "Ensuring database '$DB_NAME' exists..."
PGPASSWORD="$DB_PASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    PGPASSWORD="$DB_PASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE DATABASE \"$DB_NAME\";"

# Step 2: Load schema if tables are missing
echo "Checking if tables exist..."
TABLE_COUNT=$(PGPASSWORD="$DB_PASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';")

if [ "$TABLE_COUNT" -eq 0 ]; then
  echo "No tables found — loading schema and data..."
  PGPASSWORD="$DB_PASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" < create_tables.sql
  python load_csv.py
else
  echo "Tables already exist — skipping schema and data load."
fi

# Step 3: Start FastAPI
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
