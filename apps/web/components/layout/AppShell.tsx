"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

type NavItem = {
  href: string;
  label: string;
  planned?: boolean;
};

type NavSection = {
  title: string;
  items: NavItem[];
};

const navSections: NavSection[] = [
  {
    title: "Invest",
    items: [
      { href: "/dashboard", label: "Dashboard" },
      { href: "/portfolios", label: "Portfolios" },
      { href: "/fake-trade", label: "Portfolio Impact Simulator" },
      { href: "/risk-check", label: "Risk Check" },
    ],
  },
  {
    title: "Trade",
    items: [
      { href: "/trading", label: "Trading Terminal", planned: true },
      { href: "/trade-history", label: "Trade History", planned: true },
      { href: "/performance", label: "Performance Stats", planned: true },
    ],
  },
  {
    title: "Market",
    items: [
      { href: "/market-conditions", label: "Market Conditions", planned: true },
    ],
  },
  {
    title: "System",
    items: [
      { href: "/agent-logs", label: "Agent Logs", planned: true },
      { href: "/settings", label: "Settings", planned: true },
    ],
  },
];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const mobileItems = navSections.flatMap((section) => section.items);

  return (
    <div className="min-h-screen bg-neutral-100 text-slate-950">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-neutral-800 bg-neutral-950 text-neutral-100 lg:block">
        <div className="border-b border-neutral-800 px-6 py-5">
          <Link href="/dashboard" className="block">
            <span className="text-lg font-semibold">Northstar Invest</span>
            <span className="mt-1 block text-sm text-neutral-400">
              Invest mode online
            </span>
          </Link>
        </div>
        <nav className="space-y-6 px-3 py-5">
          {navSections.map((section) => (
            <div key={section.title}>
              <div className="px-3 text-xs font-semibold uppercase tracking-wide text-neutral-500">
                {section.title}
              </div>
              <div className="mt-2 space-y-1">
                {section.items.map((item) => (
                  <NavLink
                    key={item.href}
                    href={item.href}
                    label={item.label}
                    planned={item.planned}
                    active={isActivePath(pathname, item.href)}
                  />
                ))}
              </div>
            </div>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-neutral-800 bg-neutral-950 px-4 py-3 text-neutral-100 lg:hidden">
          <div className="mb-3 font-semibold">Northstar Invest</div>
          <nav className="flex gap-2 overflow-x-auto">
            {mobileItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="whitespace-nowrap rounded-md border border-neutral-700 px-3 py-2 text-sm font-medium text-neutral-200"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </header>

        <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavLink({
  href,
  label,
  planned,
  active,
}: {
  href: string;
  label: string;
  planned?: boolean;
  active: boolean;
}) {
  return (
    <Link
      href={href}
      className={[
        "flex items-center justify-between gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
        active
          ? "bg-emerald-400 text-neutral-950"
          : "text-neutral-300 hover:bg-neutral-900 hover:text-white",
      ].join(" ")}
    >
      <span>{label}</span>
      {planned ? (
        <span
          className={[
            "rounded border px-1.5 py-0.5 text-[10px] font-semibold uppercase",
            active
              ? "border-neutral-900 text-neutral-900"
              : "border-neutral-700 text-neutral-500",
          ].join(" ")}
        >
          Planned
        </span>
      ) : null}
    </Link>
  );
}

function isActivePath(pathname: string, href: string) {
  return (
    pathname === href ||
    (href !== "/dashboard" && pathname.startsWith(`${href}/`))
  );
}
