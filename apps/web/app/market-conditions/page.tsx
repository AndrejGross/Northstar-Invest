import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function MarketConditionsPage() {
  return (
    <PlannedModulePage
      mode="Market Mode"
      title="Market Conditions"
      description="A future market context layer for trend state, regime detection, symbol discovery, and watchlist-level signals."
      plannedItems={[
        "Trend monitor",
        "Market regime detector",
        "Symbol explorer",
        "Watchlist signal overview",
        "Volatility context",
        "Market breadth notes",
      ]}
    />
  );
}
