import json
import logging
import sys
import os

# Ensure the parent directory (ai-data-discovery-assistant) is in the Python path
# so that Claude Desktop can resolve the `mcp_server` module correctly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp.server.fastmcp import FastMCP
from mcp_server.databricks_client import DatabricksClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_databricks")

# Initialize the MCP Server
mcp = FastMCP("Databricks Data Discovery Assistant")

try:
    client = DatabricksClient()
except Exception as e:
    logger.error(f"Failed to initialize DatabricksClient. Ensure .env is populated. Error: {e}")
    client = None

@mcp.tool()
def list_catalogs() -> str:
    """
    Retrieves all catalogs available in Unity Catalog.
    Returns a JSON string of available catalogs.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.list_catalogs(), indent=2)

@mcp.tool()
def list_schemas(catalog_name: str) -> str:
    """
    Lists schemas inside a given catalog.
    Args:
        catalog_name: The name of the catalog.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.list_schemas(catalog_name), indent=2)

@mcp.tool()
def list_tables(catalog_name: str, schema_name: str) -> str:
    """
    Retrieves all tables within a schema.
    Args:
        catalog_name: The name of the catalog.
        schema_name: The name of the schema.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.list_tables(catalog_name, schema_name), indent=2)

@mcp.tool()
def describe_table(full_name: str) -> str:
    """
    Provides detailed metadata about a specific table including columns.
    Args:
        full_name: The fully qualified name of the table (e.g. main.gold.sales_summary).
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.describe_table(full_name), indent=2)

@mcp.tool()
def get_table_lineage(table_name: str) -> str:
    """
    Displays upstream and downstream lineage for a table.
    Args:
        table_name: The fully qualified name of the table.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.get_table_lineage(table_name), indent=2)

@mcp.tool()
def run_sql_query(query: str) -> str:
    """
    Executes SQL queries through a Databricks SQL Warehouse.
    Args:
        query: The SQL query to execute.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.run_sql_query(query), indent=2)

@mcp.tool()
def search_tables_by_tag(tag_name: str) -> str:
    """
    Finds tables based on metadata tags defined in Unity Catalog.
    Args:
        tag_name: The tag to search for.
    """
    if not client: return "Error: DatabricksClient not initialized."
    return json.dumps(client.search_tables_by_tag(tag_name), indent=2)

# Expose Streamable HTTP app for Databricks Apps deployment
# Databricks Playground sends POST /mcp (Streamable HTTP transport)
app = mcp.streamable_http_app

if __name__ == "__main__":
    logger.info("Starting Databricks MCP Server...")
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        mcp.run()
    else:
        mcp.run()
