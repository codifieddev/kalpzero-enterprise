"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/components/providers/auth-provider";

export default function HomePage() {
  const router = useRouter();
  const { session, status } = useAuth();

  useEffect(() => {
    if (status === "loading") {
      return;
    }

    if (status === "anonymous") {
      router.replace("/login");
      return;
    }

    router.replace(session?.roles.includes("platform_admin") ? "/platform" : "/tenant");
  }, [router, session?.roles, status]);

  return <div className="min-h-screen bg-background" />;
}
