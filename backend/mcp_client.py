# backend/mcp_client.py

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ---------------------------------------------------------
# Generic MCP client helper.
# Spawns the MCP server as a subprocess, calls a tool on it,
# and returns the result. Used by agents instead of direct
# function calls.
# ---------------------------------------------------------

async def _call_mcp_tool_async(server_script: str, tool_name: str, arguments: dict) -> str:
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content[0].text


def call_mcp_tool(server_script: str, tool_name: str, arguments: dict) -> str:
    """Sync wrapper — call this from agent code."""
    return asyncio.run(_call_mcp_tool_async(server_script, tool_name, arguments))