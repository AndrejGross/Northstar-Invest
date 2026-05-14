import type {
  CashBalance,
  FakeTrade,
  FakeTradePreviewRequest,
  FakeTradePreviewResponse,
  Holding,
  Portfolio,
  PortfolioListItem,
  PortfolioRule,
  PortfolioSummary,
  RiskCheckRequest,
  RiskCheckResponse,
  WatchlistItem,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init.headers,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(response.status, errorText || response.statusText);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function getPortfolios(): Promise<PortfolioListItem[]> {
  return apiFetch<PortfolioListItem[]>("/api/portfolios");
}

export function getPortfolio(portfolioId: string): Promise<Portfolio> {
  return apiFetch<Portfolio>(`/api/portfolios/${portfolioId}`);
}

export function getPortfolioSummary(
  portfolioId: string,
): Promise<PortfolioSummary> {
  return apiFetch<PortfolioSummary>(`/api/portfolios/${portfolioId}/summary`);
}

export function getHoldings(portfolioId: string): Promise<Holding[]> {
  return apiFetch<Holding[]>(`/api/portfolios/${portfolioId}/holdings`);
}

export function getCashBalances(portfolioId: string): Promise<CashBalance[]> {
  return apiFetch<CashBalance[]>(
    `/api/portfolios/${portfolioId}/cash-balances`,
  );
}

export function getWatchlist(portfolioId: string): Promise<WatchlistItem[]> {
  return apiFetch<WatchlistItem[]>(`/api/portfolios/${portfolioId}/watchlist`);
}

export function getFakeTrades(portfolioId: string): Promise<FakeTrade[]> {
  return apiFetch<FakeTrade[]>(`/api/portfolios/${portfolioId}/fake-trades`);
}

export function previewFakeTrade(
  portfolioId: string,
  payload: FakeTradePreviewRequest,
): Promise<FakeTradePreviewResponse> {
  return apiFetch<FakeTradePreviewResponse>(
    `/api/portfolios/${portfolioId}/fake-trades/preview`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export function runRiskCheck(
  portfolioId: string,
  payload: RiskCheckRequest,
): Promise<RiskCheckResponse> {
  return apiFetch<RiskCheckResponse>(
    `/api/portfolios/${portfolioId}/risk-check`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export function getPortfolioRules(portfolioId: string): Promise<PortfolioRule> {
  return apiFetch<PortfolioRule>(`/api/portfolios/${portfolioId}/rules`);
}

export function formatMoney(value: string | number, currency = "EUR"): string {
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return `${value} ${currency}`;
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(numericValue);
}

export function formatNumber(value: string | number): string {
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return String(value);
  }

  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 4,
  }).format(numericValue);
}

export function formatPercent(value: string | number): string {
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return `${value}%`;
  }

  return `${numericValue.toFixed(2)}%`;
}

export function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}
