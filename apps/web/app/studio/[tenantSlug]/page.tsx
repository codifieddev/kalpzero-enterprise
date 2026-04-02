import { AdminShellPreview } from "../../../components/admin-shell-preview";
import { getBlueprintPreview } from "../../../lib/runtime-publishing";

export const dynamic = "force-dynamic";

interface StudioPreviewPageProps {
  params: Promise<{
    tenantSlug: string;
  }>;
}

export default async function StudioPreviewPage({ params }: StudioPreviewPageProps) {
  const { tenantSlug } = await params;
  const blueprint = await getBlueprintPreview(tenantSlug);

  return <AdminShellPreview blueprint={blueprint} />;
}
