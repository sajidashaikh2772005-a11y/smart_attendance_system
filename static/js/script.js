document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll("a.btn");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.style.opacity = "0.7";
        });
    });
});
