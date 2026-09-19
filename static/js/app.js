document.documentElement.dataset.js = "true";

(function () {
  const root = document.documentElement;

  function currentTheme() {
    const attr = root.getAttribute("data-theme");
    if (attr === "light" || attr === "dark") {
      return attr;
    }
    return window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      /* ignore quota / private mode */
    }
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.setAttribute(
        "aria-label",
        theme === "dark" ? "فعال‌سازی حالت روشن" : "فعال‌سازی حالت تیره",
      );
      const icon = btn.querySelector("[data-theme-icon]");
      if (icon) {
        icon.textContent = theme === "dark" ? "Light" : "Dark";
      }
    });
  }

  document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  });

  applyTheme(currentTheme());
})();

(function () {
  const dialog = document.getElementById("case-dialog");
  const dataEl = document.getElementById("case-studies-data");
  if (!dialog || !dataEl) {
    return;
  }

  let projects = [];
  try {
    projects = JSON.parse(dataEl.textContent || "[]");
  } catch (e) {
    return;
  }

  const byId = Object.fromEntries(projects.map((p) => [p.id, p]));
  let lastTrigger = null;

  const titleEl = dialog.querySelector("#case-dialog-title");
  const subtitleEl = dialog.querySelector("#case-dialog-subtitle");
  const problemEl = dialog.querySelector("[data-case-problem]");
  const roleEl = dialog.querySelector("[data-case-role]");
  const stackEl = dialog.querySelector("[data-case-stack]");
  const highlightsEl = dialog.querySelector("[data-case-highlights]");

  function fillDialog(project) {
    titleEl.textContent = project.title;
    subtitleEl.textContent = project.subtitle;
    problemEl.textContent = project.problem;
    roleEl.textContent = project.role;

    stackEl.replaceChildren();
    (project.stack || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      stackEl.appendChild(li);
    });

    highlightsEl.replaceChildren();
    (project.highlights || []).forEach((h) => {
      const li = document.createElement("li");
      const strong = document.createElement("strong");
      strong.textContent = h.title;
      const span = document.createElement("span");
      span.textContent = h.body;
      li.append(strong, span);
      highlightsEl.appendChild(li);
    });
  }

  function getFocusable() {
    return Array.from(
      dialog.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
      ),
    ).filter((el) => !el.hasAttribute("disabled") && el.offsetParent !== null);
  }

  function openCase(id, trigger) {
    const project = byId[id];
    if (!project) {
      return;
    }
    lastTrigger = trigger || null;
    fillDialog(project);
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
    const closeBtn = dialog.querySelector("[data-case-close]");
    if (closeBtn) {
      closeBtn.focus();
    }
  }

  function closeCase() {
    if (typeof dialog.close === "function") {
      dialog.close();
    } else {
      dialog.removeAttribute("open");
    }
    if (lastTrigger) {
      lastTrigger.focus();
    }
  }

  document.querySelectorAll("[data-case-open]").forEach((btn) => {
    btn.addEventListener("click", () => {
      openCase(btn.getAttribute("data-case-open"), btn);
    });
  });

  dialog.querySelectorAll("[data-case-close]").forEach((btn) => {
    btn.addEventListener("click", closeCase);
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      closeCase();
    }
  });

  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    closeCase();
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key !== "Tab" || !dialog.open) {
      return;
    }
    const focusable = getFocusable();
    if (focusable.length === 0) {
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
})();
