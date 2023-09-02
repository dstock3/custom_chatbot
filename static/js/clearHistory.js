document.addEventListener('DOMContentLoaded', function() {
    const clearHistoryButton = document.getElementById('clearHistory');

    clearHistoryButton.addEventListener('click', function() {
        fetch('/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Failed to clear history.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
