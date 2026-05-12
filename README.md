# Northstar Invest

AI-powered trading and portfolio analysis platform with market monitoring, strategy simulation, and a visual control dashboard.

## Overview

Northstar is a full-stack application for building, monitoring, and improving a personal trading and investing system.

The platform combines:

- portfolio analysis
- market trend monitoring
- trade and investment simulations
- asset review and fit evaluation
- strategy experimentation
- visual dashboards and controls

The goal is to create a practical investing workspace where data, analysis, and decision-making are available in one place.

## Core Features

- **Portfolio dashboard**  
  Track positions, allocations, performance, and portfolio composition.

- **Asset review engine**  
  Evaluate whether a stock, ETF, or other asset fits the current portfolio strategy.

- **Market monitoring agents**  
  Watch market trends, momentum, volatility, and broader market conditions.

- **Strategy simulation**  
  Test fake trades, investment ideas, and strategy scenarios without risking capital.

- **Decision support**  
  Generate structured insights based on predefined rules, signals, and portfolio context.

- **Web control panel**  
  Visualize system state, review actions, adjust settings, and inspect analysis output.

## Project Vision

This project is intended to evolve into a modular investing and trading system that can:

- analyze market conditions in near real time
- track investment ideas and simulated trades
- score opportunities against portfolio goals
- provide explainable output instead of black-box decisions
- serve as both an investing assistant and a strategy research environment

## Architecture Goals

The system is being designed around modular components so features can evolve independently.

Planned modules include:

- **Frontend dashboard**
- **Backend API**
- **Market data ingestion**
- **Portfolio analysis engine**
- **Trend and condition monitoring agents**
- **Simulation engine**
- **Strategy/rules engine**
- **Notification and event system**

## Tech Stack

Planned or current stack:

- **Frontend:** React / Next.js or Vite
- **Backend:** Node.js / Python / other service layer
- **Database:** PostgreSQL
- **Market data APIs:** TBD
- **Visualization:** charts, metrics, portfolio views, event streams
- **Deployment:** TBD

> Update this section once the stack is finalized, because future-you will otherwise forget and then pretend this was “part of the plan”.

## Use Cases

- Review whether a stock or ETF fits an existing portfolio
- Simulate recurring investment strategies
- Compare alternative allocations
- Monitor market conditions before entering positions
- Track trends and generate alerts
- Test strategy ideas in a safe environment
- Build a personal investing decision dashboard

## Roadmap

### Phase 1
- [ ] Project setup
- [ ] Base frontend and backend structure
- [ ] Portfolio dashboard skeleton
- [ ] Asset watchlist
- [ ] Manual trade simulation

### Phase 2
- [ ] Market data integration
- [ ] Trend analysis module
- [ ] Portfolio fit scoring
- [ ] Strategy configuration UI
- [ ] Basic alerting

### Phase 3
- [ ] Multi-agent monitoring
- [ ] Real-time market condition evaluation
- [ ] Advanced simulations
- [ ] Explainable decision support
- [ ] Performance analytics

## Local Development

### Prerequisites

- Node.js
- npm or pnpm
- PostgreSQL
- API keys for market data providers

### Installation

```bash
git clone https://github.com/your-username/northstar.git
cd northstar
npm install
