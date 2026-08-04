# nicogaraycons

Consulting and portfolio site for Nico Garay, independent consultant specialized in AI agent integration for companies.

**Live site:** [nicogaray.com](https://nicogaray.com)

## About

This repository powers Nico Garay's consulting presence:

- **nicogaray.com** ([index.html](index.html)): main consulting portfolio, presenting AI agent integration services, remote-first positioning, and client case studies.
- **City landing pages**: localized versions for Bordeaux, Lille, Lyon, Marseille, Nantes, Nice, Paris, Toulouse, plus country pages for Belgium, Switzerland, and Luxembourg, and an English section (`/en`) for international audiences (Canada, UK, Singapore, US).
- **Case studies** (`/cas`): concrete AI agent implementation examples (e.g. appointment-booking agent for artisans, healthcare chatbot with scheduling).
- **formation.nicogaray.com** ([formation/index.html](formation/index.html)): a separate landing page under the same Vercel project, offering in-home and remote computer/smartphone lessons, mainly targeted at seniors around Créon and the Entre-deux-Mers area (Gironde, France).

## Tech stack

- Static HTML/CSS/JS, no build step or framework
- Hosted on [Vercel](https://vercel.com), with routing, redirects, and security headers configured in [vercel.json](vercel.json)
- Vercel Edge Middleware ([middleware.js](middleware.js)) for country-based access rules
- Google Analytics 4 (via GTM and direct gtag) for traffic and conversion tracking, with custom event tracking in [assets/track.js](assets/track.js) (see [docs/analytics-conversions.md](docs/analytics-conversions.md))
- Structured data (JSON-LD) for SEO and local business signals
- Multi-domain setup: `nicogaray.com` and `formation.nicogaray.com` served from the same deployment

## Structure

Each locale/city has its own directory with a self-contained `index.html`. Shared assets (tracking script, favicons, OG image) live in `assets/` and `favicon/`. `sitemap.xml` and `robots.txt` are maintained per site (root and `formation/`).

## License

Proprietary. See [LICENSE](LICENSE).
