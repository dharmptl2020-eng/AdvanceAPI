# API Learning & Development Workspace

Complete learning environment for API development from beginner to expert level, with focus on **Python, FastAPI, GraphQL, and AI automation**.

## 🚀 Quick Start

```bash
# 1. Set up environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Start combined REST + GraphQL server
python -m uvicorn main:app --reload
# → REST docs: http://localhost:8000/docs
# → GraphQL: http://localhost:8000/graphql

# 3. Start REST API only
python -m uvicorn rest_apis.main:app --reload
# → REST docs: http://localhost:8000/docs

# 4. Try examples
python examples/learning_public_api.py

# 5. Generate AI queries
OPENAI_API_KEY=sk-... python ai-automation/query_generator.py
```

See [SETUP.md](SETUP.md) for detailed setup instructions.

## 📚 Learning Path

### Beginner
- REST fundamentals with FastAPI (`rest_apis/main.py`)
- HTTP methods, status codes, request/response
- Consuming public APIs (`examples/learning_public_api.py`)

### Intermediate  
- GraphQL schema design (`graphql_apis/schema.py`)
- Data modeling with type hints
- Comparing REST vs GraphQL

### Advanced
- AI-driven query generation (`ai-automation/query_generator.py`)
- Performance optimization (N+1 prevention, pagination)
- Production patterns (auth, error handling, observability)

## 📁 Project Structure

```
/APIs/
├── rest_apis/           # FastAPI REST API with CRUD + AI
├── graphql_apis/        # Strawberry GraphQL schema
├── ai-automation/       # LLM-powered query/test generation
├── examples/            # Learning examples (JSONPlaceholder API)
├── docs/                # Architecture guides
├── requirements.txt     # Python dependencies
└── SETUP.md            # Installation guide
```

## 🏗️ Modern Stack

- **REST**: FastAPI + Uvicorn + Pydantic
- **GraphQL**: Strawberry with async resolvers
- **Database**: PostgreSQL + SQLAlchemy (future)
- **AI**: OpenAI API for query generation
- **Testing**: Pytest + pytest-asyncio

## 🤖 AI Features

- **Query Generator**: Natural language → GraphQL queries
- **Test Generator**: Auto-generate test cases from schema
- **Test Data**: Create realistic mock data
- **Query Optimizer**: Analyze and optimize GraphQL queries

## 📖 Key Examples

| Example | Purpose | Level |
|---------|---------|-------|
| `rest_apis/main.py` | Full REST API with AI endpoints | Beginner-Intermediate |
| `graphql_apis/schema.py` | GraphQL schema with resolvers | Intermediate-Expert |
| `examples/learning_public_api.py` | Consuming JSONPlaceholder API | Beginner |
| `ai-automation/query_generator.py` | LLM-driven automation | Advanced |

## 🔗 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [JSONPlaceholder - Free Fake API](https://jsonplaceholder.typicode.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 📝 Next Steps

- [ ] Complete setup and run examples
- [ ] Study REST API patterns in `rest_apis/main.py`
- [ ] Explore GraphQL schema in `graphql_apis/schema.py`
- [ ] Try public API examples
- [ ] Generate queries using AI automation
- [ ] Add database integration (PostgreSQL)
- [ ] Implement authentication (JWT)
- [ ] Build comprehensive test suite

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design patterns and data flow diagrams.
