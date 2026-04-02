import type { ReactNode } from "react";

interface StatCardProps {
  label: string;
  value: string;
  hint: string;
  accent?: ReactNode;
}

export function StatCard({ label, value, hint, accent }: StatCardProps) {
  return (
    <article className="kz-stat-card">
      <div className="kz-stat-card__header">
        <span>{label}</span>
        {accent}
      </div>
      <strong>{value}</strong>
      <p>{hint}</p>
    </article>
  );
}
