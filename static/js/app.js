document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", () => {
      const willOpen = !menu.classList.contains("is-open");
      menu.classList.toggle("is-open", willOpen);
      if (willOpen) {
        menu.removeAttribute("hidden");
      } else {
        menu.setAttribute("hidden", "");
      }
      menuBtn.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });
  }

  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = () => {
      header.classList.toggle("header-scrolled", window.scrollY > 40);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  const searchBtn = document.getElementById("open-search");
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      window.location.href = "/shop/products/";
    });
  }
});
