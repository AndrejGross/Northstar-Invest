import { RiskCheckForm } from "@/components/forms/RiskCheckForm";
import { getPortfolios } from "@/lib/api";

export default async function RiskCheckPage() {
  const result = await getPortfolios()
    .then((portfolios) => ({ portfolios, error: null }))
    .catch((error) => ({ portfolios: null, error }));

  if (result.error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-slate-950">Risk Check</h1>
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
        <h1 className="text-2xl font-semibold text-slate-950">Risk Check</h1>
        <p className="mt-1 text-sm text-slate-600">
          Evaluate a proposed trade against deterministic portfolio rules.
        </p>
      </div>
      {portfolios.length === 0 ? (
        <div className="rounded-md border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
          No portfolios found. Seed demo data first.
        </div>
      ) : (
        <RiskCheckForm portfolios={portfolios} />
      )}
    </div>
  );
}
