(function () {
  const input = document.getElementById("glossary-search");
  const grid = document.getElementById("glossary-grid");

  if (!input || !grid) {
    return;
  }

  const cards = Array.from(grid.querySelectorAll(".glossary-card"));

  input.addEventListener("input", function () {
    const keyword = this.value.trim().toLowerCase();
    cards.forEach((card) => {
      const haystack = [card.dataset.term || "", card.dataset.summary || ""].join(" ").toLowerCase();
      card.hidden = keyword ? !haystack.includes(keyword) : false;
    });
  });
})();
