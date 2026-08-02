function base64UrlDecode(segment) {
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/");
  const withPad = padded + "=".repeat((4 - (padded.length % 4)) % 4);
  const decoded = atob(withPad);
  try {
    return decodeURIComponent(
      decoded
        .split("")
        .map((c) => "%" + c.charCodeAt(0).toString(16).padStart(2, "0"))
        .join(""),
    );
  } catch {
    return decoded;
  }
}

export function decodeToken(token) {
  if (!token || typeof token !== "string") return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    return JSON.parse(base64UrlDecode(parts[1]));
  } catch {
    return null;
  }
}

export function isTokenExpired(token) {
  const payload = decodeToken(token);
  if (!payload?.exp) return false;
  return Date.now() >= payload.exp * 1000;
}

export function getUserType(token) {
  const payload = decodeToken(token);
  return payload?.context?.user_type ?? null;
}

export function getUsername(token) {
  const payload = decodeToken(token);
  return payload?.context?.username ?? null;
}
