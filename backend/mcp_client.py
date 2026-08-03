import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _call_mcp_tool_async(module_name: str, tool_name: str, arguments: dict) -> str:
    server_params = StdioServerParameters(
        command="python",
        args=["-m", module_name],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content[0].text


def call_mcp_tool(module_name: str, tool_name: str, arguments: dict) -> str:
    return asyncio.run(_call_mcp_tool_async(module_name, tool_name, arguments))
