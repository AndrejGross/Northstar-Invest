"use client";

import { useState } from "react";
import {
  formatMoney,
  formatNumber,
  formatPercent,
  previewFakeTrade,
} from "@/lib/api";
import type {
  FakeTradePreviewRequest,
  FakeTradePreviewResponse,
  PortfolioListItem,
} from "@/lib/types";

const initialForm: FakeTradePreviewRequest = {
  symbol: "VWCE",
  instrument_type: "etf",
  side: "buy",
  quantity: "1",
  price: "100",
  currency: "EUR",
  estimated_fee: "0",
  notes: "",
};

export function FakeTradePreviewForm({
  portfolios,
}: {
  portfolios: PortfolioListItem[];
}) {
  const [portfolioId, setPortfolioId] = useState(portfolios[0]?.id ?? "");
  const [form, setForm] = useState<FakeTradePreviewRequest>(initialForm);
  const [result, setResult] = useState<FakeTradePreviewResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await previewFakeTrade(portfolioId, form);
      setResult(response);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to preview fake trade.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(320px,420px)]">
      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-md border border-slate-200 bg-white p-5"
      >
        <FormSelect
          label="Portfolio"
          value={portfolioId}
          onChange={setPortfolioId}
          options={portfolios.map((portfolio) => ({
            label: portfolio.name,
            value: portfolio.id,
          }))}
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Symbol"
            value={form.symbol}
            onChange={(value) => setForm({ ...form, symbol: value })}
          />
          <FormSelect
            label="Instrument Type"
            value={form.instrument_type}
            onChange={(value) => setForm({ ...form, instrument_type: value })}
            options={[
              { label: "ETF", value: "etf" },
              { label: "Stock", value: "stock" },
            ]}
          />
          <FormSelect
            label="Side"
            value={form.side}
            onChange={(value) =>
              setForm({ ...form, side: value as "buy" | "sell" })
            }
            options={[
              { label: "Buy", value: "buy" },
              { label: "Sell", value: "sell" },
            ]}
          />
          <FormInput
            label="Quantity"
            type="number"
            value={form.quantity}
            onChange={(value) => setForm({ ...form, quantity: value })}
          />
          <FormInput
            label="Price"
            type="number"
            value={form.price}
            onChange={(value) => setForm({ ...form, price: value })}
          />
          <FormInput
            label="Currency"
            value={form.currency}
            onChange={(value) => setForm({ ...form, currency: value })}
          />
          <FormInput
            label="Estimated Fee"
            type="number"
            value={form.estimated_fee}
            onChange={(value) => setForm({ ...form, estimated_fee: value })}
          />
          <FormInput
            label="Notes"
            value={form.notes ?? ""}
            onChange={(value) => setForm({ ...form, notes: value })}
          />
        </div>
        {error ? (
          <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}
        <button
          type="submit"
          disabled={!portfolioId || isSubmitting}
          className="rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isSubmitting ? "Previewing..." : "Preview Fake Trade"}
        </button>
      </form>

      <ResultPanel result={result} currency={form.currency} />
    </div>
  );
}

function ResultPanel({
  result,
  currency,
}: {
  result: FakeTradePreviewResponse | null;
  currency: string;
}) {
  if (!result) {
    return (
      <div className="rounded-md border border-dashed border-slate-300 bg-white p-5 text-sm text-slate-500">
        Submit a fake trade to see the simulated impact.
      </div>
    );
  }

  const rows = [
    ["Trade Value", formatMoney(result.trade_value, currency)],
    ["Total Cost / Proceeds", formatMoney(result.total_cost_or_proceeds, currency)],
    ["Before Quantity", formatNumber(result.before_position_quantity)],
    ["After Quantity", formatNumber(result.after_position_quantity)],
    ["Before Weight", formatPercent(result.before_position_weight_pct)],
    ["After Weight", formatPercent(result.after_position_weight_pct)],
  ];

  return (
    <div className="space-y-4 rounded-md border border-slate-200 bg-white p-5">
      <div>
        <h2 className="text-base font-semibold text-slate-950">Preview Result</h2>
        <p className="mt-1 text-sm text-slate-600">{result.summary}</p>
      </div>
      <dl className="divide-y divide-slate-100 text-sm">
        {rows.map(([label, value]) => (
          <div key={label} className="flex justify-between gap-4 py-2">
            <dt className="text-slate-500">{label}</dt>
            <dd className="font-medium text-slate-950">{value}</dd>
          </div>
        ))}
      </dl>
      {result.warnings.length > 0 ? (
        <div className="rounded-md border border-amber-200 bg-amber-50 p-3">
          <div className="text-sm font-semibold text-amber-900">Warnings</div>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-800">
            {result.warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}

function FormInput({
  label,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}) {
  return (
    <label className="block text-sm">
      <span className="font-medium text-slate-700">{label}</span>
      <input
        type={type}
        value={value}
        min={type === "number" ? "0" : undefined}
        step={type === "number" ? "0.01" : undefined}
        onChange={(event) => onChange(event.target.value)}
        className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-950 outline-none focus:border-slate-500"
      />
    </label>
  );
}

function FormSelect({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { label: string; value: string }[];
}) {
  return (
    <label className="block text-sm">
      <span className="font-medium text-slate-700">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-950 outline-none focus:border-slate-500"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}
