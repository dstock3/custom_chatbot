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
            const notesList = document.querySelector('.notes-list');
            notesList.innerHTML = ''; 

            data[0].forEach(note => {
                let noteContent = `
                    <p class="note-date">${formatDate(note[4])}</p>
                    <p class="note-content">${note[2]}</p>
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
                    console.log(tags[i]);
                    
                    const liElement = document.createElement('li');
                    liElement.className = 'note-tag ' + data[1] + '-accent';;  
                    liElement.innerText = tags[i];                   
                    ulElement.appendChild(liElement);                
                }
                
                const noteItem = document.createElement('div');
                noteItem.className = 'note-item ' + data[1];
                noteItem.innerHTML = noteContent;
            
                noteItem.appendChild(ulElement); 
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
