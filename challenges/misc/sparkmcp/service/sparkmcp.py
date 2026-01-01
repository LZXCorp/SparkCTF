import os
import subprocess
from datetime import datetime

import sqlite3
import pytz

from fastmcp import FastMCP, Context
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

db_path = os.path.join(os.path.dirname(__file__), 'spark.db')
db_conn = sqlite3.connect(db_path)
cursor = db_conn.cursor()

SCOPE = {
    "read:data": 1 << 0,   # 1
    "write:data": 1 << 1,  # 2
    "admin:users": 1 << 2, # 4
}

def mask_to_scopes(mask):
    """Convert an integer mask to a list of scope strings."""
    return [scope for scope, bit in SCOPE.items() if mask & bit]

cursor.execute("SELECT client_id, token, scope_mask FROM auth")
users = cursor.fetchall()

tokens = {}
for client_id, token, scope_mask in users:
    tokens[token] = {
        "client_id": client_id,
        "scopes": mask_to_scopes(scope_mask)
    }

verifier = StaticTokenVerifier(
    tokens=tokens,
    required_scopes=["read:data"]
)

sparkmcp = FastMCP(
    name="SparkMCP",
    auth=verifier
)

def extract_client_id(ctx: Context) -> str:
    request = ctx.get_http_request()
    auth_header = request.headers.get("Authorization", "")
    token = ""
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    return tokens.get(token, {}).get("client_id", "Unknown client")

@sparkmcp.tool
def get_server_status() -> dict:
    """Gets current server status information."""
    try:
        cursor.execute("SELECT 1")
        sql_status = "connected"
    except Exception as e:
        sql_status = f"error: {e}"
    return {
        "status": "running",
        "version": "0.0.1",
        "sql_status": sql_status,
    }

@sparkmcp.tool
def current_datetime(timezone: str) -> str:
    """Gets the current date and time based on the user's current timezone or the system time of the MCP server."""
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz).isoformat()
    except Exception:
        return datetime.now().isoformat()

@sparkmcp.tool
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    client_id = extract_client_id(ctx)
    return {
        "session_id": ctx.request_id,
        "client_id": client_id or "Unknown client"
    }

@sparkmcp.tool
def get_flag(ctx: Context) -> str:
    """Get a string value of the flag"""
    client_id = extract_client_id(ctx)
    if client_id == "admin@sparkctf.org":
        return "SPARK{0bta1n3D_fR0M_MCP_sUCC3ssFu11y}"
    else:
        return "SPARK{try_harder_:)}"

@sparkmcp.tool
async def query_tools(filter: str = "") -> list:
    """Get all of the tools that SparkMCP has to offer, optionally filtered by name or description."""
    if filter:
        cursor.execute(
            f"SELECT name, description FROM tools WHERE name LIKE '%{filter}%' OR description LIKE '%{filter}%'"
        )
    else:
        cursor.execute("SELECT name, description FROM tools")
    tools = cursor.fetchall()
    return [{"name": name, "description": description} for name, description in tools]

@sparkmcp.tool
async def use_sparktool(tool: str) -> dict:
    """Makes use of a tool in SparkMCP to execute. The tool will provide back the results of the tool."""
    result = {}

    # Check if the tool exists
    cursor.execute(
        "SELECT name, description, command FROM tools WHERE name = ?",
        (tool,)
    )
    fetched_tool = cursor.fetchone()
    if not fetched_tool:
        result["error"] = "Tool not found"
        return result
    result["tool"] = {"name": fetched_tool[0], "description": fetched_tool[1]}

    # Execute the tool command
    command = fetched_tool[2]
    try:
        output = subprocess.check_output(command, shell=True, text=True, timeout=10)
        result["output"] = output.strip()
    except Exception as e:
        result["error"] = f"Failed to execute command: {e}"

    return result

if __name__ == '__main__':
    sparkmcp.run(
        transport = "http",
        host = "0.0.0.0",
        port = 6080
    )