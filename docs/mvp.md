# Investment Platform MVP

## Goal
Build a broker-agnostic investing platform with a web dashboard for portfolio analysis, fake trades, portfolio-fit reviews, and market trend/regime monitoring.

## MVP Features
1. Portfolio creation
2. Manual holdings and cash
3. Watchlist
4. Stock/ETF portfolio-fit review
5. Fake trade simulator
6. Market trend monitor
7. Market regime monitor
8. Agent logs and explanations
9. Demo mode with seeded data

## Out of Scope
- Real-money execution
- Crypto
- Mobile app
- Advanced ML forecasting
- Social features

## Core Pages
- Dashboard
- Portfolio
- Watchlist
- Review
- Fake Trade Simulator
- Market Conditions
- Agent Logs
- Settings

## Backend Modules
- portfolio-service
- market-data-service
- review-engine
- fake-trade-engine
- trend-monitor
- regime-detector
- regime-validator
- ai-explainer

## Data Models
- User
- Portfolio
- Holding
- CashBalance
- Watchlist
- Symbol
- ETFProfile
- FakeTrade
- AnalysisReport
- AgentDecision
- MarketSignal
- MarketRegimeSnapshot
- PortfolioRule

## Success Criteria
- Portfolio can be created and viewed
- Holdings can be added
- Fake trades can be simulated
- Stock/ETF fit can be reviewed
- Market condition can be displayed
- System explains its reasoning
- App runs locally in demo mode
