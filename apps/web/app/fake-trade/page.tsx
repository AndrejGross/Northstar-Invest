import { FakeTradePreviewForm } from "@/components/forms/FakeTradePreviewForm";
import { getPortfolios } from "@/lib/api";

export default async function FakeTradePage() {
  const result = await getPortfolios()
    .then((portfolios) => ({ portfolios, error: null }))
    .catch((error) => ({ portfolios: null, error }));

  if (result.error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-slate-950">
          Portfolio Impact Simulator
        </h1>
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
        <h1 className="text-2xl font-semibold text-slate-950">
          Portfolio Impact Simulator
        </h1>
        <p className="mt-1 text-sm text-slate-600">
          Preview how a buy or sell would affect portfolio weights without
          mutating actual holdings.
        </p>
      </div>
      {portfolios.length === 0 ? (
        <div className="rounded-md border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-500">
          No portfolios found. Seed demo data first.
        </div>
      ) : (
        <FakeTradePreviewForm portfolios={portfolios} />
      )}
    </div>
  );
}
