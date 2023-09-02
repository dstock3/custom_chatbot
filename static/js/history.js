document.addEventListener("DOMContentLoaded", function() {
    const dateHead = document.querySelector('.date-head');
    let sortAscending = true;
    
    dateHead.addEventListener('click', function() {
        sortTranscriptsByDate(sortAscending);
        sortAscending = !sortAscending; 
    });
});

function sortTranscriptsByDate(ascending) {
    const transcripts = Array.from(document.querySelectorAll('.search-row'));
    transcripts.sort((a, b) => {
        const dateA = new Date(a.querySelector('.date-item').dataset.date);
        const dateB = new Date(b.querySelector('.date-item').dataset.date);
        return ascending ? dateA - dateB : dateB - dateA;
    });

    const resultsContainer = document.getElementById('historyResults');
    resultsContainer.innerHTML = '';
    transcripts.forEach(transcript => resultsContainer.appendChild(transcript));
}
