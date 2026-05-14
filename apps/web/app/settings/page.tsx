import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function SettingsPage() {
  return (
    <PlannedModulePage
      mode="System"
      title="Settings"
      description="A future control panel for app preferences, data source settings, portfolio defaults, and simulator configuration."
      plannedItems={[
        "Base currency defaults",
        "Portfolio preferences",
        "Simulator defaults",
        "Market data settings",
        "Risk rule templates",
        "Environment status",
      ]}
    />
  );
}
