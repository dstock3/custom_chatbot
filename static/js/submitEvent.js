document.querySelector('.chat-input').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        submitFormHandler();
    }
});

function submitFormHandler() {
    const form = document.getElementById('chat-form');

    document.getElementById('loading-indicator').style.display = 'block';
    document.getElementsByClassName('display')[0].textContent = '🤔';

    const userMessages = document.querySelectorAll('.chat-message.user');
    const assistantMessages = document.querySelectorAll('.chat-message.assist');
    userMessages.forEach(msg => msg.classList.add('message-loading'));
    assistantMessages.forEach(msg => msg.classList.add('message-loading'));

    form.submit();
}

document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    submitFormHandler();
});
