# nicogaraycons

Consulting and portfolio site for Nico Garay, independent consultant specialized in AI agent integration for companies.

**Live site:** [nicogaray.com](https://nicogaray.com)

## About

This repository powers Nico Garay's consulting presence:

- **nicogaray.com** ([index.html](index.html)): main consulting portfolio, presenting AI agent integration services, remote-first positioning, and client case studies.
- **City landing pages**: localized versions for Bordeaux, Lille, Lyon, Marseille, Nantes, Nice, Paris, Toulouse, plus country pages for Belgium, Switzerland, and Luxembourg, and an English section (`/en`) for international audiences (Canada, UK, Singapore, US).
- **Case studies** (`/cas` in French, `/en/cases` in English, linked with hreflang): concrete AI agent implementations in production. They share [assets/cas/case.css](assets/cas/case.css).
- **Use-case diagnostic**: the `#results` section of the generic home pages (FR, Paris, BE, CH, LU and the English pages) lets visitors pick their problem and see the matching agent. Styles and script live in [assets/cas/diagnostic.css](assets/cas/diagnostic.css) and [assets/cas/diagnostic.js](assets/cas/diagnostic.js).
- **formation.nicogaray.com** lives in its own repository, [nicogaray7/nicogaray-formation](https://github.com/nicogaray7/nicogaray-formation).

## Tech stack

- Static HTML/CSS/JS, no build step or framework
- Hosted on GitHub Pages from the `main` branch, with the custom domain set in [CNAME](CNAME); `www.nicogaray.com` redirects to the apex domain
- `.nojekyll` publishes every file as is; [404.html](404.html) is served for unknown URLs
- Moved URLs are handled by small browser redirect pages (for example [cas/agent-rdv-artisan/](cas/agent-rdv-artisan/index.html)), since GitHub Pages cannot send server redirects
- Google Analytics 4 (direct gtag on every page, including the `/go/` redirect pages and the 404) for traffic and conversion tracking, with custom event tracking in [assets/track.js](assets/track.js) (see [docs/analytics-conversions.md](docs/analytics-conversions.md))
- Platform logos are self-hosted favicons in [assets/logos](assets/logos)
- Structured data (JSON-LD) for SEO and local business signals

## Structure

Each locale/city has its own directory with a self-contained `index.html`. Shared assets (tracking script, favicons, logos, OG image) live in `assets/` and `favicon/`. `sitemap.xml` and `robots.txt` sit at the root.

## License

Proprietary. See [LICENSE](LICENSE).

## Shared header and footer

The footer of every page except the Bordeaux landing page comes from a shared
template, so a footer change is made once:

- Templates: `_shared/footer-home.fr.html` / `.en.html` (home, city, country and
  legal pages) and `_shared/footer-case.fr.html` / `.en.html` (case studies).
- Fragments shared by several pages: `_shared/snippets/`.
- Per-page values (tagline, city links, `lead=`): `_shared/pages/<page>.json`.

After editing any of them, run `python3 _shared/render.py` and commit the
regenerated pages. Never edit a footer inside a page between the
`<!-- shared:footer -->` markers: the `Check shared header/footer` workflow
fails the pull request when a page no longer matches its template
(`python3 _shared/render.py --check` runs the same check locally).

The same script also inlines small shared CSS files (`assets/fonts.css`,
`assets/cas/diagnostic.css`) as a `<style>` block between
`<!-- shared:css:<name> -->` markers on any page listing that name in its
`"css"` array in `_shared/pages/<page>.json`, so the browser does not pay for
an extra render-blocking request. Edit the `.css` file, never the inlined
`<style>` block, then re-run `python3 _shared/render.py`.
