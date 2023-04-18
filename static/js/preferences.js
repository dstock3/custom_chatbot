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
    if (deleteButton) {
        deleteButton.addEventListener('click', () => {
            const userId = deleteButton.getAttribute('data-user-id');
            deleteUserData(userId);
        });
    }
});