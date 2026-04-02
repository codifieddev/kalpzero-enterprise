import type { CSSProperties } from "react";
import type { BusinessBlueprintDto } from "@kalpzero/contracts";

function previewVariables(blueprint: BusinessBlueprintDto): CSSProperties {
  return {
    ["--admin-primary" as string]: blueprint.adminTheme.primaryColor,
    ["--admin-accent" as string]: blueprint.adminTheme.accentColor,
    ["--admin-surface" as string]: blueprint.adminTheme.surfaceColor,
    ["--admin-ink" as string]: blueprint.adminTheme.inkColor,
    ["--admin-muted" as string]: blueprint.adminTheme.mutedColor
  };
}

export function AdminShellPreview({ blueprint }: { blueprint: BusinessBlueprintDto }) {
  return (
    <main className="kz-admin-preview" style={previewVariables(blueprint)}>
      <aside className="kz-admin-preview__sidebar">
        <p className="kz-admin-preview__brand">{blueprint.adminTheme.brandName}</p>
        <nav className="kz-admin-preview__nav">
          {blueprint.adminNavigation.map((item) => (
            <span key={`${item.label}:${item.href}`}>{item.label}</span>
          ))}
        </nav>
      </aside>
      <section className="kz-admin-preview__main">
        <header className="kz-admin-preview__hero">
          <p className="kz-site__eyebrow">Admin Blueprint</p>
          <h1>{blueprint.businessLabel} operator shell</h1>
          <p>
            Admin layout, navigation, widgets, and vocabulary can vary per tenant while the
            backend and module boundaries remain shared.
          </p>
        </header>
        <div className="kz-admin-preview__widgets">
          {blueprint.dashboardWidgets.map((widget) => (
            <article key={widget.key} className="kz-admin-preview__widget">
              <span>{widget.title}</span>
              <strong>{widget.metric}</strong>
              <p>{widget.description}</p>
            </article>
          ))}
        </div>
        <section className="kz-admin-preview__panel">
          <h2>Vocabulary</h2>
          <div className="kz-admin-preview__vocab">
            {Object.entries(blueprint.vocabulary).map(([key, value]) => (
              <article key={key}>
                <small>{key}</small>
                <strong>{value}</strong>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
