const modal = document.getElementById('notesModal');
const span = document.getElementsByClassName('close')[0];

function formatDate(dateString) {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');  
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
}

function fetchNotes() {
    fetch('/notes')
        .then(response => response.json())
        .then(data => {
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = '';

            if (data[0].length == 0) {
                notesList.innerHTML = '<p class="no-notes">No notes found.</p>';
            } else {
                data[0].forEach(note => {
                    let noteContent = `
                        <div class="note-head-container">
                            <p class="note-date">${formatDate(note[4])}</p>
                            <span class="delete-note">&times;</span>
                        </div>
                        <p class="note-content">${note[2]}</p>
                        <div class="note-id">${note[0]}</div>
                    `

                    let tags;
                    try {
                        tags = JSON.parse(note[3]);
                    } catch(e) {
                        const lines = note[3].split('\n');
                        tags = lines.map(line => line.replace(/^"|"$/g, '').trim());
                    }
                
                    const ulElement = document.createElement('ul'); 
                    ulElement.className = 'note-tags';
                
                    for (let i = 0; i < tags.length; i++) {
                        const liElement = document.createElement('li');
                        liElement.className = 'note-tag ' + data[1] + '-accent';  
                        liElement.innerText = tags[i];                   
                        ulElement.appendChild(liElement);                
                    }
                    
                    const noteItem = document.createElement('div');
                    noteItem.className = 'note-item ' + data[1];
                    noteItem.innerHTML = noteContent;
                
                    noteItem.appendChild(ulElement); 
                    notesList.appendChild(noteItem);
                });
            }
            
            modal.style.display = "block";
        })
        .catch(error => {
            console.error('Error fetching notes:', error);
        });
}

document.getElementById('showNotesModalBtn').addEventListener('click', function(event) {
    event.preventDefault();
    fetchNotes();
});

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.querySelector('.notes-list').addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-note')) {
        const noteItem = event.target.parentElement.parentElement;
        const noteId = parseInt(noteItem.querySelector('.note-id').innerText);

        fetch('/notes', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({noteId: noteId})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                fetchNotes();
            } else {
                alert('Error deleting note. Please try again.'); 
            }
        })
        .catch(error => {
            console.error('Error deleting note:', error);
        });
    }
});

function performSearch(tagContent) {
    const allNotes = document.querySelectorAll('.notes-list > div'); 

    allNotes.forEach(note => {
        const tagsInNote = note.querySelectorAll('.note-tag');
        let tagFound = false;
        tagsInNote.forEach(tag => {
            if (tag.innerText === tagContent) {
                tagFound = true;
            }
        });

        if (tagFound) {
            note.style.display = 'block';
        } else {
            note.style.display = 'none';
        }
    });
}

document.querySelector('.notes-list').addEventListener('click', function(event) {
    if (event.target.classList.contains('note-tag')) {
        const tagContent = event.target.innerText;
        performSearch(tagContent);
    }
});

document.querySelector('#notesSearchBtn').addEventListener('click', function() {
    const searchQuery = document.querySelector('#notesSearchInput').value.trim().toLowerCase();
    searchNotes(searchQuery);
});

document.querySelector('#notesSearchInput').addEventListener('input', function() {
    const searchQuery = document.querySelector('#notesSearchInput').value.trim().toLowerCase();
    searchNotes(searchQuery);
});

function searchNotes(query) {
    const allNotes = document.querySelectorAll('.notes-list > div');
    allNotes.forEach(note => {
        if (query && note.innerText.toLowerCase().includes(query)) {
            note.style.display = 'block';
        } else if (!query) {
            note.style.display = 'block';
        } else {
            note.style.display = 'none';
        }
    });
}

