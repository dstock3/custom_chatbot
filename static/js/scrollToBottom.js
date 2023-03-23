const scrollToBottom = () => {
    const chatSection = document.querySelector('.chat-section');
    chatSection.scrollTop = chatSection.scrollHeight;
}
scrollToBottom();