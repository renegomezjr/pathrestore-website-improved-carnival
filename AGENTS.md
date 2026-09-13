# Shared site components

Treat the header, navigation, and footer as shared site components even though this site uses duplicated static HTML. Whenever one of these areas changes, update every applicable page consistently, including nested pages such as resource articles. Preserve correct relative links for each page's location.

Do not introduce JavaScript, a framework, or a build system solely to deduplicate shared markup. Preserve the current simple static GitHub Pages architecture unless the site grows enough that duplication causes real maintenance problems. If that point is reached, propose a lightweight templating or static-site approach before implementing it.
