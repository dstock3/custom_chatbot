document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search");
    const tableRows = document.querySelectorAll(".history-section table tr");
  
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
  
      const searchTerm = searchInput.value.toLowerCase().trim();
  
      // loop through all table rows and hide those that don't match the search term
      for (let i = 1; i < tableRows.length; i++) {
        const row = tableRows[i];
        const userMessage = row.cells[1].innerText.toLowerCase();
        const assistantMessage = row.cells[2].innerText.toLowerCase();
        const keywords = row.cells[3].innerText.toLowerCase();
  
        if (
          userMessage.includes(searchTerm) ||
          assistantMessage.includes(searchTerm) ||
          keywords.includes(searchTerm)
        ) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      }
    });
  });