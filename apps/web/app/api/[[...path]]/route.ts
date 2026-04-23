import type { NextRequest } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface ProxyRouteContext {
  params: Promise<{
    path?: string[];
  }>;
}

function normalizeAbsoluteUrl(value: string | undefined) {
  if (!value) {
    return null;
  }

  const trimmed = value.endsWith("/") ? value.slice(0, -1) : value;
  if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
    return trimmed;
  }

  return null;
}

function resolveApiProxyBaseUrl() {
  return (
    normalizeAbsoluteUrl(process.env.KALPZERO_API_PROXY_URL) ??
    normalizeAbsoluteUrl(process.env.KALPZERO_INTERNAL_API_URL) ??
    normalizeAbsoluteUrl(process.env.KALPZERO_PUBLIC_API_URL) ??
    "http://127.0.0.1:8012"
  );
}

function buildTargetUrl(request: NextRequest, path: string[] | undefined) {
  const incomingUrl = new URL(request.url);
  const pathname = path && path.length > 0 ? `/${path.join("/")}` : "";
  return `${resolveApiProxyBaseUrl()}${pathname}${incomingUrl.search}`;
}

async function proxyRequest(request: NextRequest, context: ProxyRouteContext) {
  const { path } = await context.params;
  const incomingUrl = new URL(request.url);
  const targetUrl = buildTargetUrl(request, path);
  const headers = new Headers(request.headers);

  // Let fetch derive the backend host header from the target URL.
  headers.delete("host");
  headers.set("x-forwarded-host", incomingUrl.host);
  headers.set("x-forwarded-proto", incomingUrl.protocol.replace(":", ""));

  const init: RequestInit = {
    method: request.method,
    headers,
    cache: "no-store",
    redirect: "manual"
  };

  if (request.method !== "GET" && request.method !== "HEAD") {
    const body = await request.arrayBuffer();
    if (body.byteLength > 0) {
      init.body = body;
    }
  }

  const response = await fetch(targetUrl, init);
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: new Headers(response.headers)
  });
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const PATCH = proxyRequest;
export const DELETE = proxyRequest;
export const OPTIONS = proxyRequest;
export const HEAD = proxyRequest;
