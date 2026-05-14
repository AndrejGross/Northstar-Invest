import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function TradeHistoryPage() {
  return (
    <PlannedModulePage
      mode="Trade Mode"
      title="Trade History"
      description="A future ledger for simulated entries, exits, fees, realized PnL, notes, and session review."
      plannedItems={[
        "Closed simulated trades",
        "Entry and exit prices",
        "Realized PnL",
        "Fees and slippage",
        "Trade notes",
        "Session filters",
      ]}
    />
  );
}
