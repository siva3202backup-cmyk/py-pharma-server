from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_openapi_available():
    response=client.get('/openapi.json'); assert response.status_code==200
    paths=response.json()['paths']
    for path in ['/api/auth/login','/api/products','/api/cart','/api/orders','/api/admin/dashboard']: assert path in paths
