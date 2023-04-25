const searchHistory = (searchInput) => {
    searchInput = searchInput.trim().toLowerCase();
    const searchRows = document.querySelectorAll('.search-row');
    let noResultsMessage = document.getElementById('no-results-message');
    let resultsFound = false;

    searchRows.forEach(row => {
        const subject = row.querySelector('.subject-item').innerText.toLowerCase();
        const messages = row.querySelector('.msg-item').innerText.toLowerCase();
        const keywords = Array.from(row.querySelectorAll('.keyword-item li')).map(li => li.innerText.toLowerCase());
        const category = row.querySelector('.category-item').innerText.toLowerCase();
        const dateElement = row.querySelector('.date-item');
        const dateString = dateElement.dataset.date;
        const formattedDate = formatDate(dateString).toLowerCase();

        if (subject.includes(searchInput) || messages.includes(searchInput) || keywords.some(keyword => keyword.includes(searchInput)) || formattedDate.includes(searchInput) || category.includes(searchInput)) {
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

document.querySelectorAll('.keyword-item li div').forEach(keywordElement => {
    keywordElement.addEventListener('click', () => {
        const keyword = keywordElement.innerText.trim();
        document.getElementById('search').value = keyword;
        searchHistory(keyword);
    });
});

document.querySelectorAll('.category-item').forEach(categoryElement => {
    categoryElement.addEventListener('click', () => {
        const category = categoryElement.innerText.trim();
        document.getElementById('search').value = category;
        searchHistory(category);
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

document.getElementById('search').addEventListener('input', function (event) {
    const searchInput = event.target.value.trim();

    if (searchInput === '') {
        // If the search input is empty, show all the transcripts
        const searchRows = document.querySelectorAll('.search-row');
        searchRows.forEach(row => {
            row.style.display = '';
        });

        // Remove the 'No results found' message if it exists
        const noResultsMessage = document.getElementById('no-results-message');
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
    }
});
