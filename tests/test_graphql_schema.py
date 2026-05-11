import asyncio
from graphql_apis import schema as graphql_schema


def test_posts_query_returns_data():
    query = """
    query {
      posts(limit: 5) {
        id
        title
        author
      }
    }
    """
    result = asyncio.run(graphql_schema.schema.execute(query))
    assert result.errors is None
    assert result.data is not None
    assert "posts" in result.data
    assert isinstance(result.data["posts"], list)


def test_create_post_mutation():
    mutation = """
    mutation {
      createPost(
        title: \"Test Post\"
        content: \"This is a GraphQL test post content.\"
        author: \"TestUser\"
      ) {
        id
        title
        author
      }
    }
    """
    result = asyncio.run(graphql_schema.schema.execute(mutation))
    assert result.errors is None
    assert result.data is not None
    assert result.data["createPost"]["title"] == "Test Post"
    assert result.data["createPost"]["author"] == "TestUser"
