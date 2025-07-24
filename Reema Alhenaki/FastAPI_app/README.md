# FastAPI + PostgreSQL Dockerized Application

This project is a Dockerized **FastAPI** application connected to **PostgreSQL**.  
It automatically initializes the database and loads data on first run using `entrypoint.sh`.

## Project Overview
This project provides a RESTful API for managing **patient data** stored in PostgreSQL.  
It supports full **CRUD operations** (Create, Read, Update, Delete) on patient records.

### Key Features
- FastAPI framework for building APIs
- PostgreSQL for persistent data storage
- Automatic database creation and initialization using `entrypoint.sh`
- Full CRUD functionality for patient data
- Interactive API documentation with Swagger UI at `/docs`
- Docker Compose for multi-container management (FastAPI + Postgres)

## Project Structure
```
FastAPI_app/
│
├── app/                 # FastAPI app (routers, models, etc.)
├── data/cleaned         # CSV data files
├── create_tables.sql    # SQL schema for table creation
├── load_csv_data.py     # Script to load CSV data into DB
├── entrypoint.sh        # Automatic DB setup + start FastAPI
├── docker-compose.yml   # Compose configuration (FastAPI + Postgres)
├── Dockerfile           # Builds FastAPI container
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (DB credentials, paths)
```

## Requirements
- Docker Desktop
- Git (for cloning)

## Environment Variables
Create a `.env` file in the root directory:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=HIS_patients

OUTPUT_SQL=create_tables.sql
INFER_VARCHAR=True
SAMPLE_ROWS=100
CSV_FOLDER=./data/cleaned
```

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd FastAPI_app
```

### 2. Build and run containers
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL container
- Start FastAPI container
- Auto-create database and tables
- Load CSV data if tables are empty
- Serve API at `http://localhost:8000`

## API Documentation
Visit:
```
http://localhost:8000/docs
```
Interactive Swagger UI for testing endpoints.

## Managing Containers

### Stop containers
```bash
docker-compose down
```

### Start again (no rebuild)
```bash
docker-compose up
```

### Rebuild (after changes)
```bash
docker-compose up --build
```

## Database Access
To connect to PostgreSQL inside container:
```bash
docker exec -it his_db psql -U postgres -d HIS_patients
```
List tables:
```sql
\dt
```
Exit:
```sql
\q
```

## Forcing Data Reload (Optional)
To reload schema and data (even if tables exist):
1. Set `FORCE_INIT=true` in `.env`
2. Rebuild containers:
```bash
docker-compose down
docker-compose up --build
```

## Development Notes
- Initialization is automated via `entrypoint.sh`
- Persistent Postgres data stored in Docker volume `postgres_data`
