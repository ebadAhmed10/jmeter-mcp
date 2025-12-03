#!/usr/bin/env python3
"""
Generate visualization of JMeter results using the MCP server
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def generate_viz():
    """Generate visualizations via MCP"""
    
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "/home/ebad/jmeter-mcp-server", "run", "jmeter_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("📈 Generating visualizations...")
            
            # Generate time series
            result = await session.call_tool(
                "generate_visualization",
                arguments={
                    "jtl_file": "/home/ebad/jmeter-mcp-server/demo_results.jtl",
                    "visualization_type": "time_series",
                    "output_file": "/home/ebad/jmeter-mcp-server/time_series.png"
                }
            )
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"✅ {content.text}")
            
            # Generate HTML report
            result = await session.call_tool(
                "generate_visualization",
                arguments={
                    "jtl_file": "/home/ebad/jmeter-mcp-server/demo_results.jtl",
                    "visualization_type": "html_report",
                    "output_file": "/home/ebad/jmeter-mcp-server/analysis_report.html"
                }
            )
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"✅ {content.text}")

if __name__ == "__main__":
    asyncio.run(generate_viz())
