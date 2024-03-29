document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".dropdown-button");

    buttons.forEach(function(button) {
        button.addEventListener("click", function() {
            const content = this.nextElementSibling;
            if (!content.style.display) {
                content.style.display = "none";
            }
            content.style.display = content.style.display === "none" ? "block" : "none";
        });
    });
});