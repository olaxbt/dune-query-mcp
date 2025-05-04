# DuneLink

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)

A modern bridge connecting Dune Analytics data to intelligent agents through Model Control Protocol (MCP).

## Overview

DuneLink enables seamless integration of blockchain data analytics into your AI applications. By leveraging Dune Analytics' powerful query capabilities with the Model Control Protocol, this service allows LLMs and other AI systems to access on-chain data through simple, natural language interactions.

## Core Capabilities

### Data Retrieval Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `get_latest_result` | Retrieves pre-computed query results | Quick access to existing data |
| `run_query` | Executes a query on-demand | Real-time data analysis |

### Data Format

All data is returned in CSV format, providing:
- Universal compatibility
- Easy parsing by most data analysis tools
- Human-readable output

## Getting Started

### System Requirements

- Python 3.10 or higher
- Valid Dune Analytics API key ([Get yours here](https://dune.com/settings/api))

### Quick Setup

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/olaxbt/dune-query-mcp.git
   cd dunelink
   ```

2. **Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate it
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure API Access**
   ```bash
   # Copy example config
   cp .env.example .env
   
   # Edit with your API key
   echo "DUNE_API_KEY=your_key_here" > .env
   ```

## Usage

### Running the Service

DuneLink offers two ways to run:

#### As MCP Service

```bash
python run.py
```
This starts the MCP service on default port 8000.

#### As Web Server

```bash
python flask_app.py
```
This provides access to the web interface and REST API endpoints.

### Integrating with Applications

#### MCP Client Integration

```python
from mcp.client import Client

# Connect to DuneLink
client = Client("http://localhost:8000")

# Get latest results for a query
csv_data = client.call("get_latest_result", query_id=1234567)

# Execute a query
query_results = client.call("run_query", query_id=1234567)
```

#### REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dune/health` | GET | Service health check |
| `/dune/query/{query_id}/latest` | GET | Retrieve latest results |
| `/dune/query/{query_id}/execute` | POST | Run a query |

Example REST Call:
```bash
curl -X GET http://localhost:5000/dune/query/1234567/latest
```

## Architecture

```
dunelink/
├── app/                       # Application core
│   ├── __init__.py            # Flask & MCP setup
│   ├── routes/                # API endpoint definitions
│   │   └── dune_routes/       # Dune Analytics routes
│   │   └── templates/             # Web interface
│   └── templates/             # Web interface
├── config/                    # Configuration files
├── logs/                      # Runtime logs
├── flask_app.py               # Web server entry point
├── run.py                     # MCP server entry point
└── requirements.txt           # Dependencies
```

## Advanced Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| DUNE_API_KEY | Authentication for Dune API | None (Required) |
| PORT | Server port | 8000 |

### Performance Tuning

For high-volume query execution:

```bash
# Set a higher timeout for long-running queries
export DUNE_QUERY_TIMEOUT=600  # 10 minutes in seconds
```

## Troubleshooting

Common issues and solutions:

| Problem | Solution |
|---------|----------|
| API Key errors | Ensure `.env` file exists with valid key |
| Timeout errors | Increase timeout for complex queries |
| CSV parsing issues | Check query returns proper tabular data |

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -am 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is released under the MIT License. See `LICENSE` file for details.

## Acknowledgments

- Built with [FastMCP](https://github.com/microsoft/mcp)
- Query functionality powered by [Dune Analytics](https://dune.com/)