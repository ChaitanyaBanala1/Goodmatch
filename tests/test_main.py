from fastapi.testclient import TestClient
from main import app  # Ensure this points to your FastAPI app instance

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Goodmatch API!"}
