def test_get_health_returns_200_and_ok(client):
    """GET /health devuelve 200 y cuerpo {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
