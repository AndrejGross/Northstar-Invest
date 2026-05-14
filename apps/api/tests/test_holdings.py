def test_create_list_duplicate_and_delete_holding(client, create_portfolio):
    portfolio = create_portfolio()
    payload = {
        "symbol": "aapl",
        "instrument_type": "stock",
        "quantity": "10",
        "average_cost": "180",
        "currency": "usd",
    }

    created = client.post(
        f"/api/portfolios/{portfolio['id']}/holdings",
        json=payload,
    )
    assert created.status_code == 201
    holding = created.json()
    assert holding["symbol"] == "AAPL"
    assert holding["currency"] == "USD"

    listed = client.get(f"/api/portfolios/{portfolio['id']}/holdings")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    duplicate = client.post(
        f"/api/portfolios/{portfolio['id']}/holdings",
        json=payload,
    )
    assert duplicate.status_code == 409

    deleted = client.delete(f"/api/holdings/{holding['id']}")
    assert deleted.status_code == 204

    listed_after_delete = client.get(f"/api/portfolios/{portfolio['id']}/holdings")
    assert listed_after_delete.json() == []


def test_create_holding_missing_portfolio_returns_404(client):
    response = client.post(
        "/api/portfolios/00000000-0000-0000-0000-000000000000/holdings",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "quantity": "1",
            "average_cost": "100",
            "currency": "EUR",
        },
    )

    assert response.status_code == 404
