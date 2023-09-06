const modal = document.getElementById('notesModal');
const span = document.getElementsByClassName('close')[0];

document.getElementById('showNotesModalBtn').addEventListener('click', function(event) {
    event.preventDefault();
    
    fetch('/notes')
        .then(response => response.json())
        .then(data => {
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = ''; 
            
            data.forEach(note => {
                console.log(note);
                const noteItem = document.createElement('div');
                noteItem.className = 'note-item';
                noteItem.innerHTML = `
                    <p class="note-date">${note[4]}</p>
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
