# MCP Server Development Framework

[中文文档](README_cn.md)

## Overview

A professional framework designed for enterprise-level Model Context Protocol (MCP) tool development, standardizing the MCP server development process to help developers rapidly build high-quality AI tools. By integrating FastAPI with FastAPI-MCP, this framework enables seamless transformation from traditional APIs to AI-callable tools.

### Key Features

- **MCP Tool Standardization**: Automatically convert traditional FastAPI endpoints into AI model-callable MCP tools
- **Interface-Implementation Separation**: Support clear separation between interface definitions and implementations, facilitating testing and environment switching
- **Dependency Injection Design**: Leverage FastAPI's dependency injection mechanism for flexible component composition and decoupling
- **Complete Development Pipeline**: Provide comprehensive toolchain support from development to testing and deployment
- **Example-Driven Documentation**: Demonstrate best practices through practical examples to accelerate onboarding

This framework is particularly suitable for:
- AI tool development teams
- Developers looking to transform existing APIs into AI tools
- Organizations implementing standardized microservice architectures

## Architecture

### Core Architecture

```
┌─────────────┐      ┌───────────────┐      ┌─────────────────┐
│   API Layer │ ──→ │ Service Layer  │ ──→ │ Implementation   │
└─────────────┘      └───────────────┘      └─────────────────┘
       ↓                                            
┌─────────────┐                                     
│  MCP Endpoint│ ←── FastAPI-MCP Auto-Conversion    
└─────────────┘                                     
```

### Key Components

- **FastAPI Application**: Provides the HTTP API service foundation
- **FastAPI-MCP**: Converts API endpoints to MCP tools
- **Service Interface Layer**: Defines service contracts through abstract base classes
- **Dependency Injection Providers**: Manages service instance creation and injection
- **Implementation Classes**: Includes Mock and Real implementations with environment-based switching

## Technology Stack

- **Python 3.10+**: Utilizing latest language features and type annotations
- **FastAPI**: High-performance asynchronous web framework
- **FastAPI-MCP**: Automatically exposes FastAPI endpoints as MCP tools
- **Development Toolchain**: Includes code quality checking and testing tools

## Quick Start

### Environment Setup

This framework uses `uv` as its package manager, providing faster dependency resolution and virtual environment management. For installation instructions, see the [uv official documentation](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Install dependencies and set up the development environment
make install
```

### Launch Example Service

```bash
# Start the development server
make dev
```

Once the service is running, you can:
- Access the API documentation at `http://localhost:5000/docs`
- Connect to the MCP endpoint at `http://localhost:5000/mcp` using an MCP client (e.g., Cursor, Claude Desktop)

## Project Structure

```
.
├── main.py                    # Application entry point and route definitions
├── services/                  # Service layer implementations
│   └── parking_service.py     # Example service (replaceable with custom services)
├── pyproject.toml             # Project configuration and dependency definitions
└── Makefile                   # Development and build tasks
```

## MCP Tool Development Guide

### Development Process Overview

1. **Define Service Interfaces**: Create abstract base classes to define service contracts
2. **Implement Services**: Develop Mock or Real implementations based on requirements
3. **Create API Endpoints**: Develop API interfaces using FastAPI
4. **Enable MCP Service**: Expose endpoints as AI tools through FastAPI-MCP

### Service Interfaces and Implementations

```python
# 1. Service Interface Definition
from abc import ABC, abstractmethod
from typing import Dict, Any

class DataService(ABC):
    @abstractmethod
    def get_data(self, id: str) -> Dict[str, Any]:
        """Data retrieval interface"""
        pass

# 2A. Mock Implementation - for development and testing
class DataServiceMockImpl(DataService):
    def get_data(self, id: str) -> Dict[str, Any]:
        return {"id": id, "name": "Test Data", "mock": True}

# 2B. Real Implementation - for production environment
class DataServiceImpl(DataService):
    def __init__(self, database_url: str):
        self.db = Database(database_url)
    
    def get_data(self, id: str) -> Dict[str, Any]:
        return self.db.query("SELECT * FROM data WHERE id = :id", {"id": id})

# 3. Dependency Injection Configuration
def get_data_service() -> DataService:
    # Choose implementation based on environment
    return DataServiceMockImpl() # or return DataServiceImpl(settings.DATABASE_URL)
```

### API and MCP Tool Definition

```python
from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

app = FastAPI()

# Request model
class ItemRequest(BaseModel):
    query: str = Field(..., description="Search query parameter")
    limit: int = Field(10, description="Result limit")

# API endpoint - automatically converted to an MCP tool
@app.post("/items/search", operation_id="search_items")
async def search_items(
    request: ItemRequest,
    service: DataService = Depends(get_data_service)
):
    result = service.search_items(request.query, request.limit)
    return {"items": result["items"], "total": len(result["items"])}

# Create and mount MCP service
mcp = FastApiMCP(
    app,
    name="example-service",
    description="Example MCP service",
    base_url="http://localhost:5000",
    include_operations=["search_items"]
)

# Mount MCP service at specified path
mcp.mount(mount_path="/mcp")
```

## Dependency Injection Explained

FastAPI's dependency injection system is an integral part of this framework, providing powerful and flexible dependency management capabilities.

### Dependency Injection Fundamentals

Dependency injection is a design pattern that allows dependencies (such as services, database connections, etc.) to be injected into components that use them, rather than having components create and manage dependencies themselves. In FastAPI, dependency injection is implemented through the `Depends` function.

```python
from fastapi import Depends

def get_db():
    """Database connection provider"""
    db = connect_to_db()
    try:
        yield db  # Using yield enables lifecycle management of dependencies
    finally:
        db.close()

@app.get("/items/")
async def get_items(db = Depends(get_db)):
    return db.query(Item).all()
```

### Dependency Types

FastAPI supports several types of dependency injection:

1. **Function Dependencies**: As shown above, using functions as dependency providers
2. **Class Dependencies**: Using classes as dependencies for more complex dependency management

```python
class DatabaseDependency:
    def __init__(self, settings = Depends(get_settings)):
        self.settings = settings
    
    def __call__(self):
        db = connect_to_db(self.settings.db_url)
        try:
            yield db
        finally:
            db.close()

@app.get("/users/")
async def get_users(db = Depends(DatabaseDependency())):
    return db.query(User).all()
```

3. **Nested Dependencies**: Dependencies can depend on other dependencies, forming a dependency tree

### Application in MCP Tool Development

In this framework, dependency injection is primarily used for:

1. **Service Instance Management**: Injecting service implementations into API endpoints
2. **Environment Adaptation**: Selecting different service implementations based on runtime environment
3. **Resource Lifecycle Management**: Managing the creation and release of resources like database connections

## FastAPI-MCP Features

### Automatic MCP Tool Generation

FastAPI-MCP can automatically convert FastAPI endpoints into MCP tools:

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Define a standard FastAPI endpoint
@app.post("/predict", operation_id="predict_sentiment")
async def predict_sentiment(text: str):
    return {"sentiment": "positive", "confidence": 0.92}

# Create and mount MCP service - automatically converts the above endpoint to an MCP tool
mcp = FastApiMCP(
    app,
    name="sentiment-analysis",
    description="Sentiment analysis service",
    base_url="http://localhost:5000",
    include_operations=["predict_sentiment"]
)

# Mount MCP service at specified path
mcp.mount(mount_path="/mcp")
```

### Tool Naming Best Practices

MCP tool names default to the API endpoint's `operation_id`. We recommend following these naming conventions:

- Use clear, descriptive names
- Adopt a verb_noun format (e.g., `predict_sentiment`, `find_nearby_parking`)
- Explicitly set `operation_id` rather than relying on auto-generation

```python
# Recommended: Explicitly set operation_id
@app.post("/parking/nearby", operation_id="find_nearby_parking")
async def find_nearby(request: NearbyRequest):
    # Implementation logic...
    pass

# Not recommended: Relying on auto-generated operation_id (generates something like "find_nearby_parking_nearby_post")
@app.post("/parking/nearby")
async def find_nearby(request: NearbyRequest):
    # Implementation logic...
    pass
```

## Testing and Quality Assurance

This framework supports multi-level testing strategies:

```bash
# Run code quality checks
make check

# Run test suite
make test
```

### Testing Strategies

- **Unit Testing**: Test individual components using Mock service implementations
- **Integration Testing**: Test interactions between components
- **API Testing**: Verify HTTP interface behavior
- **MCP Tool Testing**: Validate AI tool functionality

## Performance Optimization

To ensure high performance of MCP tools, we recommend:

- **Asynchronous Processing**: Leverage FastAPI's async features for concurrent request handling
- **Caching Strategies**: Implement caching for frequently requested data
- **Batch Processing**: Design APIs that support batch operations to reduce call frequency

## Contribution Guidelines

Contributions to this framework are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

[MIT License](LICENSE)

## References

- [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework
- [FastAPI-MCP](https://github.com/tadata-org/fastapi_mcp) - MCP tool auto-generation library
