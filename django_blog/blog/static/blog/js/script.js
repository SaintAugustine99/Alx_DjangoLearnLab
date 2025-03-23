// Basic JavaScript for interactivity
document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog JavaScript loaded');
    
    // Example of adding an event listener to all "Read More" buttons
    const readMoreButtons = document.querySelectorAll('.read-more');
    readMoreButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#555';
        });
        
        button.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#333';
        });
    });
});