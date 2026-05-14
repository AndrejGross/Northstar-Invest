def test_create_update_list_duplicate_and_delete_cash_balance(client, create_portfolio):
    portfolio = create_portfolio()

    created = client.post(
        f"/api/portfolios/{portfolio['id']}/cash-balances",
        json={"currency": "eur", "amount": "1500"},
    )
    assert created.status_code == 201
    cash_balance = created.json()
    assert cash_balance["currency"] == "EUR"

    duplicate = client.post(
        f"/api/portfolios/{portfolio['id']}/cash-balances",
        json={"currency": "EUR", "amount": "500"},
    )
    assert duplicate.status_code == 409

    updated = client.patch(
        f"/api/cash-balances/{cash_balance['id']}",
        json={"amount": "1750.25"},
    )
    assert updated.status_code == 200
    assert updated.json()["amount"] == "1750.25000000"

    listed = client.get(f"/api/portfolios/{portfolio['id']}/cash-balances")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    deleted = client.delete(f"/api/cash-balances/{cash_balance['id']}")
    assert deleted.status_code == 204
