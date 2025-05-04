from app import app, get_mcp

if __name__ == '__main__':
    mcp = get_mcp()
    # Run the MCP server
    mcp.run() 