const modal = document.getElementById('notesModal');
const span = document.getElementsByClassName('close')[0];

document.getElementById('showNotesModalBtn').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent default behavior, though not strictly necessary for a button.
    
    // Fetch notes from the server.
    fetch('/notes')
        .then(response => response.json())
        .then(data => {
            // Assuming 'data' contains the notes, populate the modal with them.
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = ''; // Clear current notes.
            
            data.forEach(note => {
                const noteItem = document.createElement('div');
                noteItem.className = 'note-item';
                noteItem.innerHTML = `
                    <p class="note-date">${note.date_created}</p>
                    <p class="note-content">${note.note_content}</p>
                `;
                notesList.appendChild(noteItem);
            });
            
            // Display the modal.
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
