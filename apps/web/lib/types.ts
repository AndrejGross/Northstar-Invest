export type Portfolio = {
  id: string;
  name: string;
  description: string | null;
  base_currency: string;
  created_at: string;
  updated_at: string;
};

export type PortfolioListItem = {
  id: string;
  name: string;
  base_currency: string;
  created_at: string;
};

export type Holding = {
  id: string;
  portfolio_id: string;
  symbol: string;
  instrument_type: string;
  quantity: string;
  average_cost: string;
  currency: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type CashBalance = {
  id: string;
  portfolio_id: string;
  currency: string;
  amount: string;
  created_at: string;
  updated_at: string;
};

export type WatchlistItem = {
  id: string;
  portfolio_id: string;
  symbol: string;
  instrument_type: string;
  thesis: string | null;
  status: string;
  created_at: string;
  updated_at: string;
};

export type FakeTrade = {
  id: string;
  portfolio_id: string;
  symbol: string;
  instrument_type: string;
  side: "buy" | "sell" | string;
  quantity: string;
  price: string;
  currency: string;
  estimated_fee: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type PortfolioPositionSummary = {
  symbol: string;
  instrument_type: string;
  quantity: string;
  estimated_value: string;
  allocation_pct: string;
};

export type PortfolioAllocationItem = {
  symbol: string;
  estimated_value: string;
  allocation_pct: string;
};

export type PortfolioSummary = {
  portfolio_id: string;
  portfolio_name: string;
  base_currency: string;
  holdings_value_estimate: string;
  cash_total_estimate: string;
  total_value_estimate: string;
  holdings_count: number;
  cash_balances_count: number;
  top_positions: PortfolioPositionSummary[];
  allocation_by_symbol: PortfolioAllocationItem[];
  warnings: string[];
};

export type PortfolioRule = {
  id: string | null;
  portfolio_id: string;
  max_single_position_pct: string;
  max_stock_position_pct: string;
  max_etf_position_pct: string;
  min_cash_reserve_pct: string;
  concentration_warning_pct: string;
  concentration_danger_pct: string;
  allowed_currencies: string[] | null;
  blocked_symbols: string[] | null;
  created_at: string | null;
  updated_at: string | null;
  is_default: boolean;
};

export type FakeTradePreviewRequest = {
  symbol: string;
  instrument_type: string;
  side: "buy" | "sell";
  quantity: string;
  price: string;
  currency: string;
  estimated_fee: string;
  notes?: string;
};

export type FakeTradePreviewResponse = {
  trade_value: string;
  total_cost_or_proceeds: string;
  before_total_position_value: string;
  after_total_position_value: string;
  before_position_quantity: string;
  after_position_quantity: string;
  before_position_weight_pct: string;
  after_position_weight_pct: string;
  estimated_portfolio_value: string;
  warnings: string[];
  summary: string;
};

export type RiskCheckRequest = {
  symbol: string;
  instrument_type: string;
  side: "buy" | "sell";
  quantity: string;
  price: string;
  currency: string;
  estimated_fee: string;
};

export type RiskMetrics = {
  estimated_total_value: string;
  estimated_cash_after_trade: string;
  after_position_weight_pct: string;
  min_cash_required: string;
  after_cash_pct: string;
};

export type RiskCheckResponse = {
  allowed: boolean;
  risk_level: "low" | "medium" | "high" | "blocked";
  violations: string[];
  warnings: string[];
  metrics: RiskMetrics;
  summary: string;
};
