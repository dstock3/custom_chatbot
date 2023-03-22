const copyButtons = Array.from(document.querySelectorAll('.copy'));

copyButtons.forEach(button => {
    button.addEventListener('click', function() {
        const messageElement = this.parentElement;
        const span = messageElement.querySelector('span');
        const button = this;
        const feedback = messageElement.querySelector('.copy-feedback');
        const textToCopy = messageElement.textContent.replace(span.textContent, '').replace(button.textContent, '').replace(feedback.textContent, '').trim();

        const textArea = document.createElement('textarea');
        textArea.value = textToCopy;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        const messageSpan = messageElement.querySelector('.copy-feedback');
        messageSpan.classList.add('visible');
        setTimeout(() => {
            messageSpan.classList.remove('visible');
        }, 2000);
        
        button.textContent = '✓';

    });
});


