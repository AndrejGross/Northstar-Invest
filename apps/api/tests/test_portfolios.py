def test_create_list_and_get_portfolio(client):
    created = client.post(
        "/api/portfolios",
        json={"name": "Core Portfolio", "base_currency": "EUR"},
    )
    assert created.status_code == 201
    portfolio = created.json()

    listed = client.get("/api/portfolios")
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == portfolio["id"]

    fetched = client.get(f"/api/portfolios/{portfolio['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Core Portfolio"


def test_get_missing_portfolio_returns_404(client):
    response = client.get("/api/portfolios/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
