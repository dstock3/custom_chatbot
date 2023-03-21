const copyButtons = Array.from(document.querySelectorAll('.copy'));

copyButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Get the assistant message content
        const parentElement = button.parentElement;
        const assistantMessageContent = parentElement.childNodes[2].textContent.trim();

        // Create a temporary textarea to hold the content
        const tempTextarea = document.createElement('textarea');
        tempTextarea.value = assistantMessageContent;
        document.body.appendChild(tempTextarea);
    
        // Select the content and copy it to the clipboard
        tempTextarea.select();
        document.execCommand('copy');
    
        // Remove the temporary textarea from the DOM
        document.body.removeChild(tempTextarea);
    
        // Show a confirmation message
        button.textContent = '✓';
    });
});


