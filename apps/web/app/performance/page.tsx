import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function PerformancePage() {
  return (
    <PlannedModulePage
      mode="Trade Mode"
      title="Performance Stats"
      description="A future analytics page for profitability, drawdowns, win rate, expectancy, and strategy review across simulated trades."
      plannedItems={[
        "Win rate",
        "Average win and loss",
        "Expectancy",
        "Max drawdown",
        "Profit factor",
        "Strategy tags",
      ]}
    />
  );
}
