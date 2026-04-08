# AI Data Discovery Assistant

An AI-enabled Data Discovery Assistant that uses the Model Context Protocol (MCP) to allow AI agents to safely discover Databricks Unity Catalog metadata, inspect datasets, and run SQL queries.

## Project Structure
- `mcp_server/`: The core MCP server (`server.py`) and Databricks API client (`databricks_client.py`).
- `agent/`: Example script demonstrating how an AI agent interacts with the tools (`ai_agent.py`).
- `config/`: Configurations and environment loading (`settings.py`).
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables for connecting to Databricks.

## Setup Instructions

1. **Install Dependencies**
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. **Configure Environment**
   Open the `.env` file and set the following variables:
   - `DATABRICKS_HOST`: Your Databricks workspace URL (e.g., `https://adb-123456789.azuredatabricks.net`).
   - `DATABRICKS_TOKEN`: Your Personal Access Token.
   - `DATABRICKS_WAREHOUSE_ID`: The ID of your Databricks SQL Warehouse.

## How to Run the MCP Server Locally (Testing)

You can run the MCP server directly in your terminal to see it using the FastMCP CLI inspector:
```powershell
# Open terminal in the project root directory
npx @modelcontextprotocol/inspector py mcp_server/server.py
```
*Note: This requires Node.js/npm installed to run the inspector web UI.*

## How to Implement/Connect With Claude Desktop

To use this MCP server with Claude Desktop (or any other MCP-compatible client), you need to configure the client to launch your Python script.

1. Open your Claude Desktop configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the Databricks MCP server to the `mcpServers` section. You must provide the absolute path to your Python executable and the absolute path to the `mcp_server/server.py` script.

**Example `claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "databricks-discovery": {
      "command": "C:\\Users\\VinayKumarBuddhi\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
      "args": [
        "c:\\Users\\VinayKumarBuddhi\\OneDrive - Celebal Technologies Private Limited\\Desktop\\projects\\MCPs on Databricks\\ai-data-discovery-assistant\\mcp_server\\server.py"
      ],
      "env": {
        "DATABRICKS_HOST": "your-workspace-url",
        "DATABRICKS_TOKEN": "your-token",
        "DATABRICKS_WAREHOUSE_ID": "your-warehouse-id"
      }
    }
  }
}
```

3. **Restart Claude Desktop**. It will launch the MCP server as a subprocess and expose the Databricks tools to Claude. You can then just ask Claude: *"What catalogs are available in my Databricks workspace?"*

## Tools Provided by the MCP Server
- `list_catalogs()`: Retrieves all catalogs.
- `list_schemas(catalog_name)`: Lists schemas inside a given catalog.
- `list_tables(catalog_name, schema_name)`: Retrieves all tables within a schema.
- `describe_table(full_name)`: Detailed metadata about a specific table (e.g., `main.default.my_table`).
- `get_table_lineage(table_name)`: Displays upstream and downstream lineage.
- `search_tables_by_tag(tag_name)`: Finds tables based on metadata tags.
- `run_sql_query(query)`: Executes SQL queries on your Databricks SQL Warehouse.
