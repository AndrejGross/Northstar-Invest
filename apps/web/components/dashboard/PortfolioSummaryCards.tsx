import { formatMoney } from "@/lib/api";
import type { PortfolioSummary } from "@/lib/types";

export function PortfolioSummaryCards({
  summary,
}: {
  summary: PortfolioSummary;
}) {
  const cards = [
    {
      label: "Total Value",
      value: formatMoney(summary.total_value_estimate, summary.base_currency),
    },
    {
      label: "Holdings",
      value: formatMoney(summary.holdings_value_estimate, summary.base_currency),
    },
    {
      label: "Cash",
      value: formatMoney(summary.cash_total_estimate, summary.base_currency),
    },
    {
      label: "Positions",
      value: summary.holdings_count.toString(),
    },
    {
      label: "Cash Balances",
      value: summary.cash_balances_count.toString(),
    },
  ];

  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
      {cards.map((card) => (
        <div
          key={card.label}
          className="rounded-md border border-slate-200 bg-white p-4"
        >
          <div className="text-xs font-medium uppercase text-slate-500">
            {card.label}
          </div>
          <div className="mt-2 text-2xl font-semibold text-slate-950">
            {card.value}
          </div>
        </div>
      ))}
    </div>
  );
}
