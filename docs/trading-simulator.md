# Trading Simulator

The Trading Simulator is a future Trade Mode module for practicing simulated trading without broker access or real order execution. It is separate from the Portfolio Impact Simulator, which only previews how a hypothetical buy or sell would affect an investment portfolio.

## Goal

Create a realistic simulated trading environment where the user can practice long and short trades, manage open positions, review PnL, and measure strategy performance over live or replayed market data.

## MVP Scope

- Trading terminal page with chart, order ticket, active positions, and session state.
- Simulated long and short entries.
- Position close flow for partial and full exits.
- Market, limit, stop loss, and take profit simulation rules, if enough price data is available.
- Trade history for entries, exits, fees, slippage assumptions, and notes.
- Basic PnL calculations for realized and unrealized results.
- Performance statistics such as win rate, average win, average loss, profit factor, expectancy, and max drawdown.
- Replay sessions using historical candles before live data is introduced.

## Out of Scope for MVP

- Real broker execution.
- Real money balances.
- Margin account compliance beyond simplified simulator assumptions.
- Options, futures, or leveraged instruments.
- AI-generated trade recommendations.
- Social sharing or public leaderboards.

## User Flows

1. Open Trade Mode and select a symbol.
2. Review the chart, trend context, and recent price action.
3. Enter a simulated long or short position from the order ticket.
4. Attach optional stop loss and take profit levels.
5. Monitor active position PnL as replay or live prices change.
6. Close part or all of the position.
7. Review trade history, notes, and performance statistics.
8. Replay a session to practice a market period again.

## Backend Models Needed Later

- TradingSession: simulator account/session, mode, starting capital, status, and replay window.
- SimulatedPosition: symbol, side, quantity, entry price, current price, stop loss, take profit, opened_at, and closed_at.
- SimulatedOrder: order type, side, symbol, quantity, status, submitted price, filled price, and timestamps.
- SimulatedTradeFill: fills that update positions and realized PnL.
- TradeJournalEntry: notes, tags, setup, mistakes, and screenshots or chart references.
- MarketCandle: OHLCV candle storage or cache for replay.
- PerformanceSnapshot: session-level metrics over time.

## Frontend Pages Needed Later

- `/trading`: trading terminal with chart, order ticket, active positions, and replay controls.
- `/trade-history`: closed simulated trades, filters, and notes.
- `/performance`: profitability and risk statistics.
- `/market-conditions`: market context that can feed Trade Mode decisions.

## Market Data Requirements

The simulator needs reliable candle and quote data. The first version should work with historical candles for replay mode. Future versions can add live quotes, websocket streams, and delayed market data providers.

Required data:

- Symbol metadata.
- OHLCV candles at useful intervals.
- Latest quote or replay cursor price.
- Trading calendar and session status.
- Optional spread and slippage assumptions.

## Long and Short Positions

Long positions profit when price rises above entry. Short positions profit when price falls below entry. The simulator should track side explicitly, calculate position value by side, and prevent closing more than the open quantity.

## PnL Calculations

Unrealized PnL should be calculated from current or replay price. Realized PnL should be calculated when a position is closed. Fees and slippage should be included as simulator assumptions.

Basic formulas:

- Long unrealized PnL: `(current_price - entry_price) * quantity - fees`
- Short unrealized PnL: `(entry_price - current_price) * quantity - fees`
- Realized PnL: same side-aware formula at exit price, minus total fees and slippage

## Stop Loss and Take Profit

The MVP should allow optional stop loss and take profit levels per position. During replay, each candle should be checked to see whether either level would have triggered. If both could trigger inside the same candle, the simulator must use a deterministic rule and clearly document the assumption.

## Trade Statistics

The simulator should calculate:

- Total trades.
- Win rate.
- Average win and average loss.
- Profit factor.
- Expectancy.
- Realized PnL.
- Max drawdown.
- Average holding time.
- Best and worst trade.

## Replay Mode

Replay Mode lets the user practice historical sessions. It should support selecting a symbol, time range, candle interval, playback speed, pause/resume, and step-forward controls. Orders should fill against replay prices, not current live prices.

## Future Live Data Integration

Live data can be added after replay mode is stable. It should remain simulation-only unless a separate broker integration is explicitly designed. Live quotes should update active simulated positions, but must never place real orders.
