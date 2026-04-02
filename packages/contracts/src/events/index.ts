export type DomainEventName =
  | "tenant.provisioned"
  | "import.job.queued"
  | "import.completed"
  | "import.failed"
  | "commerce.order.created"
  | "commerce.fulfillment.updated"
  | "commerce.shipment.updated"
  | "travel.booking.updated"
  | "travel.lead.updated"
  | "hotel.reservation.updated"
  | "invoice.issued"
  | "publishing.content.published"
  | "ai.usage.recorded";

export interface DomainEventDto<TPayload = Record<string, unknown>> {
  id: string;
  name: DomainEventName;
  tenantId: string;
  aggregateId: string;
  occurredAt: string;
  payload: TPayload;
}

export interface AuditEventDto {
  id: string;
  tenantId: string;
  actorUserId: string;
  action: string;
  subjectType: string;
  subjectId: string;
  metadata: Record<string, unknown>;
  createdAt: string;
}
