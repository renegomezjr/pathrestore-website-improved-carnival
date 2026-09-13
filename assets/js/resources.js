// Entries stay visible without JavaScript. Search uses the visible listing text.
const search = document.querySelector('#resource-search');
const entries = Array.from(document.querySelectorAll('.resource-entry'), (element) => ({
  element,
  text: Array.from(element.querySelectorAll('.resource-title, .resource-entry-summary, .resource-topic'))
    .map((field) => field.textContent).join(' ').toLowerCase()
}));
const status = document.querySelector('.search-status');

function filterResources() {
  const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let count = 0;
  entries.forEach(({ element, text }) => {
    const matches = terms.every((term) => text.includes(term));
    element.hidden = !matches;
    if (matches) count += 1;
  });
  status.textContent = count === 0
    ? 'No resources found. Try another search.'
    : terms.length ? `${count} resource${count === 1 ? '' : 's'} found.` : '';
}

search.addEventListener('input', filterResources);
document.querySelector('.resource-search').hidden = false;
filterResources();
