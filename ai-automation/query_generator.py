"""
AI Automation: Natural Language to GraphQL Query Generator
Demonstrates AI-driven API development
Uses OpenAI to convert natural language to executable GraphQL queries
"""
import os
from openai import AsyncOpenAI
import asyncio
import json

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# Schema Context for AI
# ============================================================================

GRAPHQL_SCHEMA_CONTEXT = """
GraphQL Schema available:
- Query:
  - posts(skip: Int, limit: Int, author: String): [Post]
  - post(id: Int): Post
  - user(id: Int): User
  - searchPosts(query: String): [Post]

- Types:
  - Post: { id, title, content, author, createdAt, tags }
  - User: { id, name, email, posts: [Post] }

- Mutation:
  - createPost(title: String, content: String, author: String, tags: [String]): Post
  - updatePost(id: Int, title: String, content: String): Post
  - deletePost(id: Int): Boolean
"""

# ============================================================================
# Query Generation
# ============================================================================

async def natural_language_to_graphql(user_query: str) -> dict:
    """
    Convert natural language to GraphQL query
    Example: "Show me Alice's posts" -> GraphQL query
    """
    prompt = f"""
You are a GraphQL expert. Convert the user's natural language query to a valid GraphQL query.

{GRAPHQL_SCHEMA_CONTEXT}

User Query: "{user_query}"

Return ONLY a valid GraphQL query (wrapped in triple backticks with 'graphql' language identifier).
Do not include any explanation, just the query.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )
    
    # Extract GraphQL query from response
    content = response.choices[0].message.content
    query = content.strip('```graphql').strip('```').strip()
    
    return {"original_query": user_query, "generated_graphql": query}


async def test_generator_to_graphql(test_intent: str) -> dict:
    """
    Generate test queries from test intent
    Example: "Find all posts about GraphQL" -> GraphQL query for testing
    """
    prompt = f"""
You are a GraphQL testing expert. Generate a comprehensive GraphQL query for testing.

Test Intent: "{test_intent}"

{GRAPHQL_SCHEMA_CONTEXT}

Return a GraphQL query that would test this scenario. Include:
1. The main query to fetch data
2. All relevant fields
3. Appropriate filters/parameters

Format: Return ONLY the GraphQL query in backticks.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=400
    )
    
    content = response.choices[0].message.content
    query = content.strip('```graphql').strip('```').strip()
    
    return {"test_intent": test_intent, "generated_test_query": query}


async def generate_test_data(schema_context: str) -> dict:
    """
    Generate realistic test data from schema
    Example: Create mock Post objects matching the schema
    """
    prompt = f"""
You are a test data generation expert. Generate realistic test data for the GraphQL schema.

{schema_context}

Generate 3 sample Post objects with realistic data. Return as JSON array.
Example format:
[
  {{"id": 1, "title": "...", "content": "...", "author": "...", "tags": [...]}},
  ...
]

Return ONLY the JSON array, no explanation.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    content = response.choices[0].message.content
    test_data = json.loads(content)
    
    return {"generated_test_data": test_data}


async def optimize_graphql_query(query: str) -> dict:
    """
    AI-driven query optimization
    Analyzes queries for N+1 problems, complexity issues, etc.
    """
    prompt = f"""
You are a GraphQL performance expert. Analyze this GraphQL query for optimization opportunities.

Query:
```graphql
{query}
```

Identify:
1. Potential N+1 problems
2. Query complexity issues
3. Missing pagination
4. Redundant field requests

Return a JSON object with:
{{"issues": [...], "optimizations": [...], "optimized_query": "..."}}

Return ONLY valid JSON.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=400
    )
    
    content = response.choices[0].message.content
    analysis = json.loads(content)
    
    return analysis


# ============================================================================
# AI Test Generation
# ============================================================================

async def generate_mutation_tests(mutation_name: str) -> dict:
    """
    Generate comprehensive test cases for a mutation
    Includes happy path, edge cases, error scenarios
    """
    prompt = f"""
Generate comprehensive test cases for the "{mutation_name}" GraphQL mutation.

Test scenarios should cover:
1. Happy path (valid inputs)
2. Edge cases (empty strings, max length, special characters)
3. Error cases (invalid IDs, permissions, validation errors)
4. Concurrency scenarios

Return as JSON with test cases:
{{
  "test_cases": [
    {{"name": "...", "input": {...}, "expected": {...}}},
    ...
  ]
}}

Return ONLY valid JSON.
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )
    
    content = response.choices[0].message.content
    test_cases = json.loads(content)
    
    return test_cases


# ============================================================================
# Example Usage & Testing
# ============================================================================

async def main():
    """Run demonstration of AI query generation"""
    
    print("\n" + "="*60)
    print("AI AUTOMATION: Natural Language to GraphQL")
    print("="*60)
    
    # Test 1: Natural language to GraphQL
    print("\n[1] Converting natural language to GraphQL...")
    result = await natural_language_to_graphql("Show me all posts about GraphQL by Alice")
    print(f"User Query: {result['original_query']}")
    print(f"Generated GraphQL:\n{result['generated_graphql']}")
    
    # Test 2: Generate test queries
    print("\n[2] Generating test queries...")
    test_result = await test_generator_to_graphql("Fetch all posts and verify pagination works with limit 10")
    print(f"Test Intent: {test_result['test_intent']}")
    print(f"Generated Test Query:\n{test_result['generated_test_query']}")
    
    # Test 3: Generate test data
    print("\n[3] Generating test data...")
    data_result = await generate_test_data(GRAPHQL_SCHEMA_CONTEXT)
    print(f"Generated Test Data: {json.dumps(data_result['generated_test_data'], indent=2)}")
    
    # Test 4: Query optimization
    print("\n[4] Analyzing query for optimization...")
    sample_query = """
    query {
      posts(limit: 100) {
        id
        title
        author { name }
      }
    }
    """
    optimization = await optimize_graphql_query(sample_query)
    print(f"Optimization Analysis: {json.dumps(optimization, indent=2)}")
    
    # Test 5: Mutation tests
    print("\n[5] Generating mutation test cases...")
    mutation_tests = await generate_mutation_tests("createPost")
    print(f"Test Cases: {json.dumps(mutation_tests, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
