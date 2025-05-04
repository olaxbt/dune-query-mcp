from flask import Flask
from flask_cors import CORS
from loguru import logger
import configparser
import os
from flasgger import Swagger
from mcp.server.fastmcp import FastMCP

# Initialize the Flask application
app = Flask(__name__)

# Initialize MCP server
mcp = FastMCP(
    name="DuneLink",
    description="A modern bridge connecting Dune Analytics data to intelligent agents",
    dependencies=["httpx", "pandas", "python-dotenv"]
)

# Load configuration
config = configparser.ConfigParser()
config.read('config/config.ini')

# Initialize Swagger for API documentation
app.config['SWAGGER'] = {
    'title': 'DuneLink API',
    'uiversion': 3,
}

# Initialize extensions
CORS(app)
swagger = Swagger(app)

# Set up logging
logger.add("logs/dune_mcp.log", rotation="1 MB", colorize=True, format="<green>{time}</green> <level>{message}</level>")

# Export MCP for use in routes
def get_mcp():
    return mcp

# Register Blueprints (must be after the get_mcp function is defined)
from app.routes.dune_routes import dune_bp
app.register_blueprint(dune_bp, url_prefix='/dune') 