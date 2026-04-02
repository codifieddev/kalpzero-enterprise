const navItems = [
  { label: "Platform", value: "Auth, tenancy, registry, audit" },
  { label: "Wave 1", value: "Commerce, travel, hotel" },
  { label: "AI", value: "Governed tenant runtimes" },
  { label: "Migration", value: "Legacy and external adapters" }
];

export function Sidebar() {
  return (
    <div className="kz-nav">
      <div>
        <p className="kz-nav__brand">KalpZero Enterprise</p>
        <p className="kz-nav__caption">Canonical workspace</p>
      </div>
      <ul className="kz-nav__list">
        {navItems.map((item) => (
          <li key={item.label}>
            <span>{item.label}</span>
            <small>{item.value}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
