// Edge Middleware Vercel : bloque l'acces depuis l'Inde.
// Vercel fournit le pays du visiteur via l'en-tete x-vercel-ip-country.
// S'applique a nicogaray.com et formation.nicogaray.com (meme projet).

export const config = { matcher: "/:path*" };

export default function middleware(request) {
  const country = request.headers.get("x-vercel-ip-country");
  if (country === "IN") {
    return new Response("Ce site n'est pas accessible depuis votre pays.", {
      status: 403,
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  }
}
