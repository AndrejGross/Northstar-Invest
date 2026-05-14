import { PlannedModulePage } from "@/components/layout/PlannedModulePage";

export default function AgentLogsPage() {
  return (
    <PlannedModulePage
      mode="System"
      title="Agent Logs"
      description="A future system view for background analysis runs, portfolio review history, and automation transparency."
      plannedItems={[
        "Analysis run history",
        "Risk review logs",
        "Data refresh events",
        "Automation status",
        "Error visibility",
        "Audit trail",
      ]}
    />
  );
}
