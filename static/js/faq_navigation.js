document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.faq-nav-btn');
    const sections = document.querySelectorAll('.faq-section');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update buttons
            navButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Update sections
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(button.dataset.target).classList.add('active');
        });
    });
});
