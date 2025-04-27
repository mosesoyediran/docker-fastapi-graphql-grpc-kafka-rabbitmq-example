def test_hello_query(client):
    """
    Test the hello query returns correct greeting.
    """
    query = """
    query {
      hello
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["hello"] == "Hello from Strawberry resolver!"

def test_create_user_mutation(client):
    """
    Test creating a new user with mutation.
    """
    mutation = """
    mutation {
      createUser(name: "Moses") {
        ok
        userId
        message
      }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    data = response.json()["data"]["createUser"]
    assert response.status_code == 200
    assert data["ok"] is True
    assert data["userId"] is not None
    assert "created successfully" in data["message"]

def test_get_users_query(client):
    """
    Test getting users query.
    """
    query = """
    query {
      getUsers {
        id
        name
      }
    }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["getUsers"]
    assert response.status_code == 200
    assert isinstance(data, list)
    # You can add deeper checks later like: assert any(u["name"] == "Moses" for u in data)
