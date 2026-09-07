# Path Restore

A calm, mobile-first static website for a soul care and wellness coaching practice.
Built with plain HTML and shared CSS. No framework, build step, JavaScript, external fonts, or paid services.

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

Each page contains its own semantic header, navigation, main, and footer. This deliberate duplication keeps the website build-free. When editing navigation or footer content, update all five pages. `aria-current="page"` identifies the current navigation item.

Relative links allow previews on both GitHub Pages project paths and a future custom domain. No deployment, domain, DNS, or paid service has been configured.

## Design system

Edit the CSS `:root` variables to change colors, fonts, spacing, and the 72rem maximum page width. Georgia supplies warm serif headings; the device's system font handles body text. The palette uses ivory, olive, and muted green, with high-contrast text and a visible brown keyboard focus outline. The navigation remains visible and wraps on small screens. Two-column layouts start at 48rem.

The homepage landscape is a decorative inline SVG, hidden from assistive technology; it requires no image download. Replace it with approved photography only if desired. For meaningful photos, supply descriptive alt text; purely decorative photos should have empty alt text.

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
