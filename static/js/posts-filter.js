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
    topic: "",
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
    if (state.topic) {
      url.searchParams.set("topic", state.topic);
    } else {
      url.searchParams.delete("topic");
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
      const topics = (card.dataset.topics || "").split("|").filter(Boolean);
      const topicMatch = !state.topic || topics.includes(state.topic);
      const tags = (card.dataset.tags || "").split("|").filter(Boolean);
      const tagMatch = !state.tag || tags.includes(state.tag);
      const visible = topicMatch && tagMatch;
      card.hidden = !visible;
      if (visible) {
        visibleCount += 1;
      }
    });

    const parts = [];
    if (state.topic) {
      parts.push("研究领域：" + state.topic);
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
    state.topic = params.get("topic") || "";
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
    state.topic = "";
    state.tag = "";
    updateButtons();
    applyFilters();
    updateUrl();
  });

  setStateFromUrl();
  updateButtons();
  applyFilters();
})();
