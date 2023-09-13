const modal = document.getElementById('notesModal');
const span = document.getElementsByClassName('close')[0];

function formatDate(dateString) {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');  
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
}

document.getElementById('showNotesModalBtn').addEventListener('click', function(event) {
    event.preventDefault();
    
    fetch('/notes')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = ''; 

            data[0].forEach(note => {
                const noteItem = document.createElement('div');
                noteItem.className = 'note-item ' + data[1];
                noteItem.innerHTML = `
                    <p class="note-date">${formatDate(note[4])}</p>
                    <p class="note-content">${note[2]}</p>
                `;
                notesList.appendChild(noteItem);
            });
            
            modal.style.display = "block";
        })
        .catch(error => {
            console.error('Error fetching notes:', error);
        });
});

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
