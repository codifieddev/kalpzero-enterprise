import { StatCard } from "@kalpzero/ui";

const publicSurfaces = [
  {
    label: "Tenant sites",
    value: "Brand + SEO",
    hint: "Dedicated domain profiles, content states, and live publishing contracts."
  },
  {
    label: "Commerce storefront",
    value: "Catalog commerce",
    hint: "Product, inventory, coupon, and checkout aware public pages."
  },
  {
    label: "Travel landing pages",
    value: "Package discovery",
    hint: "Destination-led content with departures, itinerary, and inquiry capture."
  },
  {
    label: "Hotel direct booking",
    value: "Reservation path",
    hint: "Room inventory and property publishing powered by the unified hotel pack."
  }
];

export default function DiscoverPage() {
  return (
    <main className="kz-public">
      <section className="kz-public__hero">
        <p className="kz-section-label">Public publishing</p>
        <h1>Discovery and publishing are first-class platform capabilities.</h1>
        <p>
          The public surface is no longer a fallback demo layer. It is fed by canonical
          brand, content, inventory, and SEO contracts.
        </p>
      </section>

      <section className="kz-grid">
        {publicSurfaces.map((surface) => (
          <StatCard
            key={surface.label}
            label={surface.label}
            value={surface.value}
            hint={surface.hint}
          />
        ))}
      </section>
    </main>
  );
}
