import type { CSSProperties } from "react";
import type { PageBlockDto, PublicSitePayloadDto } from "@kalpzero/contracts";
import Link from "next/link";

function siteVariables(site: PublicSitePayloadDto): CSSProperties {
  return {
    ["--tenant-primary" as string]: site.publicTheme.primaryColor,
    ["--tenant-accent" as string]: site.publicTheme.accentColor,
    ["--tenant-surface" as string]: site.publicTheme.surfaceColor,
    ["--tenant-ink" as string]: site.publicTheme.inkColor,
    ["--tenant-muted" as string]: site.publicTheme.mutedColor,
    ["--tenant-heading" as string]: site.publicTheme.headingFont,
    ["--tenant-body" as string]: site.publicTheme.bodyFont
  };
}

function renderBlock(block: PageBlockDto) {
  if (block.kind === "hero") {
    return (
      <section key={block.id} className="kz-site__hero">
        {block.eyebrow ? <p className="kz-site__eyebrow">{block.eyebrow}</p> : null}
        {block.headline ? <h1>{block.headline}</h1> : null}
        {block.body ? <p className="kz-site__lead">{block.body}</p> : null}
        {block.ctaLabel && block.ctaHref ? (
          <div className="kz-site__actions">
            <Link href={block.ctaHref} className="kz-site__cta">
              {block.ctaLabel}
            </Link>
          </div>
        ) : null}
      </section>
    );
  }

  if (block.kind === "feature_grid") {
    return (
      <section key={block.id} className="kz-site__panel">
        {block.headline ? <h2>{block.headline}</h2> : null}
        {block.body ? <p className="kz-site__copy">{block.body}</p> : null}
        <div className="kz-site__grid">
          {(block.items ?? []).map((item) => (
            <article key={item.title} className="kz-site__card">
              <h3>{item.title}</h3>
              {item.value ? <strong>{item.value}</strong> : null}
              {item.description ? <p>{item.description}</p> : null}
            </article>
          ))}
        </div>
      </section>
    );
  }

  if (block.kind === "stat_strip") {
    return (
      <section key={block.id} className="kz-site__stats">
        {(block.items ?? []).map((item) => (
          <article key={item.title} className="kz-site__stat">
            {item.value ? <strong>{item.value}</strong> : null}
            <span>{item.title}</span>
          </article>
        ))}
      </section>
    );
  }

  if (block.kind === "cta") {
    return (
      <section key={block.id} className="kz-site__panel kz-site__panel--cta">
        {block.headline ? <h2>{block.headline}</h2> : null}
        {block.body ? <p className="kz-site__copy">{block.body}</p> : null}
        {block.ctaLabel && block.ctaHref ? (
          <Link href={block.ctaHref} className="kz-site__cta">
            {block.ctaLabel}
          </Link>
        ) : null}
      </section>
    );
  }

  return (
    <section key={block.id} className="kz-site__panel">
      {block.headline ? <h2>{block.headline}</h2> : null}
      {block.body ? <p className="kz-site__copy">{block.body}</p> : null}
    </section>
  );
}

export function RuntimeSite({ site }: { site: PublicSitePayloadDto }) {
  return (
    <main className="kz-site" style={siteVariables(site)}>
      <header className="kz-site__header">
        <Link href="/" className="kz-site__brand">
          {site.businessLabel}
        </Link>
        <nav className="kz-site__nav">
          {site.publicNavigation.map((item) => (
            <Link
              key={`${item.label}:${item.href}`}
              href={item.href === "/" ? `/${site.tenantSlug}` : `/${site.tenantSlug}${item.href}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </header>
      <div className="kz-site__content">{site.page.blocks.map((block) => renderBlock(block))}</div>
      <section className="kz-site__discovery">
        <p className="kz-site__eyebrow">Discovery</p>
        <h2>{site.discovery.headline}</h2>
        <p className="kz-site__copy">{site.discovery.summary}</p>
        <div className="kz-site__grid">
          {site.discovery.cards.map((card) => (
            <article key={card.href} className="kz-site__card">
              <h3>{card.title}</h3>
              <p>{card.summary}</p>
              <Link href={card.href === "/" ? `/${site.tenantSlug}` : `/${site.tenantSlug}${card.href}`}>
                Open
              </Link>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
