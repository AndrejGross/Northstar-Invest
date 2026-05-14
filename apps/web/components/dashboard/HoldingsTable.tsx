import { formatMoney, formatNumber } from "@/lib/api";
import type { Holding } from "@/lib/types";
import { EmptyState } from "./EmptyState";

export function HoldingsTable({ holdings }: { holdings: Holding[] }) {
  if (holdings.length === 0) {
    return <EmptyState message="No holdings yet." />;
  }

  return (
    <div className="overflow-x-auto rounded-md border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3 text-right">Quantity</th>
            <th className="px-4 py-3 text-right">Avg Cost</th>
            <th className="px-4 py-3">Currency</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {holdings.map((holding) => (
            <tr key={holding.id}>
              <td className="px-4 py-3 font-medium text-slate-950">
                {holding.symbol}
              </td>
              <td className="px-4 py-3 text-slate-600">
                {holding.instrument_type}
              </td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatNumber(holding.quantity)}
              </td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatMoney(holding.average_cost, holding.currency)}
              </td>
              <td className="px-4 py-3 text-slate-600">{holding.currency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
