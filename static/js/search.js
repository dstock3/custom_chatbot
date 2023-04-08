const searchHistory = (searchInput) => {
    searchInput = searchInput.trim().toLowerCase();
    const searchRows = document.querySelectorAll('.search-row');
    let noResultsMessage = document.getElementById('no-results-message');
    let resultsFound = false;

    searchRows.forEach(row => {
        const userMessage = row.querySelector('.user-msg-item').innerText.toLowerCase();
        const assistantMessage = row.querySelector('.system-msg-item').innerText.toLowerCase();
        const keywords = Array.from(row.querySelectorAll('.keyword-item li')).map(li => li.innerText.toLowerCase());
        const dateElement = row.querySelector('.date-item');
        const dateString = dateElement.dataset.date;
        const formattedDate = formatDate(dateString).toLowerCase();

        if (userMessage.includes(searchInput) || assistantMessage.includes(searchInput) || keywords.some(keyword => keyword.includes(searchInput)) || formattedDate.includes(searchInput)) {
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
            const historySection = document.querySelector('.history');
            historySection.appendChild(noResultsMessage);
        }
    } else {
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
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

const formatDate = (dateString) => {
    const [year, month, day] = dateString.split(' ')[0].split('-');
    const date = new Date(year, month - 1, day);
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const monthName = monthNames[date.getMonth()];
    const formattedDate = `${monthName} ${date.getDate()}, ${date.getFullYear()}`;

    return formattedDate;
};

document.querySelectorAll('.date-item').forEach(dateElement => {
    const dateString = dateElement.dataset.date;
    const formattedDate = formatDate(dateString);
    dateElement.innerText = formattedDate;
});
