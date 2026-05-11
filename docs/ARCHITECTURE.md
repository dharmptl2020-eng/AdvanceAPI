# API Architecture Guide

## Project Overview

This workspace contains modern API learning materials organized by complexity level, with emphasis on Python, GraphQL, and AI automation.

## Tech Stack

### REST API (FastAPI)
- **Framework**: FastAPI (async-first, built on Starlette)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic (automatic OpenAPI schema generation)
- **Key Features**: 
  - Type hints for automatic documentation
  - Dependency injection system
  - Async/await support for I/O operations
  - Automatic API documentation at `/docs`

### GraphQL (Strawberry)
- **Framework**: Strawberry (dataclass-based, modern)
- **Key Features**:
  - Type hints drive schema generation
  - Async resolver support
  - Schema validation and complexity analysis
  - Integration with FastAPI for hybrid APIs

### Database (Production)
- **Primary**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for schema management
- **In Memory**: Python lists (learning examples only)

### AI Integration
- **OpenAI API**: For content analysis and query generation
- **Anthropic API**: Alternative AI provider (future)
- **Use Cases**: Query generation, test automation, documentation

## Architecture Patterns

### 1. Layered Architecture

```
API Layer (REST/GraphQL endpoints)
    ↓
Business Logic Layer (resolvers, service classes)
    ↓
Data Access Layer (ORM, repositories)
    ↓
Database Layer
```

### 2. Dependency Injection (FastAPI)

```python
async def get_db_session():
    """Provides database session"""
    ...

@app.get("/posts")
async def list_posts(db: Session = Depends(get_db_session)):
    """Automatically injects dependency"""
    ...
```

### 3. GraphQL Resolver Pattern

```python
@strawberry.type
class User:
    id: int
    name: str
    
    @strawberry.field
    async def posts(self) -> List[Post]:
        """Lazy-loaded resolver prevents N+1 queries"""
        return await fetch_user_posts(self.id)
```

### 4. AI Integration Points

```
User Input → LLM (OpenAI) → Structured Output
Examples:
- "Show me GraphQL posts" → GraphQL query
- Query text → Test cases
- API schema → Documentation
```

## Data Flow Examples

### REST API: Create Post

```
POST /posts {title, content, author}
    ↓
FastAPI validates with Pydantic
    ↓
Dependency injection provides DB session
    ↓
Business logic inserts into database
    ↓
Response: {id, title, content, created_at, ...}
```

### GraphQL: Fetch User with Posts

```
GraphQL Query: user(id: 1) { name, posts { title } }
    ↓
Query resolver executes
    ↓
User resolver returns user object
    ↓
Posts field resolver (lazy-load) fetches related posts
    ↓
Response: Exactly requested fields, nothing more
```

### AI: Generate Test Cases

```
User Intent: "Test the createPost mutation"
    ↓
OpenAI analyzes mutation schema
    ↓
Generates 5-10 test scenarios (happy/edge/error cases)
    ↓
Returns parametrized test data
    ↓
Tests execute against API
```

## Learning Path

### Phase 1: REST Fundamentals (Beginner)
- Start with `rest_apis/main.py`
- Understand HTTP methods, status codes
- Try JSONPlaceholder example in `examples/learning_public_api.py`
- Build simple CRUD endpoints

### Phase 2: GraphQL Basics (Intermediate)
- Study `graphql_apis/schema.py`
- Understand queries vs mutations
- Implement type-safe schema
- Compare REST vs GraphQL benefits

### Phase 3: AI-Driven Development (Advanced)
- Use `ai-automation/query_generator.py`
- Generate queries from natural language
- Auto-generate test cases
- Build documentation from schemas

### Phase 4: Production Patterns (Expert)
- Database integration (SQLAlchemy)
- Authentication (JWT)
- Error handling and observability
- Performance optimization (DataLoader, query complexity)

## Key Files Reference

| File | Purpose | Level |
|------|---------|-------|
| `rest_apis/main.py` | FastAPI REST example with AI | Beginner-Intermediate |
| `graphql_apis/schema.py` | Strawberry GraphQL schema | Intermediate-Expert |
| `examples/learning_public_api.py` | Consuming public APIs | Beginner |
| `ai-automation/query_generator.py` | LLM-driven query generation | Advanced |
| `requirements.txt` | All Python dependencies | - |

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run REST API
python -m uvicorn rest_apis.main:app --reload

# Run GraphQL API
python -m uvicorn graphql_apis.main:app --reload

# Run learning examples
python examples/learning_public_api.py

# Generate queries with AI
OPENAI_API_KEY=sk-... python ai-automation/query_generator.py
```

## Performance Considerations

1. **N+1 Query Problem**: Use DataLoader in GraphQL resolvers
2. **Query Complexity**: Limit recursive query depth
3. **Pagination**: Always paginate large datasets (cursor-based preferred)
4. **Caching**: Implement HTTP caching headers, Redis for session data
5. **Rate Limiting**: Prevent abuse with token bucket algorithm

## Security Checklist

- [ ] Validate all input (Pydantic handles this)
- [ ] Use HTTPS in production
- [ ] Implement authentication (JWT recommended)
- [ ] Add authorization checks at resolver level
- [ ] Sanitize error messages (don't leak internal details)
- [ ] Set CORS policies appropriately
- [ ] Use environment variables for secrets

## AI Agent Notes

When building new features:
1. Check `examples/` for similar patterns
2. Prefer schema-first (GraphQL schema or OpenAPI)
3. Add tests alongside features
4. Document resolver arguments and error scenarios
5. Use AI to generate test data, queries, and documentation
