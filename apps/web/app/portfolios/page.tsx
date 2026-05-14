import Link from "next/link";
import { formatDate, getPortfolios } from "@/lib/api";
import { EmptyState } from "@/components/dashboard/EmptyState";

export default async function PortfoliosPage() {
  const result = await getPortfolios()
    .then((portfolios) => ({ portfolios, error: null }))
    .catch((error) => ({ portfolios: null, error }));

  if (result.error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-slate-950">Portfolios</h1>
        <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {result.error instanceof Error
            ? result.error.message
            : "Unable to load portfolios."}
        </div>
      </div>
    );
  }

  const portfolios = result.portfolios ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-950">Portfolios</h1>
        <p className="mt-1 text-sm text-slate-600">
          Portfolios available from the backend API.
        </p>
      </div>

      {portfolios.length === 0 ? (
        <EmptyState message="No portfolios found." />
      ) : (
        <div className="overflow-x-auto rounded-md border border-slate-200 bg-white">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Base Currency</th>
                <th className="px-4 py-3">Created</th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {portfolios.map((portfolio) => (
                <tr key={portfolio.id}>
                  <td className="px-4 py-3 font-medium text-slate-950">
                    {portfolio.name}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {portfolio.base_currency}
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    {formatDate(portfolio.created_at)}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Link
                      href={`/portfolios/${portfolio.id}`}
                      className="font-medium text-slate-700 hover:text-slate-950"
                    >
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
