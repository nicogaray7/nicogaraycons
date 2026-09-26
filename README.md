# nicogaraycons

Consulting and portfolio site for Nico Garay, independent consultant specialized in AI agent integration for companies.

**Live site:** [nicogaray.com](https://nicogaray.com)

## About

This repository powers Nico Garay's consulting presence:

- **nicogaray.com** ([index.html](index.html)): main consulting portfolio, presenting AI agent integration services, remote-first positioning, and client case studies.
- **City landing pages**: localized versions for Bordeaux, Lille, Lyon, Marseille, Nantes, Nice, Paris, Toulouse, plus country pages for Belgium, Switzerland, and Luxembourg, and an English section (`/en`) for international audiences (Canada, UK, Singapore, US).
- **Case studies** (`/cas`): concrete AI agent implementation examples.
- **formation.nicogaray.com** lives in its own repository, [nicogaray7/nicogaray-formation](https://github.com/nicogaray7/nicogaray-formation).

## Tech stack

- Static HTML/CSS/JS, no build step or framework
- Hosted on GitHub Pages from the `main` branch, with the custom domain set in [CNAME](CNAME); `www.nicogaray.com` redirects to the apex domain
- `.nojekyll` publishes every file as is; [404.html](404.html) is served for unknown URLs
- Moved URLs are handled by small browser redirect pages (for example [cas/agent-rdv-artisan/](cas/agent-rdv-artisan/index.html)), since GitHub Pages cannot send server redirects
- Google Analytics 4 (via GTM and direct gtag) for traffic and conversion tracking, with custom event tracking in [assets/track.js](assets/track.js) (see [docs/analytics-conversions.md](docs/analytics-conversions.md))
- Platform logos are self-hosted favicons in [assets/logos](assets/logos)
- Structured data (JSON-LD) for SEO and local business signals

## Structure

Each locale/city has its own directory with a self-contained `index.html`. Shared assets (tracking script, favicons, logos, OG image) live in `assets/` and `favicon/`. `sitemap.xml` and `robots.txt` sit at the root.

## License

Proprietary. See [LICENSE](LICENSE).
