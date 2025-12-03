#!/usr/bin/env python3
"""
Analyze JMeter results using the MCP server
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def analyze_results():
    """Analyze the demo JMeter results via MCP"""
    
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "/home/ebad/jmeter-mcp-server", "run", "jmeter_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            print("=" * 70)
            print("📊 ANALYZING JMETER RESULTS")
            print("=" * 70)
            
            # 1. Analyze results
            print("\n🔍 1. General Analysis:")
            print("-" * 70)
            result = await session.call_tool(
                "analyze_jmeter_results",
                arguments={
                    "jtl_file": "/home/ebad/jmeter-mcp-server/demo_results.jtl",
                    "detailed": True
                }
            )
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            
            # 2. Identify bottlenecks
            print("\n\n🚨 2. Performance Bottlenecks:")
            print("-" * 70)
            result = await session.call_tool(
                "identify_performance_bottlenecks",
                arguments={
                    "jtl_file": "/home/ebad/jmeter-mcp-server/demo_results.jtl"
                }
            )
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            
            # 3. Get insights
            print("\n\n💡 3. Performance Insights:")
            print("-" * 70)
            result = await session.call_tool(
                "get_performance_insights",
                arguments={
                    "jtl_file": "/home/ebad/jmeter-mcp-server/demo_results.jtl"
                }
            )
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            
            print("\n" + "=" * 70)
            print("✅ Analysis Complete!")
            print("=" * 70)

if __name__ == "__main__":
    asyncio.run(analyze_results())
