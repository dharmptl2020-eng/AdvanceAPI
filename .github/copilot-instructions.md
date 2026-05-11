# Copilot Instructions for API Development Workspace

## Overview
This workspace is a learning and development environment for APIs, progressing from beginner to expert levels, with emphasis on:
- API architecture and design patterns
- GraphQL implementation and best practices
- AI-driven automation for API development and testing
- Production-ready API development practices

## Project Structure (to be populated)
```
/APIs
├── rest_apis/           # RESTful API examples (beginner → intermediate)
├── graphql_apis/        # GraphQL implementations (intermediate → expert)
├── ai-automation/       # AI-driven API testing and generation
├── docs/                # Learning materials and architecture guides
├── examples/            # Code examples and templates
└── tools/               # Utility scripts for API development
```

## API Development Progression

### Beginner Level
- **REST Fundamentals**: Request/response structure, HTTP methods (GET, POST, PUT, DELETE), status codes
- **Authentication**: API keys, basic auth, introduction to JWT
- **Data Formats**: JSON/XML serialization, content negotiation
- **Tools**: Postman/Insomnia for testing, curl basics

### Intermediate Level
- **API Design**: RESTful conventions, resource modeling, versioning strategies
- **GraphQL Basics**: Query language concepts, schema design, resolvers
- **Error Handling**: Standardized error responses, retry logic
- **Documentation**: OpenAPI/Swagger specs, schema documentation

### Expert Level
- **Advanced GraphQL**: Federation, subscriptions, directive systems, N+1 query optimization
- **Performance**: Caching strategies, rate limiting, pagination, cursor-based navigation
- **Security**: OAuth 2.0, API gateways, CORS, input validation, SQL injection prevention
- **Observability**: Structured logging, tracing (OpenTelemetry), metrics collection

## GraphQL Focus Areas

### Schema Design
- Prefer nullable fields strategically; use non-null (`!`) for guaranteed data
- Design mutations to be specific and predictable (avoid massive update objects)
- Use custom scalar types for domain-specific data (Date, DateTime, Email, UUID)
- Example: See `graphql_apis/schema/` for type definitions

### Performance Optimization
- Use DataLoader pattern to prevent N+1 query problems
- Implement query complexity analysis to prevent expensive queries
- Leverage field-level resolvers for lazy-loading relationships
- Example patterns: `graphql_apis/resolvers/` 

### AI Integration Points
- Generate GraphQL queries from natural language via LLMs
- Auto-generate test cases based on schema
- Create mutation builders from type definitions
- Document resolvers with examples for AI agents

## AI Automation & Use Cases

### Code Generation
- Generate API clients from OpenAPI/GraphQL specs
- Create CRUD endpoints from data models
- Generate test suites with parametrized cases

### Testing Automation
- Property-based testing with AI-generated test data
- Automatic API contract verification
- Load testing simulation generation

### Documentation Generation
- Extract examples from working code
- Generate API guides from schemas
- Create integration walkthroughs

## Key Conventions & Patterns

### API Response Structure
```json
{
  "data": {},           // Actual response payload (GraphQL or REST)
  "meta": {
    "timestamp": "ISO-8601",
    "version": "v1"
  },
  "errors": []          // Array of error objects (if applicable)
}
```

### Error Handling
- Use consistent error codes and messages
- Include error context and remediation steps
- Log errors with correlation IDs for tracing

### GraphQL Query Patterns
- Always use fragments for repeated fields
- Implement query complexity scoring
- Require authentication at resolver level, not just HTTP

### Testing Approach
- Unit tests for resolvers and business logic
- Integration tests with real databases/services
- AI-driven property-based testing for edge cases

## Development Workflow

### Quick Start Commands
```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run REST API (FastAPI)
python -m uvicorn rest_apis.main:app --reload
# → Swagger UI: http://localhost:8000/docs

# Test with public API (JSONPlaceholder)
python examples/learning_public_api.py

# Generate AI queries
OPENAI_API_KEY=sk-... python ai-automation/query_generator.py
```

### Key Files for Reference
- **REST API**: `rest_apis/main.py` - FastAPI with CRUD + AI endpoints
- **GraphQL Schema**: `graphql_apis/schema.py` - Strawberry types & resolvers
- **Learning Example**: `examples/learning_public_api.py` - Consuming JSONPlaceholder API
- **AI Automation**: `ai-automation/query_generator.py` - LLM-powered query generation
- **Architecture**: `docs/ARCHITECTURE.md` - Design patterns & data flows

## External Dependencies & Integration

### Core Technologies (Selected Stack)
- **REST**: FastAPI (async-first Python framework)
- **GraphQL**: Strawberry (type-hint driven, dataclass-based)
- **Server**: Uvicorn (ASGI server for async support)
- **Validation**: Pydantic (automatic OpenAPI schema)
- **Databases**: PostgreSQL (future) + SQLAlchemy ORM
- **Testing**: Pytest + pytest-asyncio
- **AI Integration**: OpenAI API (primary), Anthropic (alternative)

### Python-Specific Details
- **Type Hints**: Required for FastAPI automatic documentation and validation
- **Async/Await**: Use throughout for I/O operations (database, API calls)
- **Dependency Injection**: FastAPI's `Depends()` pattern for managing services
- **Pydantic Models**: Serve as both validation schema and automatic OpenAPI types

### API Tools & Platforms
- Swagger UI (`/docs`) - Built into FastAPI
- ReDoc (`/redoc`) - FastAPI REST documentation
- GraphQL Playground - For Strawberry queries
- JSONPlaceholder - Public API for learning
- OpenAI API - For AI-driven features

## AI Agent Responsibilities

When working on code in this workspace, prioritize:

1. **Pattern Recognition**: Identify established patterns in `examples/` and apply consistently
2. **Schema-First Development**: Generate code from GraphQL/OpenAPI schemas, not vice versa
3. **Testability**: Generate solutions with corresponding test cases
4. **Documentation**: Include resolver comments, argument descriptions, and error scenarios
5. **Performance**: Flag potential N+1 problems, recommend caching strategies

## Next Steps for Setup

- [ ] Choose API framework (REST technology stack)
- [ ] Select GraphQL implementation
- [ ] Set up development environment (Node/Python/Go)
- [ ] Initialize database schema templates
- [ ] Create first CRUD API example
- [ ] Document local development commands
- [ ] Set up AI testing framework
- [ ] Create GraphQL schema examples

---

**Last Updated**: May 10, 2026  
**Maintained By**: Technical Manager  
**Focus Areas**: API Design, GraphQL, AI Automation
