const searchHistory = (searchInput) => {
    const searchRows = document.querySelectorAll('.search-row');
    let noResultsMessage = document.getElementById('no-results-message');
    let resultsFound = false;

    const matchesSearch = (text) => text.toLowerCase().includes(searchInput.toLowerCase());

    searchRows.forEach(row => {
        const userMessage = row.querySelector('.user-msg-item').innerText;
        const assistantMessage = row.querySelector('.system-msg-item').innerText;
        const keywords = Array.from(row.querySelectorAll('.keyword-item li')).map(li => li.innerText);

        const matchFound = [userMessage, assistantMessage, ...keywords].some(matchesSearch);

        row.style.display = matchFound ? '' : 'none';
        resultsFound = resultsFound || matchFound;
    });

    if (!resultsFound && !noResultsMessage) {
        noResultsMessage = document.createElement('p');
        noResultsMessage.id = 'no-results-message';
        noResultsMessage.innerText = 'No results found';
        const historySection = document.querySelector('.history');
        historySection.appendChild(noResultsMessage);
    } else if (resultsFound && noResultsMessage) {
        noResultsMessage.remove();
    }
};

document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const searchInput = document.getElementById('search').value.trim();
    searchHistory(searchInput);
});

document.querySelectorAll('.keyword-item li').forEach(keywordElement => {
    keywordElement.addEventListener('click', () => {
        const keyword = keywordElement.innerText.trim();
        document.getElementById('search').value = keyword;
        searchHistory(keyword);
    });
});