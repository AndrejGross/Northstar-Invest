def test_preview_buy_does_not_mutate_holdings(
    client,
    create_portfolio,
    add_cash_balance,
    add_holding,
):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")
    holding = add_holding(portfolio["id"], quantity="10", average_cost="100")

    preview = client.post(
        f"/api/portfolios/{portfolio['id']}/fake-trades/preview",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "2",
            "price": "110",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )
    assert preview.status_code == 200
    assert preview.json()["after_position_quantity"] == "12.00000000"

    fetched_holding = client.get(f"/api/holdings/{holding['id']}")
    assert fetched_holding.json()["quantity"] == "10.00000000"


def test_preview_sell_validates_existing_holding(client, create_portfolio, add_holding):
    portfolio = create_portfolio()
    add_holding(portfolio["id"], quantity="10")

    preview = client.post(
        f"/api/portfolios/{portfolio['id']}/fake-trades/preview",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "sell",
            "quantity": "3",
            "price": "115",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert preview.status_code == 200
    assert preview.json()["after_position_quantity"] == "7.00000000"


def test_sell_more_than_holding_quantity_returns_validation_error(
    client,
    create_portfolio,
    add_holding,
):
    portfolio = create_portfolio()
    add_holding(portfolio["id"], quantity="10")

    response = client.post(
        f"/api/portfolios/{portfolio['id']}/fake-trades/preview",
        json={
            "symbol": "VWCE",
            "instrument_type": "etf",
            "side": "sell",
            "quantity": "11",
            "price": "115",
            "currency": "EUR",
            "estimated_fee": "1",
        },
    )

    assert response.status_code == 422


def test_save_and_list_fake_trade(client, create_portfolio, add_cash_balance):
    portfolio = create_portfolio()
    add_cash_balance(portfolio["id"], amount="10000")

    saved = client.post(
        f"/api/portfolios/{portfolio['id']}/fake-trades",
        json={
            "symbol": "SPY",
            "instrument_type": "etf",
            "side": "buy",
            "quantity": "1",
            "price": "500",
            "currency": "EUR",
            "estimated_fee": "2",
        },
    )
    assert saved.status_code == 201

    listed = client.get(f"/api/portfolios/{portfolio['id']}/fake-trades")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
