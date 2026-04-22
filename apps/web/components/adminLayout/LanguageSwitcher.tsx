"use client";

import React, { useState } from "react";
import { Languages } from "lucide-react";
import { useTranslation } from "@/lib/i18n/context";

const LOCALE_META: Record<string, { flag: string; label: string }> = {
  en: { flag: "🇬🇧", label: "EN" },
  hi: { flag: "🇮🇳", label: "HI" },
  hr: { flag: "🇭🇷", label: "HR" },
  "zh-hant": { flag: "🇹🇼", label: "繁中" },
};

export function LanguageSwitcher() {
  const { locale, setLocale, availableLocales } = useTranslation();
  const [open, setOpen] = useState(false);
  const meta = LOCALE_META[locale] || LOCALE_META.en;

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 bg-slate-900/50 px-2.5 py-1.5 rounded-full border border-slate-800 shadow-inner text-xs hover:border-slate-600 transition-colors"
      >
        <Languages size={12} className="text-slate-400" />
        <span>{meta.flag}</span>
        <span className="text-slate-400 font-bold text-[10px]">
          {meta.label}
        </span>
      </button>
      {open && (
        <div className="absolute top-full right-0 mt-1 bg-slate-900 border border-slate-700 rounded-lg overflow-hidden shadow-xl z-50 min-w-[120px]">
          {availableLocales.map((loc) => {
            const m = LOCALE_META[loc];
            if (!m) return null;
            return (
              <button
                key={loc}
                onClick={() => {
                  setLocale(loc);
                  setOpen(false);
                }}
                className={`w-full flex items-center gap-2 px-3 py-2 text-xs hover:bg-slate-800 transition-colors ${
                  locale === loc
                    ? "text-cyan-400 bg-slate-800/50"
                    : "text-slate-300"
                }`}
              >
                <span>{m.flag}</span>
                <span className="font-medium">{m.label}</span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
