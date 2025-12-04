#!/usr/bin/env python3
"""
MCP client to connect to the running JMeter MCP server via stdio
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def connect_and_test():
    """Connect to the running JMeter MCP server"""
    
    print("Connecting to JMeter MCP server...")
    
    # Server parameters - connect to the running server via stdio
    server_params = StdioServerParameters(
        command="python3",
        args=["jmeter_server.py"],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                
                print("\n" + "=" * 60)
                print("✅ Successfully connected to JMeter MCP server!")
                print("=" * 60)
                print(f"\n📊 Available MCP Tools: {len(tools.tools)}")
                print("=" * 60)
                
                for i, tool in enumerate(tools.tools, 1):
                    print(f"\n{i}. {tool.name}")
                    print(f"   Description: {tool.description}")
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        props = tool.inputSchema.get('properties', {})
                        if props:
                            print(f"   Parameters:")
                            for param_name, param_info in props.items():
                                print(f"     - {param_name}: {param_info.get('description', 'N/A')}")
                
                print("\n" + "=" * 60)
                print(f"✅ Total tools available: {len(tools.tools)}")
                print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(connect_and_test())
