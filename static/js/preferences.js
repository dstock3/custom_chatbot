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

document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.querySelector('.delete-user-button');
    const deleteModal = document.querySelector('.delete-modal');
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

    const cancelDeleteButton = document.querySelector('.cancel-button');
    
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







