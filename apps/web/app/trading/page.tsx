import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function TradingPage() {
  return (
    <PlannedModulePage
      mode="Trade Mode"
      title="Trading Terminal"
      description="A future simulator workspace for charts, order tickets, long and short simulated positions, and replay-driven practice."
      plannedItems={[
        "Interactive chart",
        "Order ticket",
        "Active simulated positions",
        "Stop loss and take profit controls",
        "Replay session controls",
        "PnL panel",
      ]}
    />
  );
}
