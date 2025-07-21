from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/patients/")
    assert response.status_code in (200, 404)
    assert isinstance(response.json(), list)
