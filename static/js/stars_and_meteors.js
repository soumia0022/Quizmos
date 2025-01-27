function createStars() {
    const starsContainer = document.getElementById('stars-container');
    starsContainer.innerHTML = '';
    
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.animationDelay = `${Math.random() * 2}s`;
        starsContainer.appendChild(star);
    }
}

function createMeteors() {
    const meteorsContainer = document.getElementById('meteors-container');
    meteorsContainer.innerHTML = '';
    
    for (let i = 0; i < 5; i++) {
        const meteor = document.createElement('div');
        meteor.className = 'meteor';
        meteor.style.left = `${Math.random() * 100}%`;
        meteor.style.top = `-100px`;
        meteor.style.animationDuration = `${Math.random() * 2 + 1}s`;
        meteor.style.animationDelay = `${Math.random() * 3}s`;
        meteorsContainer.appendChild(meteor);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    createStars();
    createMeteors();
    
    // Recreate meteors periodically
    setInterval(() => {
        createMeteors();
    }, 5000);
});