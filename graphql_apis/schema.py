"""
Strawberry GraphQL Schema Starter Template
Modern Python GraphQL with type hints, async resolvers, and AI integration
"""
import strawberry
from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass
import os
from openai import AsyncOpenAI

# ============================================================================
# Data Models
# ============================================================================

@strawberry.type
class Post:
    """Blog post type"""
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    tags: List[str]

@strawberry.type
class AIInsight:
    """AI-generated content analysis"""
    post_id: int
    summary: str
    key_topics: List[str]
    sentiment: str

@strawberry.type
class User:
    """User type with resolver for posts"""
    id: int
    name: str
    email: str
    
    @strawberry.field
    async def posts(self) -> List[Post]:
        """Lazy-load user's posts (prevent N+1 queries)"""
        # In production, use DataLoader pattern
        return [p for p in POSTS_DB if p.author == self.name]

@strawberry.type
class PaginatedPosts:
    """Cursor-based pagination for large datasets"""
    nodes: List[Post]
    cursor: Optional[str]
    has_next: bool

# ============================================================================
# In-memory Storage
# ============================================================================

POSTS_DB: List[Post] = [
    Post(
        id=1,
        title="Getting Started with GraphQL",
        content="GraphQL is a query language for APIs...",
        author="Alice",
        created_at=datetime.now(),
        tags=["graphql", "api", "learning"]
    )
]

USERS_DB: List[User] = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com")
]

post_counter = 1

# ============================================================================
# Query Resolvers (Read Operations)
# ============================================================================

@strawberry.type
class Query:
    """Root query type - defines all read operations"""
    
    @strawberry.field
    async def post(self, id: int) -> Optional[Post]:
        """Fetch a single post by ID"""
        for post in POSTS_DB:
            if post.id == id:
                return post
        return None
    
    @strawberry.field
    async def posts(
        self, 
        skip: int = 0, 
        limit: int = 10,
        author: Optional[str] = None
    ) -> List[Post]:
        """
        Fetch posts with optional filtering and pagination
        Demonstrates query parameters and filtering
        """
        results = POSTS_DB
        if author:
            results = [p for p in results if p.author == author]
        return results[skip:skip + limit]
    
    @strawberry.field
    async def posts_paginated(
        self,
        limit: int = 10,
        cursor: Optional[str] = None
    ) -> PaginatedPosts:
        """
        Cursor-based pagination for production APIs
        Better for real-time data and large datasets
        """
        start_idx = int(cursor) if cursor else 0
        nodes = POSTS_DB[start_idx:start_idx + limit]
        next_cursor = str(start_idx + limit) if start_idx + limit < len(POSTS_DB) else None
        
        return PaginatedPosts(
            nodes=nodes,
            cursor=next_cursor,
            has_next=next_cursor is not None
        )
    
    @strawberry.field
    async def user(self, id: int) -> Optional[User]:
        """Fetch user by ID (demonstrates N+1 prevention with lazy loading)"""
        for user in USERS_DB:
            if user.id == id:
                return user
        return None
    
    @strawberry.field
    async def search_posts(self, query: str) -> List[Post]:
        """
        Full-text search across posts
        In production, use Elasticsearch or database full-text search
        """
        query_lower = query.lower()
        return [
            p for p in POSTS_DB 
            if query_lower in p.title.lower() or query_lower in p.content.lower()
        ]

# ============================================================================
# Mutation Resolvers (Write Operations)
# ============================================================================

@strawberry.type
class Mutation:
    """Root mutation type - defines all write operations"""
    
    @strawberry.mutation
    async def create_post(
        self,
        title: str,
        content: str,
        author: str,
        tags: Optional[List[str]] = None
    ) -> Post:
        """Create a new post - specific mutation for single responsibility"""
        global post_counter
        post_counter += 1
        if tags is None:
            tags = []
        new_post = Post(
            id=post_counter,
            title=title,
            content=content,
            author=author,
            created_at=datetime.now(),
            tags=tags
        )
        POSTS_DB.append(new_post)
        return new_post
    
    @strawberry.mutation
    async def update_post(
        self,
        id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Post]:
        """Update post fields - partial updates supported"""
        for post in POSTS_DB:
            if post.id == id:
                if title is not None:
                    post.title = title
                if content is not None:
                    post.content = content
                if tags is not None:
                    post.tags = tags
                return post
        return None
    
    @strawberry.mutation
    async def delete_post(self, id: int) -> bool:
        """Delete a post - returns success status"""
        for i, post in enumerate(POSTS_DB):
            if post.id == id:
                POSTS_DB.pop(i)
                return True
        return False
    
    @strawberry.mutation
    async def analyze_post_with_ai(self, post_id: int) -> Optional[AIInsight]:
        """
        AI integration mutation: Analyze post content
        Demonstrates calling external AI services from GraphQL
        """
        post = None
        for p in POSTS_DB:
            if p.id == post_id:
                post = p
                break
        
        if not post:
            return None
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        
        client = AsyncOpenAI(api_key=api_key)
        
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the blog post and return JSON with: summary (str), topics (list), sentiment (str)"
                },
                {
                    "role": "user",
                    "content": f"Title: {post.title}\n\nContent: {post.content}"
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        
        return AIInsight(
            post_id=post_id,
            summary=analysis.get("summary", ""),
            key_topics=analysis.get("topics", []),
            sentiment=analysis.get("sentiment", "neutral")
        )

# ============================================================================
# Schema Definition
# ============================================================================

schema = strawberry.Schema(query=Query, mutation=Mutation)

if __name__ == "__main__":
    import asyncio
    
    # Example GraphQL query
    query = """
    query {
        posts(limit: 5) {
            id
            title
            author
            tags
        }
        user(id: 1) {
            name
            email
            posts {
                title
            }
        }
    }
    """
    
    result = asyncio.run(schema.execute(query))
    print(result.data)
