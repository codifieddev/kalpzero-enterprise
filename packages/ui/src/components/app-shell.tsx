import type { PropsWithChildren, ReactNode } from "react";

interface AppShellProps extends PropsWithChildren {
  eyebrow: string;
  title: string;
  subtitle: string;
  sidebar: ReactNode;
}

export function AppShell({ eyebrow, title, subtitle, sidebar, children }: AppShellProps) {
  return (
    <div className="kz-shell">
      <aside className="kz-shell__sidebar">{sidebar}</aside>
      <main className="kz-shell__main">
        <header className="kz-shell__hero">
          <p className="kz-shell__eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p className="kz-shell__subtitle">{subtitle}</p>
        </header>
        <section className="kz-shell__content">{children}</section>
      </main>
    </div>
  );
}
