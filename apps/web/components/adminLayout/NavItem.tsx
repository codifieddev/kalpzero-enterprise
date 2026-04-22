"use client";

import React from "react";
import { useRouter } from "next/navigation";

interface NavItemProps {
  href: string;
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  borderHover?: boolean;
  collapsed?: boolean;
  onClick?: () => void;
}

export function NavItem({
  href,
  icon,
  label,
  active = false,
  borderHover = false,
  collapsed = false,
  onClick,
}: NavItemProps) {
  const router = useRouter();

  const handleClick = () => {
    router.push(href);
    if (onClick) onClick();
  };

  return (
    <button
      onClick={handleClick}
      title={collapsed ? label : undefined}
      className={`w-full flex items-center gap-3 py-2.5 rounded-lg text-sm transition-all duration-300 relative group overflow-hidden ${
        collapsed ? "justify-center px-2" : "px-3"
      } ${
        active
          ? "bg-cyan-500/10 text-cyan-300 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]"
          : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
      }`}
    >
      {/* Active Indicator Line */}
      {active && (
        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1/2 bg-cyan-400 rounded-r-md shadow-[0_0_10px_rgba(0,240,255,0.8)]"></div>
      )}

      {/* Icon */}
      <span
        className={`relative z-10 transition-colors ${
          active ? "text-cyan-400" : "group-hover:text-cyan-400/70"
        }`}
      >
        {icon}
      </span>

      {/* Label */}
      {!collapsed && (
        <span
          className={`relative z-10 tracking-wide ${
            active ? "font-medium" : "font-normal"
          }`}
        >
          {label}
        </span>
      )}

      {/* Optional border glow on hover */}
      {borderHover && !active && (
        <div className="absolute inset-0 border border-transparent group-hover:border-cyan-500/30 rounded-lg transition-colors pointer-events-none"></div>
      )}
    </button>
  );
}
