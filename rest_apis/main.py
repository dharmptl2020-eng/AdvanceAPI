"""
FastAPI REST API Starter Template
Modern Python stack with async/await, Pydantic validation, and OpenAI integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import os
from openai import AsyncOpenAI

app = FastAPI(
    title="API Learning Platform",
    description="REST API with AI integration for learning",
    version="1.0.0"
)

# ============================================================================
# Data Models (Pydantic)
# ============================================================================

class Post(BaseModel):
    """Blog post data model"""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    author: str
    created_at: Optional[datetime] = None
    tags: List[str] = []

class PostResponse(Post):
    """Enhanced response with metadata"""
    id: int
    created_at: datetime

class AIInsight(BaseModel):
    """AI-generated insight from post content"""
    post_id: int
    summary: str
    key_topics: List[str]
    sentiment: str

# ============================================================================
# In-memory Storage (replace with database later)
# ============================================================================

posts_db: List[Post] = []
post_counter = 0

# ============================================================================
# Dependency Injection
# ============================================================================

async def get_openai_client():
    """Provide OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    return AsyncOpenAI(api_key=api_key)

# ============================================================================
# REST Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/posts", response_model=PostResponse)
async def create_post(post: Post):
    """Create a new blog post"""
    global post_counter
    post_counter += 1
    post.id = post_counter
    post.created_at = datetime.now()
    posts_db.append(post)
    return post

@app.get("/posts", response_model=List[PostResponse])
async def list_posts(skip: int = 0, limit: int = 10):
    """List all posts with pagination"""
    return posts_db[skip:skip + limit]

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Retrieve a specific post"""
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, updated_post: Post):
    """Update an existing post"""
    for i, post in enumerate(posts_db):
        if post.id == post_id:
            updated_post.id = post_id
            updated_post.created_at = post.created_at
            posts_db[i] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    """Delete a post"""
    for i, post in enumerate(posts_db):
        if post.id == post_id:
            posts_db.pop(i)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")

# ============================================================================
# AI-Driven Endpoints
# ============================================================================

@app.post("/posts/{post_id}/analyze", response_model=AIInsight)
async def analyze_post_with_ai(
    post_id: int, 
    client: AsyncOpenAI = Depends(get_openai_client)
):
    """
    Use OpenAI to generate insights from post content
    Demonstrates AI integration point for learning
    """
    post = None
    for p in posts_db:
        if p.id == post_id:
            post = p
            break
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Call OpenAI API to analyze content
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert content analyst. Analyze the following blog post and provide: 1) A one-sentence summary, 2) Key topics (3-5 topics), 3) Overall sentiment (positive/neutral/negative). Format as JSON."
            },
            {
                "role": "user",
                "content": f"Title: {post.title}\n\nContent: {post.content}"
            }
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    # Parse response (simplified - add error handling in production)
    import json
    analysis = json.loads(response.choices[0].message.content)
    
    return AIInsight(
        post_id=post_id,
        summary=analysis.get("summary", ""),
        key_topics=analysis.get("topics", []),
        sentiment=analysis.get("sentiment", "neutral")
    )

@app.post("/query/natural-language")
async def query_with_natural_language(
    query: str,
    client: AsyncOpenAI = Depends(get_openai_client)
):
    """
    Convert natural language to API query
    Example of AI transforming user intent to structured data
    """
    prompt = f"""
Given this natural language query about blog posts, extract structured parameters:
Query: "{query}"

Return JSON with: action (list/create/search), filters (dict), limit (int)
Example: {{"action": "list", "filters": {{"author": "John"}}, "limit": 5}}
"""
    
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150
    )
    
    return {"parsed_query": response.choices[0].message.content}

# ============================================================================
# Error Handling & Responses
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Standardized error response"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.now().isoformat()
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
