from flask import jsonify, request, render_template
from app.routes.dune_routes import dune_bp
from app import get_mcp
import httpx
import os
import pandas as pd
import time
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MCP instance
mcp = get_mcp()

# Configuration
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
BASE_URL = "https://api.dune.com/api/v1"
HEADERS = {"X-Dune-API-Key": DUNE_API_KEY}

@dune_bp.route('/', methods=['GET'])
def index():
    """Render the index page"""
    return render_template('index.html')

@dune_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "message": "DuneLink is running"}), 200

@mcp.tool()
def get_latest_result(query_id: int) -> str:
    """
    Get the latest results for a specific query ID as a CSV string on Dune Analytics
    
    Args:
        query_id: The Dune Analytics query ID
        
    Returns:
        A CSV string containing the query results
    """
    logger.info(f"Fetching latest results for Dune query ID: {query_id}")
    try:
        # Fetch latest results
        url = f"{BASE_URL}/query/{query_id}/results"
        with httpx.Client() as client:
            response = client.get(url, headers=HEADERS, timeout=300)
            response.raise_for_status()
            data = response.json()
            
        # Convert results to DataFrame
        result_data = data.get("result", {}).get("rows", [])
        if not result_data:
            logger.warning(f"No data available for query ID: {query_id}")
            return "No data available"
        
        logger.info(f"Successfully retrieved results for query ID: {query_id}")
        df = pd.DataFrame(result_data)
        return df.to_csv(index=False)
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching query results: {str(e)}")
        return f"HTTP error fetching query results: {str(e)}"
    except Exception as e:
        logger.error(f"Error processing query results: {str(e)}")
        return f"Error processing query results: {str(e)}"

@mcp.tool()
def run_query(query_id: int) -> str:
    """
    Run a query by ID and return results as a CSV string on Dune Analytics
    
    Args:
        query_id: The Dune Analytics query ID to execute
        
    Returns:
        A CSV string containing the query results
    """
    logger.info(f"Executing Dune query ID: {query_id}")
    try:
        # Execute the query
        url = f"{BASE_URL}/query/execute/{query_id}"
        with httpx.Client() as client:
            execute_response = client.post(url, headers=HEADERS, timeout=300)
            execute_response.raise_for_status()
            execution_data = execute_response.json()
            execution_id = execution_data.get("execution_id")
            
            if not execution_id:
                logger.error("Failed to start query execution")
                return "Failed to start query execution"

            # Poll for status until complete
            status_url = f"{BASE_URL}/execution/{execution_id}/status"
            logger.info(f"Polling execution status for execution ID: {execution_id}")
            attempts = 0
            max_attempts = 60  # Timeout after ~5 minutes
            
            while attempts < max_attempts:
                status_response = client.get(status_url, headers=HEADERS)
                status_response.raise_for_status()
                status_data = status_response.json()
                state = status_data.get("state")
                
                if state == "EXECUTING" or state == "PENDING":
                    attempts += 1
                    time.sleep(5)  # Wait before polling again
                    logger.debug(f"Query still executing... (attempt {attempts}/{max_attempts})")
                elif state == "COMPLETED":
                    logger.info("Query execution completed successfully")
                    break
                else:
                    logger.error(f"Query execution failed with state: {state}")
                    return f"Query execution failed with state: {state}"
                
                if attempts >= max_attempts:
                    logger.error("Query execution timed out")
                    return "Query execution timed out"

            # Fetch results
            logger.info("Fetching query execution results")
            results_url = f"{BASE_URL}/execution/{execution_id}/results"
            results_response = client.get(results_url, headers=HEADERS)
            results_response.raise_for_status()
            results_data = results_response.json()
        
        # Convert results to DataFrame
        result_data = results_data.get("result", {}).get("rows", [])
        if not result_data:
            logger.warning("No data available in query results")
            return "No data available"
        
        logger.info("Successfully processed query results")
        df = pd.DataFrame(result_data)
        return df.to_csv(index=False)
    except httpx.HTTPError as e:
        logger.error(f"HTTP error running query: {str(e)}")
        return f"HTTP error running query: {str(e)}"
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"Error processing query: {str(e)}"

@dune_bp.route('/query/<int:query_id>/latest', methods=['GET'])
def api_get_latest_result(query_id):
    """API endpoint to get latest query results"""
    result = get_latest_result(query_id)
    return jsonify({"result": result}), 200

@dune_bp.route('/query/<int:query_id>/execute', methods=['POST'])
def api_run_query(query_id):
    """API endpoint to execute a query"""
    result = run_query(query_id)
    return jsonify({"result": result}), 200