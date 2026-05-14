import Link from "next/link";
import type { ReactNode } from "react";
import {
  formatMoney,
  formatPercent,
  getCashBalances,
  getFakeTrades,
  getHoldings,
  getPortfolios,
  getPortfolioSummary,
  getWatchlist,
} from "@/lib/api";
import { CashBalancesTable } from "@/components/dashboard/CashBalancesTable";
import { EmptyState } from "@/components/dashboard/EmptyState";
import { FakeTradesTable } from "@/components/dashboard/FakeTradesTable";
import { HoldingsTable } from "@/components/dashboard/HoldingsTable";
import { PortfolioSummaryCards } from "@/components/dashboard/PortfolioSummaryCards";
import { Section } from "@/components/dashboard/Section";
import { WatchlistTable } from "@/components/dashboard/WatchlistTable";

export default async function DashboardPage() {
  const result = await loadDashboardData();

  if (result.error) {
    return (
      <PageHeader
        title="Dashboard"
        description="Unable to load data from the API."
      >
        <ErrorState error={result.error} />
      </PageHeader>
    );
  }

  if (!result.data) {
    return (
      <PageHeader
        title="Dashboard"
        description="No portfolios were returned by the API."
      >
        <EmptyState message="Seed demo data or create a portfolio in the API to populate the dashboard." />
      </PageHeader>
    );
  }

  const { portfolio, summary, holdings, cashBalances, watchlist, fakeTrades } =
    result.data;

  return (
    <PageHeader
      title={summary.portfolio_name}
      description="Portfolio snapshot from the FastAPI backend."
    >
      <div className="space-y-8">
        <PortfolioSummaryCards summary={summary} />

        {summary.warnings.length > 0 ? (
          <div className="rounded-md border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
            <div className="font-semibold">Summary Warnings</div>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {summary.warnings.map((warning) => (
                <li key={warning}>{warning}</li>
              ))}
            </ul>
          </div>
        ) : null}

        <Section title="Top Positions">
          {summary.top_positions.length === 0 ? (
            <EmptyState message="No top positions yet." />
          ) : (
            <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {summary.top_positions.map((position) => (
                <div
                  key={position.symbol}
                  className="rounded-md border border-slate-200 bg-white p-4"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="font-semibold text-slate-950">
                        {position.symbol}
                      </div>
                      <div className="text-sm text-slate-500">
                        {position.instrument_type}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-slate-950">
                        {formatMoney(
                          position.estimated_value,
                          summary.base_currency,
                        )}
                      </div>
                      <div className="text-sm text-slate-500">
                        {formatPercent(position.allocation_pct)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Section>

        <Section
          title="Holdings"
          action={
            <Link
              href={`/portfolios/${portfolio.id}`}
              className="text-sm font-medium text-slate-700 hover:text-slate-950"
            >
              View detail
            </Link>
          }
        >
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

        <Section title="Fake Trades">
          <FakeTradesTable fakeTrades={fakeTrades} />
        </Section>
      </div>
    </PageHeader>
  );
}

async function loadDashboardData() {
  try {
    const portfolios = await getPortfolios();
    const portfolio = portfolios[0];

    if (!portfolio) {
      return { data: null, error: null };
    }

    const [summary, holdings, cashBalances, watchlist, fakeTrades] =
      await Promise.all([
        getPortfolioSummary(portfolio.id),
        getHoldings(portfolio.id),
        getCashBalances(portfolio.id),
        getWatchlist(portfolio.id),
        getFakeTrades(portfolio.id),
      ]);

    return {
      data: { portfolio, summary, holdings, cashBalances, watchlist, fakeTrades },
      error: null,
    };
  } catch (error) {
    return { data: null, error };
  }
}

function PageHeader({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-950">{title}</h1>
        <p className="mt-1 text-sm text-slate-600">{description}</p>
      </div>
      {children}
    </div>
  );
}

function ErrorState({ error }: { error: unknown }) {
  return (
    <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-700">
      {error instanceof Error ? error.message : "Unknown API error"}
    </div>
  );
}
