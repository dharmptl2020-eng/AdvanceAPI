"""
Learning Example: Consuming Public APIs
Demonstrates beginner-level API consumption with JSONPlaceholder
Good starting point for understanding HTTP requests, responses, and data handling
"""
import httpx
import asyncio
from typing import Optional, List
from datetime import datetime

# ============================================================================
# JSONPlaceholder: Free fake API for learning
# https://jsonplaceholder.typicode.com/
# ============================================================================

BASE_URL = "https://jsonplaceholder.typicode.com"

class JSONPlaceholderAPI:
    """Simple wrapper around JSONPlaceholder API"""
    
    def __init__(self):
        self.client = httpx.Client(base_url=BASE_URL)
    
    # ========================================================================
    # Beginner: Basic GET Requests
    # ========================================================================
    
    def get_all_posts(self) -> List[dict]:
        """Fetch all posts - simplest API call"""
        response = self.client.get("/posts")
        response.raise_for_status()  # Raise exception if status != 2xx
        return response.json()
    
    def get_post(self, post_id: int) -> dict:
        """Fetch a single post by ID"""
        response = self.client.get(f"/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    
    def get_user(self, user_id: int) -> dict:
        """Fetch a single user"""
        response = self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    # ========================================================================
    # Intermediate: Query Parameters & Filtering
    # ========================================================================
    
    def get_posts_by_user(self, user_id: int) -> List[dict]:
        """Filter posts by user ID using query parameter"""
        response = self.client.get("/posts", params={"userId": user_id})
        response.raise_for_status()
        return response.json()
    
    def get_posts_with_comments(self, post_id: int) -> dict:
        """Fetch post with nested comments - nested resources"""
        response = self.client.get(f"/posts/{post_id}/comments")
        response.raise_for_status()
        return response.json()
    
    # ========================================================================
    # Intermediate: POST Requests (Create)
    # ========================================================================
    
    def create_post(self, user_id: int, title: str, body: str) -> dict:
        """Create a new post - typically returns the created object with ID"""
        payload = {
            "userId": user_id,
            "title": title,
            "body": body
        }
        response = self.client.post("/posts", json=payload)
        response.raise_for_status()
        return response.json()
    
    # ========================================================================
    # Intermediate: PUT/PATCH Requests (Update)
    # ========================================================================
    
    def update_post(self, post_id: int, title: str, body: str) -> dict:
        """Full update (PUT) - replaces entire resource"""
        payload = {
            "userId": 1,  # Mock value
            "title": title,
            "body": body
        }
        response = self.client.put(f"/posts/{post_id}", json=payload)
        response.raise_for_status()
        return response.json()
    
    def patch_post(self, post_id: int, title: Optional[str] = None) -> dict:
        """Partial update (PATCH) - updates only specified fields"""
        payload = {}
        if title:
            payload["title"] = title
        response = self.client.patch(f"/posts/{post_id}", json=payload)
        response.raise_for_status()
        return response.json()
    
    # ========================================================================
    # Intermediate: DELETE Requests
    # ========================================================================
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a resource"""
        response = self.client.delete(f"/posts/{post_id}")
        response.raise_for_status()
        return response.status_code == 200
    
    # ========================================================================
    # Advanced: Error Handling
    # ========================================================================
    
    def get_post_safe(self, post_id: int) -> Optional[dict]:
        """Fetch post with comprehensive error handling"""
        try:
            response = self.client.get(f"/posts/{post_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


# ============================================================================
# Async Example (Modern Python approach)
# ============================================================================

class AsyncJSONPlaceholderAPI:
    """Async version for concurrent requests - better performance"""
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL)
        return self
    
    async def __aexit__(self, *args):
        await self.client.aclose()
    
    async def get_all_posts(self) -> List[dict]:
        """Fetch all posts asynchronously"""
        response = await self.client.get("/posts")
        response.raise_for_status()
        return response.json()
    
    async def get_user(self, user_id: int) -> dict:
        """Fetch user asynchronously"""
        response = await self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    async def fetch_posts_and_users_concurrently(self, user_ids: List[int]):
        """
        Demonstrate concurrent requests - faster than sequential
        Makes multiple requests in parallel
        """
        posts_task = self.client.get("/posts")
        user_tasks = [self.client.get(f"/users/{uid}") for uid in user_ids]
        
        results = await asyncio.gather(posts_task, *user_tasks)
        
        posts = results[0].json()
        users = [r.json() for r in results[1:]]
        
        return {"posts": posts, "users": users}


# ============================================================================
# Learning Examples
# ============================================================================

def example_beginner():
    """Beginner example: Basic API consumption"""
    print("\n=== BEGINNER EXAMPLE ===")
    api = JSONPlaceholderAPI()
    
    # Fetch first post
    post = api.get_post(1)
    print(f"Post 1: {post['title']}")
    print(f"Body: {post['body'][:50]}...")
    
    # Fetch user
    user = api.get_user(1)
    print(f"User: {user['name']} ({user['email']})")


def example_intermediate():
    """Intermediate example: Filtering and relationships"""
    print("\n=== INTERMEDIATE EXAMPLE ===")
    api = JSONPlaceholderAPI()
    
    # Get all posts by user 1
    user_posts = api.get_posts_by_user(1)
    print(f"User 1 has {len(user_posts)} posts")
    
    # Get comments on post 1
    comments = api.get_posts_with_comments(1)
    print(f"Post 1 has {len(comments)} comments")
    
    # Create a new post
    new_post = api.create_post(1, "My Learning Post", "This is a test post")
    print(f"Created post with ID: {new_post['id']}")


def example_error_handling():
    """Advanced example: Robust error handling"""
    print("\n=== ERROR HANDLING EXAMPLE ===")
    api = JSONPlaceholderAPI()
    
    # Try to fetch non-existent post
    post = api.get_post_safe(99999)
    if post:
        print(f"Post found: {post['title']}")
    else:
        print("Post not found (handled gracefully)")


async def example_async():
    """Modern example: Async/await for concurrent requests"""
    print("\n=== ASYNC EXAMPLE ===")
    
    async with AsyncJSONPlaceholderAPI() as api:
        # Sequential approach (slower)
        start = datetime.now()
        posts = await api.get_all_posts()
        user = await api.get_user(1)
        sequential_time = (datetime.now() - start).total_seconds()
        print(f"Sequential: {sequential_time:.2f}s - {len(posts)} posts, user: {user['name']}")
        
        # Concurrent approach (faster)
        start = datetime.now()
        result = await api.fetch_posts_and_users_concurrently([1, 2, 3])
        concurrent_time = (datetime.now() - start).total_seconds()
        print(f"Concurrent: {concurrent_time:.2f}s - fetched {len(result['users'])} users")


if __name__ == "__main__":
    # Run examples
    example_beginner()
    example_intermediate()
    example_error_handling()
    
    # Run async example
    asyncio.run(example_async())
