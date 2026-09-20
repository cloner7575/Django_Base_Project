document.documentElement.dataset.js = "true";

// HTMX drops non-2xx responses by default. Our views answer 400 for invalid
// forms and 503 for degraded dependencies and still render a partial, so swap
// those instead of leaving the user staring at an unchanged page.
const SWAPPABLE_ERROR_STATUSES = [400, 422, 503];

document.addEventListener("htmx:beforeSwap", (event) => {
  if (SWAPPABLE_ERROR_STATUSES.includes(event.detail.xhr.status)) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});
