def _set_rules(client, portfolio_id, **overrides):
    payload = {
        "max_single_position_pct": 25,
        "max_stock_position_pct": 20,
        "max_etf_position_pct": 40,
        "min_cash_reserve_pct": 5,
        "concentration_warning_pct": 20,
        "concentration_danger_pct": 35,
        "allowed_currencies": ["EUR", "USD"],
        "blocked_symbols": ["TSLA"],
    }
    payload.update(overrides)
    response = client.put(f"/api/portfolios/{portfolio_id}/rules", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def test_blocked_symbol_blocks_trade(client, create_portfolio, add_cash_balance):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")
    _set_rules(client, portfolio["id"])

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/risk-check",
        json={
            "symbol": "tsla",
            "instrument_type": "stock",
            "side": "buy",
            "quantity": "1",
            "price": "200",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.status_code == 200
    assert response.json()["allowed"] is False
    assert response.json()["risk_level"] == "blocked"


def test_insufficient_cash_blocks_buy(client, create_portfolio, add_cash_balance):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="100")
    _set_rules(client, portfolio["id"], blocked_symbols=[])

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/risk-check",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "2",
            "price": "100",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.json()["allowed"] is False
    assert any("Insufficient EUR cash" in item for item in response.json()["violations"])


def test_concentration_warning_is_returned(
    client,
    create_portfolio,
    add_cash_balance,
    add_holding,
):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")
    add_holding(portfolio["id"], symbol="VWCE", instrument_type="etf", quantity="10")
    _set_rules(
        client,
        portfolio["id"],
        max_single_position_pct=80,
        max_etf_position_pct=80,
        concentration_warning_pct=10,
        concentration_danger_pct=70,
        blocked_symbols=[],
    )

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/risk-check",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "1",
            "price": "100",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.json()["allowed"] is True
    assert response.json()["risk_level"] == "medium"
    assert response.json()["warnings"]


def test_concentration_danger_blocks_trade(
    client,
    create_portfolio,
    add_cash_balance,
    add_holding,
):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")
    add_holding(portfolio["id"], symbol="VWCE", instrument_type="etf", quantity="10")
    _set_rules(
        client,
        portfolio["id"],
        max_single_position_pct=100,
        max_etf_position_pct=100,
        concentration_warning_pct=10,
        concentration_danger_pct=15,
        blocked_symbols=[],
    )

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/risk-check",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "10",
            "price": "100",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.json()["allowed"] is False
    assert response.json()["risk_level"] == "blocked"


def test_valid_small_buy_returns_allowed(client, create_portfolio, add_cash_balance):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")
    _set_rules(client, portfolio["id"], blocked_symbols=[])

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/risk-check",
        json={
            "symbol": "SPY",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "1",
            "price": "100",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.status_code == 200
    assert response.json()["allowed"] is True
    assert response.json()["risk_level"] in {"low", "medium"}
