# Path Restore

A calm, mobile-first static website for a soul care and wellness coaching practice.
Built with static HTML and shared CSS. The resource library uses a small JavaScript search enhancement.

## Preview locally

From this folder, run:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000 in your browser. Stop the server with Ctrl+C.
You can also open `index.html` directly, though a local server more closely resembles hosting.

## File structure

- `index.html` — homepage, introduction, coaching themes, consultation CTA.
- `coaching.html` — draft approach and coaching structure.
- `about.html` — practitioner biography and portrait placeholders.
- `resources.html` — resource landing page with a draft reflection prompt.
- `schedule.html` — consultation introduction and clearly labeled Healthie placeholder.
- `assets/css/styles.css` — shared design tokens, typography, components, and responsive layouts, organized into numbered sections.
- `.nojekyll` — tells GitHub Pages to serve this as a plain static site.

Each page contains its own semantic header, navigation, main, and footer. This deliberate duplication keeps the website build-free. When editing navigation or footer content, update every page, including resource articles. `aria-current="page"` identifies the current navigation item.

Relative links allow local previews. GitHub Pages serves the production site at `https://pathrestore.com`.

## Article publishing and search discovery

One-time setup when adopting this workflow: in **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source and confirm the custom domain is `pathrestore.com` with HTTPS enforced. Once the workflow is on `main`, run **Actions → Publish Path Restore → Run workflow** on `main` if it did not already deploy. The root IndexNow key is published with the site. No secrets or search-engine account changes are needed.

- Publish approved articles as `resources/article-slug.html` and add a card with a relative link in `resources.html`. Keep drafts out of the public library. Use the exact production HTTPS canonical and an absolute HTTPS `og:image` URL on `pathrestore.com`.
- In the article's JSON-LD, set `datePublished` when known and update `dateModified` for significant changes. Use `YYYY-MM-DD`. The publish workflow generates the live sitemap from the Resources links and copies those dates into `lastmod` where available. Google discovers URLs by crawling the sitemap already submitted in Search Console and advertised in `robots.txt`.
- After Pages reports success, the workflow checks new and materially changed articles against the last successful run. It checks the live HTML, canonical, title, description, social image, sitemap and crawler access, then sends those URLs in one IndexNow submission to participating engines, including Bing. Shared navigation and footer edits alone do not trigger a submission.
- Check **Actions → Publish Path Restore** for deployment, validation and IndexNow results. If live checks fail, read the reported URL and fix the metadata, image, or crawl rules. If IndexNow rejects the batch, check the live root key file and HTTP status. After a transient failure, run the workflow on current `main` again. The next successful run also picks up pending changes since the last successful submission.
- Occasionally review sitemap processing and indexing coverage in Google Search Console and Bing Webmaster Tools. A successful notification confirms receipt. Search engines decide when to crawl and index each URL.

## Design system

Edit the CSS `:root` variables to change colors, fonts, spacing, and the 72rem maximum page width. Georgia supplies warm serif headings; the device's system font handles body text. The palette uses ivory, olive, and muted green, with high-contrast text and a visible brown keyboard focus outline. The navigation remains visible and wraps on small screens. Two-column layouts start at 48rem.

The approved Path Restore logo is the landscape-and-path SVG currently displayed in the homepage hero, without the tagline. Its reusable asset is `assets/images/path-restore-logo.svg`. Preserve its shapes, colors, proportions, and internal spacing; do not redraw or restyle it. The homepage retains the identical inline SVG and existing CSS framing to preserve its layout. The standalone asset contains the SVG artwork; the rounded hero framing is applied separately by the page CSS. The header’s “path restore” and “Mentoring and coaching” HTML text remain unchanged. When using the logo as a meaningful image, use alt text such as “Path Restore”; decorative repetitions may use empty alt text.

## Before publishing

All descriptive copy is provisional, visibly labeled by a working-draft notice on every page. Search for `placeholder`, `Draft`, `PLACEHOLDER`, and `HEALTHIE` to find editorial work.

- Approve or replace homepage copy, coaching themes, and the draft reflection prompt.
- Confirm coaching methods, scope, service details, pricing, consultation duration, format, and spiritual language.
- Add the real practitioner name, biography, verified credentials, and portrait; replace the portrait's alt-text placeholder.
- Add reviewed resources and real source links. No fake article links are present.
- Replace the Schedule placeholder with the existing verified Healthie iframe. Give it a descriptive `title`, use the `.booking-frame` class, and add a real direct booking link outside the embed. Verify keyboard operation, mobile layout, scrolling, time zones, and a complete booking flow. Review any privacy language needed for that integration.
- Confirm canonical and Open Graph URLs using `https://pathrestore.com/` as the provisional preferred domain. These HTML metadata values do not configure the domain. Add an approved social image with `og:image` and `og:image:alt`; comments mark its location in every page.
- Remove working-draft notices and editorial placeholder text only after those items are complete.

## Review

Check all five pages on a narrow phone and desktop. Tab through navigation and calls to action, try the skip link, and check the page at 200% zoom. Navigation works without JavaScript. Each page has a unique title and description, one main heading, semantic landmarks, and a current-page navigation label.

The existing Jekyll-related `.gitignore` is retained; it is harmless for this plain HTML site. There are no dependencies to install.
