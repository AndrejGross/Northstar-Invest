type PlannedModulePageProps = {
  mode: string;
  title: string;
  description: string;
  plannedItems: string[];
};

export function PlannedModulePage({
  mode,
  title,
  description,
  plannedItems,
}: PlannedModulePageProps) {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wide text-emerald-700">
          {mode}
        </div>
        <h1 className="mt-2 text-2xl font-semibold text-slate-950">{title}</h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
          {description}
        </p>
      </div>

      <section className="rounded-md border border-slate-200 bg-white p-6">
        <div className="max-w-2xl">
          <div className="text-sm font-semibold text-slate-950">
            Planned module
          </div>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            This area is intentionally waiting for its backend contracts and
            product flow. The route exists now so the app structure matches the
            long-term workstation design.
          </p>
        </div>

        <div className="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {plannedItems.map((item) => (
            <div
              key={item}
              className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700"
            >
              {item}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
