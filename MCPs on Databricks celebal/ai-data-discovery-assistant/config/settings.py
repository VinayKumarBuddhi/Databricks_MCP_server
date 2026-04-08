import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID")

def validate_settings():
    missing = []
    if not DATABRICKS_HOST:
        missing.append("DATABRICKS_HOST")
    if not DATABRICKS_TOKEN:
        missing.append("DATABRICKS_TOKEN")
    if not DATABRICKS_WAREHOUSE_ID:
        missing.append("DATABRICKS_WAREHOUSE_ID")
        
    if missing:
        raise ValueError(f"Missing essential environment variables in .env file: {', '.join(missing)}")
