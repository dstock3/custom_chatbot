const scrollToBottom = () => {
    const chatSection = document.querySelector('.chat-container');
    chatSection.scrollTop = chatSection.scrollHeight;
}
scrollToBottom();