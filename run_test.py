#!/usr/bin/env python3
"""
Run a JMeter test using the MCP server
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_jmeter_test():
    """Run the sample JMeter test via MCP"""
    
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "/home/ebad/jmeter-mcp-server", "run", "jmeter_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            print("🚀 Running JMeter test: sample_test.jmx")
            print("=" * 60)
            
            # Call the execute_jmeter_test_non_gui tool
            result = await session.call_tool(
                "execute_jmeter_test_non_gui",
                arguments={
                    "test_file": "/home/ebad/jmeter-mcp-server/sample_test.jmx",
                    "log_file": "test_results.jtl",
                    "generate_report": True,
                    "report_output_dir": "jmeter_report"
                }
            )
            
            print("\n📊 Test Results:")
            print("=" * 60)
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_jmeter_test())
