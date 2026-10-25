// Cloudflare Pages middleware: one canonical host.
//
// www.elitebalaji.com and elitebalaji.pages.dev both served a full copy of
// the site, and Google indexed www pages as separate URLs, splitting their
// clicks and rankings. Every request to those hosts is answered with a 301 to
// the same path on elitebalaji.com. Branch previews (<branch>.elitebalaji.pages.dev)
// are untouched, so previews keep working.
//
// Deliberately tiny: anything unexpected falls through to the static site,
// so this can never take the site down.
const CANONICAL = "elitebalaji.com";
const REDIRECT_HOSTS = new Set(["www.elitebalaji.com", "elitebalaji.pages.dev"]);

export async function onRequest(context) {
  try {
    const url = new URL(context.request.url);
    if (REDIRECT_HOSTS.has(url.hostname)) {
      url.hostname = CANONICAL;
      url.protocol = "https:";
      url.port = "";
      return Response.redirect(url.toString(), 301);
    }
  } catch {
    // fall through
  }
  return context.next();
}
