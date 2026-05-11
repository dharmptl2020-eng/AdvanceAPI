"""
Python API Development: A Quick Visual Guide

This file summarizes the key concepts you'll encounter
"""

# ============================================================================
# 1. PYDANTIC MODELS (REST API Data Validation)
# ============================================================================

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Post(BaseModel):
    """Automatic validation + OpenAPI documentation"""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)  # Required, validates
    content: str = Field(..., min_length=10)
    tags: List[str] = []  # Optional with default

# Usage: FastAPI automatically converts JSON → Post object
# Returns 422 if validation fails


# ============================================================================
# 2. FASTAPI ENDPOINTS (REST Architecture)
# ============================================================================

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# DEPENDENCY INJECTION - reusable services
async def get_current_user():
    return {"user_id": 1, "name": "Alice"}

# REST ENDPOINTS - match HTTP methods
@app.get("/posts")  # GET method - fetch
async def list_posts(skip: int = 0, limit: int = 10):
    """Query parameters: ?skip=0&limit=10"""
    return {"posts": [...]}

@app.post("/posts")  # POST method - create
async def create_post(post: Post, user = Depends(get_current_user)):
    """Body: { "title": "...", "content": "...", "tags": [...] }"""
    return {"id": 1, ...post}

@app.get("/posts/{post_id}")  # PATH PARAMETER
async def get_post(post_id: int):
    """URL: /posts/123"""
    return {"id": post_id, ...}

@app.put("/posts/{post_id}")  # PUT method - full update
async def update_post(post_id: int, post: Post):
    return {"id": post_id, ...post}

@app.delete("/posts/{post_id}")  # DELETE method - remove
async def delete_post(post_id: int):
    return {"deleted": True}


# ============================================================================
# 3. STRAWBERRY GRAPHQL (GraphQL Schema)
# ============================================================================

import strawberry
from typing import List, Optional

@strawberry.type
class Post:
    """GraphQL type = Python class with type hints"""
    id: int
    title: str
    content: str
    tags: List[str]
    
    @strawberry.field
    async def summary(self) -> str:
        """Field resolver - computed property"""
        return f"{self.title}: {self.content[:50]}..."

@strawberry.type
class Query:
    """Root query - all read operations"""
    
    @strawberry.field
    async def posts(self, author: Optional[str] = None) -> List[Post]:
        """Query: posts(author: "Alice") { title content }"""
        pass
    
    @strawberry.field
    async def post(self, id: int) -> Optional[Post]:
        """Query: post(id: 1) { title }"""
        pass

@strawberry.type
class Mutation:
    """Root mutation - all write operations"""
    
    @strawberry.mutation
    async def create_post(
        self,
        title: str,
        content: str,
        tags: List[str]
    ) -> Post:
        """Mutation: createPost(title: "...") { id title }"""
        pass

schema = strawberry.Schema(query=Query, mutation=Mutation)


# ============================================================================
# 4. ASYNC/AWAIT (Modern Python)
# ============================================================================

import asyncio
import httpx

# ❌ WRONG - Blocks other requests
def sync_fetch_users():
    for i in range(100):
        response = requests.get(f"https://api.example.com/users/{i}")  # Waits!
        print(response.json())

# ✅ CORRECT - Non-blocking, processes all concurrently
async def async_fetch_users():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"https://api.example.com/users/{i}") for i in range(100)]
        responses = await asyncio.gather(*tasks)  # Concurrent!
        for response in responses:
            print(response.json())

# Usage in FastAPI:
@app.get("/users")
async def list_users():
    """FastAPI runs this in thread pool if blocking, or async event loop"""
    return await async_fetch_users()


# ============================================================================
# 5. DEPENDENCY INJECTION (FastAPI Pattern)
# ============================================================================

# Define once, use everywhere
async def get_database():
    """Database connection dependency"""
    db = connect_to_postgres()
    yield db  # Clean up after
    db.close()

async def get_current_user(token: str):
    """Authentication dependency"""
    return verify_token(token)

# Inject automatically
@app.get("/protected")
async def protected_endpoint(
    db = Depends(get_database),
    user = Depends(get_current_user)
):
    """FastAPI calls dependencies, passes results"""
    return {"user": user, "data": db.query(...)}


# ============================================================================
# 6. GRAPHQL VS REST COMPARISON
# ============================================================================

"""
REST Endpoint: GET /users/1/posts
Response:
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "posts": [
    {"id": 1, "title": "...", "content": "...", ...},
    {"id": 2, "title": "...", "content": "...", ...}
  ]
}
Problem: Over-fetching! You get everything

---

GraphQL Query: query { user(id: 1) { name posts { title } } }
Response:
{
  "user": {
    "name": "Alice",
    "posts": [
      {"title": "Post 1"},
      {"title": "Post 2"}
    ]
  }
}
Benefit: Exact data requested, nothing more!
"""


# ============================================================================
# 7. AI INTEGRATION (LLM-Powered Features)
# ============================================================================

from openai import AsyncOpenAI

client = AsyncOpenAI()

async def analyze_post_with_ai(content: str):
    """Call OpenAI to analyze content"""
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Analyze this post"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Usage: Call from REST endpoint or GraphQL resolver
@app.post("/analyze")
async def analyze(text: str):
    insight = await analyze_post_with_ai(text)
    return {"insight": insight}


# ============================================================================
# 8. ERROR HANDLING (Standardized Responses)
# ============================================================================

from fastapi import HTTPException

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# FastAPI automatically returns:
# {"detail": "Post not found"}
# with 404 status code


# ============================================================================
# 9. TESTING PATTERN
# ============================================================================

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/posts",
            json={"title": "Test", "content": "Test content"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test"


# ============================================================================
# 10. COMMON GOTCHAS
# ============================================================================

"""
❌ Mistake 1: Blocking I/O in async function
@app.get("/data")
async def get_data():
    return requests.get("...").json()  # BLOCKS! Use httpx instead

✅ Correct:
@app.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        return (await client.get("...")).json()

---

❌ Mistake 2: N+1 queries in GraphQL
@strawberry.type
class User:
    @strawberry.field
    async def posts(self) -> List[Post]:
        # Called for EVERY user! If you fetch 100 users, 100 DB queries!
        return await db.query("SELECT * FROM posts WHERE user_id = ?", self.id)

✅ Correct: Use DataLoader
from strawberry.dataloader import DataLoader

async def load_posts_batch(user_ids):
    # ONE query for all users!
    return await db.query("SELECT * FROM posts WHERE user_id IN ?", user_ids)

post_loader = DataLoader(load_fn=load_posts_batch)

@strawberry.type
class User:
    @strawberry.field
    async def posts(self, info) -> List[Post]:
        return await info.context["post_loader"].load(self.id)

---

❌ Mistake 3: Type hints optional in FastAPI
@app.get("/posts")
def list_posts(skip, limit):  # What types are these?
    pass

✅ Correct:
@app.get("/posts")
async def list_posts(skip: int = 0, limit: int = 10):
    # FastAPI validates: /posts?skip=abc → 422 error
    pass
"""

print(__doc__)
