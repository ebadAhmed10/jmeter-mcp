#!/usr/bin/env python3
"""
Simple MCP client to test the JMeter MCP server
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_jmeter_mcp():
    """Test the JMeter MCP server by listing available tools"""
    
    # Server parameters - using uv to run the server
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "/home/ebad/jmeter-mcp", "run", "jmeter_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            
            print("=" * 60)
            print("Available MCP Tools:")
            print("=" * 60)
            for tool in tools.tools:
                print(f"\n📦 {tool.name}")
                print(f"   Description: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"   Parameters: {json.dumps(tool.inputSchema.get('properties', {}), indent=6)}")
            
            print("\n" + "=" * 60)
            print(f"Total tools available: {len(tools.tools)}")
            print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_jmeter_mcp())
