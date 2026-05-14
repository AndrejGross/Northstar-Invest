def test_get_default_rules_when_no_saved_rule_exists(client, create_portfolio):
    portfolio = create_portfolio()

    response = client.get(f"/api/portfolios/{portfolio['id']}/rules")

    assert response.status_code == 200
    assert response.json()["is_default"] is True
    assert response.json()["max_single_position_pct"] == "25"


def test_update_rules_normalizes_symbols_and_currencies(client, create_portfolio):
    portfolio = create_portfolio()

    response = client.put(
        f"/api/portfolios/{portfolio['id']}/rules",
        json={
            "max_single_position_pct": 30,
            "max_stock_position_pct": 20,
            "max_etf_position_pct": 45,
            "min_cash_reserve_pct": 5,
            "concentration_warning_pct": 20,
            "concentration_danger_pct": 35,
            "allowed_currencies": ["eur", " usd "],
            "blocked_symbols": ["tsla", " TSLA "],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["is_default"] is False
    assert body["allowed_currencies"] == ["EUR", "USD"]
    assert body["blocked_symbols"] == ["TSLA"]
