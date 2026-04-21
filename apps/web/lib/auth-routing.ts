export function resolvePostLoginRoute(role: string | null | undefined): string {
  switch (role) {
    case "platform_admin":
      return "/platform";
    case "platform_owner":
      return "/dashboard";
    default:
      return "/tenant";
  }
}
