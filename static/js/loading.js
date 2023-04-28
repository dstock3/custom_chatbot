document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    document.getElementById('loading-indicator').style.display = 'block';
    document.getElementsByClassName('display')[0].textContent = '🤔';

    const userMessages = document.querySelectorAll('.chat-message.user');
    const assistantMessages = document.querySelectorAll('.chat-message.assist');
    userMessages.forEach(msg => msg.classList.add('message-loading'));
    assistantMessages.forEach(msg => msg.classList.add('message-loading'));

    event.target.submit();
});
