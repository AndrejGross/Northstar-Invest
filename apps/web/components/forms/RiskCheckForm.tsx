"use client";

import { useState } from "react";
import { formatMoney, formatPercent, runRiskCheck } from "@/lib/api";
import type {
  PortfolioListItem,
  RiskCheckRequest,
  RiskCheckResponse,
} from "@/lib/types";

const initialForm: RiskCheckRequest = {
  symbol: "VWCE",
  instrument_type: "etf",
  side: "buy",
  quantity: "1",
  price: "100",
  currency: "EUR",
  estimated_fee: "0",
};

export function RiskCheckForm({
  portfolios,
}: {
  portfolios: PortfolioListItem[];
}) {
  const [portfolioId, setPortfolioId] = useState(portfolios[0]?.id ?? "");
  const [form, setForm] = useState<RiskCheckRequest>(initialForm);
  const [result, setResult] = useState<RiskCheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await runRiskCheck(portfolioId, form);
      setResult(response);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to run risk check.",
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
          {isSubmitting ? "Checking..." : "Run Risk Check"}
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
  result: RiskCheckResponse | null;
  currency: string;
}) {
  if (!result) {
    return (
      <div className="rounded-md border border-dashed border-slate-300 bg-white p-5 text-sm text-slate-500">
        Submit a proposed trade to see deterministic risk output.
      </div>
    );
  }

  const metrics = [
    ["Estimated Total Value", formatMoney(result.metrics.estimated_total_value, currency)],
    ["Cash After Trade", formatMoney(result.metrics.estimated_cash_after_trade, currency)],
    ["Min Cash Required", formatMoney(result.metrics.min_cash_required, currency)],
    ["After Position Weight", formatPercent(result.metrics.after_position_weight_pct)],
    ["After Cash Percent", formatPercent(result.metrics.after_cash_pct)],
  ];

  return (
    <div className="space-y-4 rounded-md border border-slate-200 bg-white p-5">
      <div>
        <div className="flex items-center gap-2">
          <span
            className={`rounded-md px-2 py-1 text-xs font-semibold ${
              result.allowed
                ? "bg-emerald-100 text-emerald-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {result.allowed ? "Allowed" : "Blocked"}
          </span>
          <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">
            {result.risk_level}
          </span>
        </div>
        <p className="mt-3 text-sm text-slate-600">{result.summary}</p>
      </div>
      <dl className="divide-y divide-slate-100 text-sm">
        {metrics.map(([label, value]) => (
          <div key={label} className="flex justify-between gap-4 py-2">
            <dt className="text-slate-500">{label}</dt>
            <dd className="font-medium text-slate-950">{value}</dd>
          </div>
        ))}
      </dl>
      <MessageList title="Violations" items={result.violations} tone="red" />
      <MessageList title="Warnings" items={result.warnings} tone="amber" />
    </div>
  );
}

function MessageList({
  title,
  items,
  tone,
}: {
  title: string;
  items: string[];
  tone: "amber" | "red";
}) {
  if (items.length === 0) {
    return null;
  }

  const classes =
    tone === "red"
      ? "border-red-200 bg-red-50 text-red-800"
      : "border-amber-200 bg-amber-50 text-amber-800";

  return (
    <div className={`rounded-md border p-3 ${classes}`}>
      <div className="text-sm font-semibold">{title}</div>
      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
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
