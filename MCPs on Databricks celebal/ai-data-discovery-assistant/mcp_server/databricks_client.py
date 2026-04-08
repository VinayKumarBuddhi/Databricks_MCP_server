import requests
import urllib.parse
from config.settings import DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_WAREHOUSE_ID, validate_settings

class DatabricksClient:
    def __init__(self):
        validate_settings()
        # Ensure host doesn't have a trailing slash
        self.host = DATABRICKS_HOST.rstrip("/")
        self.token = DATABRICKS_TOKEN
        self.warehouse_id = DATABRICKS_WAREHOUSE_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get(self, endpoint, params=None):
        url = f"{self.host}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, payload=None):
        url = f"{self.host}{endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def list_catalogs(self):
        """Retrieves all catalogs available in Unity Catalog."""
        return self._get("/api/2.1/unity-catalog/catalogs")

    def list_schemas(self, catalog_name):
        """Lists schemas inside a given catalog."""
        return self._get("/api/2.1/unity-catalog/schemas", params={"catalog_name": catalog_name})

    def list_tables(self, catalog_name, schema_name):
        """Retrieves all tables within a schema."""
        return self._get("/api/2.1/unity-catalog/tables", params={
            "catalog_name": catalog_name,
            "schema_name": schema_name
        })

    def describe_table(self, full_name):
        """Provides detailed metadata about a specific table."""
        return self._get(f"/api/2.1/unity-catalog/tables/{urllib.parse.quote(full_name)}")

    def get_table_lineage(self, table_name):
        """Displays upstream and downstream lineage for a table."""
        return self._get("/api/2.0/lineage-tracking/table-lineage", params={"table_name": table_name})

    def run_sql_query(self, query):
        """Executes SQL queries through a Databricks SQL Warehouse."""
        payload = {
            "statement": query,
            "warehouse_id": self.warehouse_id,
            "wait_timeout": "50s"  # Wait for query to complete
        }
        return self._post("/api/2.0/sql/statements", payload=payload)

    def search_tables_by_tag(self, tag_name):
        """
        Finds tables based on metadata tags.
        Note: Databricks lacks a simple global tag search in some UC API versions,
        this might be a basic implementation relying on the Discovery API or iterating.
        For now, we will use the Unity Catalog search API.
        """
        payload = {
            "query_text": f"tags:{tag_name}"
        }
        return self._get("/api/2.0/discovery/search", params=payload)
