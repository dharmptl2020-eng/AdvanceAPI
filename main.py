"""
GraphQL Server Integration with FastAPI
Serves Strawberry GraphQL alongside REST endpoints
"""
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from graphql_apis.schema import schema as graphql_schema

# Import REST API
from rest_apis.main import app as rest_app

# Create combined app
app = FastAPI(
    title="API Learning Platform",
    description="REST + GraphQL API with AI integration",
    version="1.0.0"
)

# Mount GraphQL at /graphql
graphql_app = GraphQL(graphql_schema, debug=True)

# Mount REST routes
app.include_router(rest_app.router)

# Mount GraphQL
app.mount("/graphql", graphql_app)

@app.get("/")
async def root():
    """API entry point with documentation links"""
    return {
        "message": "API Learning Platform",
        "endpoints": {
            "rest_docs": "http://localhost:8000/docs",
            "rest_redoc": "http://localhost:8000/redoc",
            "graphql": "http://localhost:8000/graphql",
            "health": "http://localhost:8000/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
