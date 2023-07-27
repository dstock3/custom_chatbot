document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll(".dropdown-button");

    buttons.forEach(function(button) {
        button.addEventListener("click", function() {
            var content = this.nextElementSibling;
            content.style.display = content.style.display === "none" ? "block" : "none";
        });
    });
});