import {
  formatPercent,
  getCashBalances,
  getFakeTrades,
  getHoldings,
  getPortfolio,
  getPortfolioRules,
  getPortfolioSummary,
  getWatchlist,
} from "@/lib/api";
import { CashBalancesTable } from "@/components/dashboard/CashBalancesTable";
import { FakeTradesTable } from "@/components/dashboard/FakeTradesTable";
import { HoldingsTable } from "@/components/dashboard/HoldingsTable";
import { PortfolioSummaryCards } from "@/components/dashboard/PortfolioSummaryCards";
import { Section } from "@/components/dashboard/Section";
import { WatchlistTable } from "@/components/dashboard/WatchlistTable";

export default async function PortfolioDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const result = await loadPortfolioDetail(id);

  if (result.error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-slate-950">
          Portfolio Detail
        </h1>
        <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {result.error instanceof Error
            ? result.error.message
            : "Unable to load portfolio."}
        </div>
      </div>
    );
  }

  if (!result.data) {
    return null;
  }

  const {
    portfolio,
    summary,
    holdings,
    cashBalances,
    watchlist,
    fakeTrades,
    rules,
  } = result.data;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold text-slate-950">
          {portfolio.name}
        </h1>
        <p className="mt-1 text-sm text-slate-600">
          Base currency: {portfolio.base_currency}
        </p>
      </div>

      <PortfolioSummaryCards summary={summary} />

      <Section title="Portfolio Rules">
        <div className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 text-sm md:grid-cols-3">
          <RuleMetric
            label="Max Single Position"
            value={formatPercent(rules.max_single_position_pct)}
          />
          <RuleMetric
            label="Max Stock Position"
            value={formatPercent(rules.max_stock_position_pct)}
          />
          <RuleMetric
            label="Max ETF Position"
            value={formatPercent(rules.max_etf_position_pct)}
          />
          <RuleMetric
            label="Min Cash Reserve"
            value={formatPercent(rules.min_cash_reserve_pct)}
          />
          <RuleMetric
            label="Allowed Currencies"
            value={rules.allowed_currencies?.join(", ") ?? "Any"}
          />
          <RuleMetric
            label="Blocked Symbols"
            value={rules.blocked_symbols?.join(", ") ?? "None"}
          />
        </div>
      </Section>

      <Section title="Holdings">
        <HoldingsTable holdings={holdings} />
      </Section>

      <div className="grid gap-8 xl:grid-cols-2">
        <Section title="Cash Balances">
          <CashBalancesTable cashBalances={cashBalances} />
        </Section>
        <Section title="Watchlist">
          <WatchlistTable watchlist={watchlist} />
        </Section>
      </div>

      <Section title="Saved Impact Simulations">
        <FakeTradesTable fakeTrades={fakeTrades} />
      </Section>
    </div>
  );
}

async function loadPortfolioDetail(id: string) {
  try {
    const [
      portfolio,
      summary,
      holdings,
      cashBalances,
      watchlist,
      fakeTrades,
      rules,
    ] = await Promise.all([
      getPortfolio(id),
      getPortfolioSummary(id),
      getHoldings(id),
      getCashBalances(id),
      getWatchlist(id),
      getFakeTrades(id),
      getPortfolioRules(id),
    ]);

    return {
      data: {
        portfolio,
        summary,
        holdings,
        cashBalances,
        watchlist,
        fakeTrades,
        rules,
      },
      error: null,
    };
  } catch (error) {
    return { data: null, error };
  }
}

function RuleMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs font-medium uppercase text-slate-500">{label}</div>
      <div className="mt-1 font-semibold text-slate-950">{value}</div>
    </div>
  );
}
