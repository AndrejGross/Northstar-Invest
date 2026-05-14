import type { WatchlistItem } from "@/lib/types";
import { EmptyState } from "./EmptyState";

export function WatchlistTable({ watchlist }: { watchlist: WatchlistItem[] }) {
  if (watchlist.length === 0) {
    return <EmptyState message="No watchlist items yet." />;
  }

  return (
    <div className="overflow-x-auto rounded-md border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Thesis</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {watchlist.map((item) => (
            <tr key={item.id}>
              <td className="px-4 py-3 font-medium text-slate-950">
                {item.symbol}
              </td>
              <td className="px-4 py-3 text-slate-600">
                {item.instrument_type}
              </td>
              <td className="px-4 py-3 text-slate-700">{item.status}</td>
              <td className="px-4 py-3 text-slate-600">{item.thesis ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
