import { formatMoney } from "@/lib/api";
import type { CashBalance } from "@/lib/types";
import { EmptyState } from "./EmptyState";

export function CashBalancesTable({
  cashBalances,
}: {
  cashBalances: CashBalance[];
}) {
  if (cashBalances.length === 0) {
    return <EmptyState message="No cash balances yet." />;
  }

  return (
    <div className="overflow-x-auto rounded-md border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">Currency</th>
            <th className="px-4 py-3 text-right">Amount</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {cashBalances.map((balance) => (
            <tr key={balance.id}>
              <td className="px-4 py-3 font-medium text-slate-950">
                {balance.currency}
              </td>
              <td className="px-4 py-3 text-right text-slate-700">
                {formatMoney(balance.amount, balance.currency)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
