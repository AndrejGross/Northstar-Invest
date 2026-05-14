import { formatDate, formatMoney, formatNumber } from "@/lib/api";
import type { FakeTrade } from "@/lib/types";
import { EmptyState } from "./EmptyState";

export function FakeTradesTable({ fakeTrades }: { fakeTrades: FakeTrade[] }) {
  if (fakeTrades.length === 0) {
    return <EmptyState message="No saved impact simulations yet." />;
  }

  return (
    <div className="overflow-x-auto rounded-md border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">Created</th>
            <th className="px-4 py-3">Side</th>
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3 text-right">Quantity</th>
            <th className="px-4 py-3 text-right">Price</th>
            <th className="px-4 py-3 text-right">Fee</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {fakeTrades.map((trade) => (
            <tr key={trade.id}>
              <td className="px-4 py-3 text-slate-600">
                {formatDate(trade.created_at)}
              </td>
              <td className="px-4 py-3 font-medium text-slate-950">
                {trade.side}
              </td>
              <td className="px-4 py-3 text-slate-700">{trade.symbol}</td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatNumber(trade.quantity)}
              </td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatMoney(trade.price, trade.currency)}
              </td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatMoney(trade.estimated_fee, trade.currency)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
