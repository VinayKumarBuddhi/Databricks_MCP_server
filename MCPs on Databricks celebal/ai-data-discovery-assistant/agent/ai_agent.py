import sys
import os
import json

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server.server import list_catalogs, list_schemas, search_tables_by_tag, list_tables

def simulate_ai_agent_discovery():
    """
    Simulates an AI Agent trying to discover data.
    """
    print("[Agent]: 'I need to find tables in our Databricks workspace.'")
    print("Action 1: Calling `list_catalogs` tool...")
    
    # In a real MCP setup, the LLM requests this tool execution over stdio.
    # We call the underlying function directly for the demo.
    cat_response = json.loads(list_catalogs())
    catalogs = [c['name'] for c in cat_response.get('catalogs', [])][:3] # Take first 3
    print(f"Result: Found catalogs: {catalogs}\n")
    
    if not catalogs:
        print("No catalogs found.")
        return

    print(f"[Agent]: 'I'll look into the `{catalogs[0]}` catalog.'")
    print(f"Action 2: Calling `list_schemas('{catalogs[0]}')` tool...")
    
    schema_response = json.loads(list_schemas(catalogs[0]))
    schemas = [s['name'] for s in schema_response.get('schemas', [])][:3]
    print(f"Result: Found schemas: {schemas}\n")
    
    if not schemas:
        print("No schemas found.")
        return
        
    print(f"[Agent]: 'Let's see the tables in the `{schemas[0]}` schema.'")
    print(f"Action 3: Calling `list_tables('{catalogs[0]}', '{schemas[0]}')` tool...")
    
    table_response = json.loads(list_tables(catalogs[0], schemas[0]))
    tables = [t['name'] for t in table_response.get('tables', [])][:5]
    print(f"Result: Found tables: {tables}\n")
    
    print("[Agent]: 'I have successfully discovered the data structure!'")

if __name__ == "__main__":
    simulate_ai_agent_discovery()
