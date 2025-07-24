import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import re


# Load environment variables
load_dotenv()

# Load config
CSV_FOLDER = os.getenv("CSV_FOLDER")
POSTGRES_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
print("🔍 CSV_FOLDER:", os.getenv("CSV_FOLDER"))  # Debug line
print("🔍 POSTGRES_URL:", os.getenv("POSTGRES_URL"))  # Debug line

# Create database engine
engine = create_engine(POSTGRES_URL)

# Define CSVs and matching table names
csv_files = {
    "HIS_Patient.csv": "HIS_Patient",
    "HIS_Appointment.csv": "HIS_Appointment",
    "HIS_DoctorOrder.csv": "HIS_DoctorOrder",
    "HIS_PatientVitalSigns.csv": "HIS_PatientVitalSigns"
}

def clean_column_names(df):
    """Clean DataFrame column names by stripping extra spaces."""
    df.columns = [col.strip() for col in df.columns]
    return df


#Converting Data to DATE and TIMESTAMP type
def clean_dates(df):
    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna().astype(str).head(5).tolist()

            if all(re.match(r"\d{1,2}/\d{1,2}/\d{4}$", s.strip()) for s in sample):
                try:
                    df[col] = pd.to_datetime(df[col], format="%d/%m/%Y").dt.date
                    print(f"📅 '{col}' converted to DATE")
                except:
                    pass

            elif all(re.match(r"\d{1,2}/\d{1,2}/\d{4}.*\d{1,2}:\d{2}", s.strip()) for s in sample):
                try:
                    df[col] = pd.to_datetime(df[col], dayfirst=True)
                    print(f"⏱️ '{col}' converted to TIMESTAMP")
                except:
                    pass
    return df


# List all tables in the order of importing
ordered_tables = [
    "HIS_Patient",         
    "HIS_Appointment",     
    "HIS_PatientVitalSigns",
    "HIS_DoctorOrder",
]

#Reading csv files and importing them to postgressql 
for table in ordered_tables:
    csv_file = os.path.join(CSV_FOLDER, f"{table}.csv")
    if not os.path.exists(csv_file):
        print(f"⚠️ Skipping {table}, file not found: {csv_file}")
        continue

    print(f"📥 Inserting {table}.csv into {table}...")

    df = pd.read_csv(csv_file)
    df = clean_column_names(df)
    df = clean_dates(df)

    try:
        df.to_sql(table, engine, if_exists="append", index=False)
        print(f"✅ Loaded {table}.csv successfully.\n")
    except Exception as e:
        print(f"❌ Failed to load {table}. Error:\n{e}\n")



print("✅ All CSVs successfully loaded into PostgreSQL.")

