async function deleteUserData(userId) {
    try {
        const response = await fetch('/preferences', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId })
        });

        if (response.ok) {
            window.location.href = '/';
        } else {
            console.error('Failed to delete user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

const confirmPersonaButton = document.querySelector('.confirm-create-button');

async function createPersona() {
    const userId = confirmPersonaButton.getAttribute('data-user-id');
    const personaName = document.getElementById('new-persona-name').value;
    const personaContent = document.getElementById('new-persona-content').value;

    try {
        const response = await fetch('/new_persona', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, persona_name: personaName, persona_description: personaContent })
        });
        
        if (response.ok) {
            window.location.href = '/preferences';
        } else {
            console.error('Failed to create persona');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

if (confirmPersonaButton) {
    confirmPersonaButton.addEventListener('click', function() {
        createPersona(this);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.querySelector('.delete-user-button');
    const deleteModal = document.querySelector('#delete-modal');
    const overlay = document.querySelector('.overlay');

    if (deleteButton) {
        deleteButton.addEventListener('click', () => {
            deleteModal.classList.toggle('is-active');
            overlay.style.display = 'block';
        });
    }

    const confirmDeleteButton = document.querySelector('.confirm-delete-button');
    
    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', () => {
            const userId = deleteButton.getAttribute('data-user-id');
            deleteUserData(userId);
        });
    }

    const cancelDeleteButton = document.querySelector('.cancel-delete-button');
    
    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', () => {
            deleteModal.classList.toggle('is-active');
            overlay.style.display = 'none';
        });
    }

    const successAlert = document.querySelector('.alert-success');

    if (successAlert) {
        const closeButton = successAlert.querySelector('.close-button');
        closeButton.addEventListener('click', () => {
            successAlert.style.display = 'none';
        });
        
        setTimeout(() => {
            successAlert.style.display = 'none';
        }, 5000);
    }

    const personaButton = document.querySelector('.create-persona-button');
    const personaModal = document.querySelector('#persona-modal');

    if (personaButton) {
        personaButton.addEventListener('click', () => {
            personaModal.classList.toggle('is-active');
            overlay.style.display = 'block';
        });
    }

    const cancelPersonaButton = document.querySelector('.cancel-create-button');

    if (cancelPersonaButton) {
        cancelPersonaButton.addEventListener('click', () => {
            personaModal.classList.toggle('is-active');
            overlay.style.display = 'none';
        });
    }

    const confirmPersonaButton = document.querySelector('.confirm-create-button');

    if (confirmPersonaButton) {
        confirmPersonaButton.addEventListener('click', () => {
            const userId = personaButton.getAttribute('data-user-id');
            createPersona(userId);
        });
    }
});

document.querySelector('.custom-dropdown').addEventListener('click', function() {
    let options = this.querySelector('.options-container');
    options.style.display = options.style.display === 'block' ? 'none' : 'block';
});

document.querySelectorAll('.option-item').forEach(function(option) {
    option.addEventListener('click', function() {
        let selected = this.closest('.custom-dropdown').querySelector('.selected-option');
        selected.textContent = this.textContent;
        selected.setAttribute('data-value', this.getAttribute('data-value'));
        document.getElementById('hidden-theme-pref').value = this.getAttribute('data-value');
    });
});







