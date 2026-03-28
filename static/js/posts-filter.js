(function () {
  const root = document.getElementById("posts-filters");
  const grid = document.getElementById("posts-grid");
  const status = document.getElementById("posts-filter-status");
  const resetButton = document.getElementById("posts-filter-reset");

  if (!root || !grid || !status || !resetButton) {
    return;
  }

  const cards = Array.from(grid.querySelectorAll(".post-card"));
  const state = {
    category: "",
    tag: "",
  };

  const updateButtons = () => {
    root.querySelectorAll("[data-filter-group]").forEach((group) => {
      const key = group.getAttribute("data-filter-group");
      const value = state[key] || "";
      group.querySelectorAll(".filter-chip").forEach((button) => {
        const active = button.getAttribute("data-filter-value") === value;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      });
    });
  };

  const updateUrl = () => {
    const url = new URL(window.location.href);
    if (state.category) {
      url.searchParams.set("category", state.category);
    } else {
      url.searchParams.delete("category");
    }
    if (state.tag) {
      url.searchParams.set("tag", state.tag);
    } else {
      url.searchParams.delete("tag");
    }
    window.history.replaceState({}, "", url);
  };

  const applyFilters = () => {
    let visibleCount = 0;
    cards.forEach((card) => {
      const categoryMatch = !state.category || card.dataset.category === state.category;
      const tags = (card.dataset.tags || "").split("|").filter(Boolean);
      const tagMatch = !state.tag || tags.includes(state.tag);
      const visible = categoryMatch && tagMatch;
      card.hidden = !visible;
      if (visible) {
        visibleCount += 1;
      }
    });

    const parts = [];
    if (state.category) {
      parts.push("栏目：" + state.category);
    }
    if (state.tag) {
      parts.push("标签：" + state.tag);
    }

    status.textContent = parts.length
      ? "当前筛选为 " + parts.join(" / ") + "，共 " + visibleCount + " 篇文章。"
      : "当前显示全部 " + visibleCount + " 篇文章。";
  };

  const setStateFromUrl = () => {
    const params = new URLSearchParams(window.location.search);
    state.category = params.get("category") || "";
    state.tag = params.get("tag") || "";
  };

  root.querySelectorAll(".filter-chip").forEach((button) => {
    button.addEventListener("click", function () {
      const parent = this.closest("[data-filter-group]");
      if (!parent) {
        return;
      }
      const key = parent.getAttribute("data-filter-group");
      state[key] = this.getAttribute("data-filter-value") || "";
      updateButtons();
      applyFilters();
      updateUrl();
    });
  });

  resetButton.addEventListener("click", function () {
    state.category = "";
    state.tag = "";
    updateButtons();
    applyFilters();
    updateUrl();
  });

  setStateFromUrl();
  updateButtons();
  applyFilters();
})();
