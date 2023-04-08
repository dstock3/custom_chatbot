document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const searchInput = document.getElementById('search').value.trim().toLowerCase();
    const searchRows = document.querySelectorAll('.search-row');
    let noResultsMessage = document.getElementById('no-results-message');
    let resultsFound = false;

    searchRows.forEach(row => {
        const userMessage = row.cells[1].innerText.toLowerCase();
        const assistantMessage = row.cells[2].innerText.toLowerCase();
        const keywords = row.cells[3].innerText.toLowerCase();

        if (userMessage.includes(searchInput) || assistantMessage.includes(searchInput) || keywords.includes(searchInput)) {
            row.style.display = '';
            resultsFound = true;
        } else {
            row.style.display = 'none';
        }
    });

    if (!resultsFound) {
        if (!noResultsMessage) {
            noResultsMessage = document.createElement('p');
            noResultsMessage.id = 'no-results-message';
            noResultsMessage.innerText = 'No results found';
            const historySection = document.querySelector('.history-section');
            historySection.appendChild(noResultsMessage);
        }
    } else {
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }
});
