# Python API Development Setup Guide

## Prerequisites
- Python 3.10+
- pip (Python package manager)
- OpenAI API key (for AI features)

## Quick Start

### 1. Set Up Environment
```bash
# Clone/navigate to workspace
cd /Users/hdpatel/APIs

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run the Server
```bash
# Start combined REST + GraphQL server
python -m uvicorn main:app --reload

# Visit documentation
# http://localhost:8000/docs          (Swagger UI)
# http://localhost:8000/graphql       (GraphQL endpoint)
# http://localhost:8000/redoc         (ReDoc)
# http://localhost:8000/openapi.json  (OpenAPI spec)
```

### 3. Run REST API Only
```bash
# Start FastAPI REST server only
python -m uvicorn rest_apis.main:app --reload

# Visit REST docs
# http://localhost:8000/docs
```

### 4. Run GraphQL Schema Directly
```bash
# Run the GraphQL schema file for local testing
python graphql_apis/schema.py
```

### 4. Try Learning Examples
```bash
# Consume public API (JSONPlaceholder)
python examples/learning_public_api.py
```

### 5. Generate Queries with AI
```bash
# Generate GraphQL queries from natural language
python ai-automation/query_generator.py
```

## File Structure After Setup

```
/APIs/
├── rest_apis/
│   └── main.py                    # FastAPI application with CRUD + AI
├── graphql_apis/
│   └── schema.py                  # Strawberry GraphQL schema
├── ai-automation/
│   └── query_generator.py         # LLM-powered query generation
├── examples/
│   └── learning_public_api.py     # Learning: consuming JSONPlaceholder API
├── docs/
│   ├── ARCHITECTURE.md            # System design & patterns
│   └── (to add: tutorials, API docs)
├── .github/
│   └── copilot-instructions.md    # AI agent guidelines
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # (to create)
```

## Development Workflow

### Adding a New REST Endpoint
1. Define Pydantic model in `rest_apis/main.py`
2. Create route handler with type hints
3. Use Depends() for injections
4. Test with `curl` or Postman

### Adding a GraphQL Query
1. Define `@strawberry.type` for data model
2. Create query resolver in `Query` class
3. Add field arguments if needed
4. Test with GraphQL playground

### Testing
```bash
# Run tests (setup pytest first)
pytest tests/

# Test specific file
pytest tests/test_rest_api.py -v

# Run with coverage
pytest --cov=rest_apis tests/
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### OpenAI API Key Issues
```bash
# Verify key is set
echo $OPENAI_API_KEY

# Check key is valid
python -c "from openai import AsyncOpenAI; print('OK')"
```

### Import Errors
```bash
# Verify virtual environment is active
which python

# Should show: /Users/hdpatel/APIs/venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. **Extend REST API**: Add database (PostgreSQL + SQLAlchemy)
2. **Add GraphQL Server**: Create main.py that serves GraphQL
3. **Implement Tests**: Create test suite for both APIs
4. **Add Authentication**: Implement JWT tokens
5. **Deploy**: Use Docker + cloud provider (AWS/GCP/Heroku)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [JSONPlaceholder - Fake API](https://jsonplaceholder.typicode.com/)
- [OpenAI API](https://platform.openai.com/docs)
