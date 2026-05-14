# Northstar Invest Product Structure

Northstar Invest is organized as a workstation with four product areas: Invest Mode, Trade Mode, Market Mode, and System. This keeps long-term portfolio analysis separate from future trading simulation, market context, and operational settings.

## Invest Mode

Invest Mode is the current product center. It focuses on long-term portfolio construction, allocation review, risk rules, and safe scenario planning.

Included modules:

- Dashboard: portfolio-level summary, holdings estimates, cash balances, watchlist, warnings, and saved impact simulations.
- Portfolios: portfolio records, detail views, holdings, cash balances, watchlists, and rules.
- Watchlist: symbols tracked for portfolio research and future consideration.
- Portfolio Review: deterministic review of allocations, cash, concentration, and rule compliance.
- Portfolio Impact Simulator: buy or sell scenario preview for an existing portfolio. It does not place trades and does not mutate real holdings.
- Risk Rules: configurable constraints such as max position size, cash reserve, allowed currencies, and blocked symbols.

## Trade Mode

Trade Mode is planned as a separate trading simulator. It is not the same thing as the Portfolio Impact Simulator.

Future modules:

- Trading Terminal: main simulated trading workspace.
- Chart: price chart with indicators and replay controls.
- Order Ticket: simulated long and short entry controls.
- Active Positions: open simulated positions with PnL, stop loss, and take profit.
- Trade History: closed simulated trades and review notes.
- Performance Stats: profitability, drawdown, win rate, expectancy, and strategy metrics.
- Replay Sessions: practice sessions using historical or replayed price data.

## Market Mode

Market Mode is planned as the market context layer. It should help the user understand trend, regime, and symbol opportunity before making investment or simulation decisions.

Future modules:

- Market Conditions: broad market state and risk environment.
- Trend Monitor: trend status for watchlists and selected symbols.
- Regime Detector: market regime classification for future decision support.
- Symbol Explorer: symbol discovery, details, and watchlist promotion.

## System

System contains operational views and preferences for transparency and control.

Included or planned modules:

- Agent Logs: future history of automated reviews, analysis runs, errors, and background jobs.
- Settings: app preferences, portfolio defaults, market data settings, and simulator defaults.

## Naming Decision

The existing backend fake-trade endpoints currently power the Portfolio Impact Simulator. The UI should use the Portfolio Impact Simulator name because the feature previews portfolio impact only. A future Trading Simulator should have its own domain model, routes, pages, and metrics.
