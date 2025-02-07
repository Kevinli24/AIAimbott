// script.js
const timerElement = document.getElementById('timer');
const statusElement = document.getElementById('status');
const container = document.getElementById('container');
const catSound = document.getElementById('catSound');
const dogSound = document.getElementById('dogSound');
const volumeControl = document.getElementById('volume');

let currentAnimals = {
    box1: 'cat',
    box2: 'dog'
};

// Volume Control
volumeControl.addEventListener('input', (e) => {
    catSound.volume = e.target.value;
    dogSound.volume = e.target.value;
});

// Image Click Handler
function handleImageClick(event) {
    const clickedBox = event.currentTarget;
    const animalType = currentAnimals[clickedBox.id];
    
    if (animalType === 'cat') {
        catSound.currentTime = 0;
        catSound.play();
        statusElement.textContent = "You clicked a Cat! 🐱";
    } else {
        dogSound.currentTime = 0;
        dogSound.play();
        statusElement.textContent = "You clicked a Dog! 🐶";
    }

    clickedBox.classList.add('correct');
    setTimeout(() => {
        clickedBox.classList.remove('correct');
    }, 500);
}

// Image Management
async function fetchRandomImage(animalType) {
    try {
        const apiUrl = animalType === 'cat' 
            ? 'https://api.thecatapi.com/v1/images/search' 
            : 'https://api.thedogapi.com/v1/images/search';
        const response = await fetch(apiUrl);
        const data = await response.json();
        return data[0].url;
    } catch (error) {
        console.error('Error fetching image:', error);
        return 'fallback.jpg';
    }
}

async function updateImages() {
    // Remove old event listeners
    container.querySelectorAll('.image-box').forEach(box => {
        box.removeEventListener('click', handleImageClick);
    });

    // Random swap logic
    if (Math.random() > 0.5) {
        // Swap animal types first
        const temp = currentAnimals.box1;
        currentAnimals.box1 = currentAnimals.box2;
        currentAnimals.box2 = temp;
        
        // Then swap DOM positions
        container.insertBefore(document.getElementById('box2'), document.getElementById('box1'));
    }

    // Load images based on current animal types
    const box1Image = document.getElementById('box1').querySelector('.animal-image');
    const box2Image = document.getElementById('box2').querySelector('.animal-image');
    
    box1Image.src = await fetchRandomImage(currentAnimals.box1);
    box2Image.src = await fetchRandomImage(currentAnimals.box2);

    // Add new event listeners
    container.querySelectorAll('.image-box').forEach(box => {
        box.addEventListener('click', handleImageClick);
    });
}

// Timer System
function startTimer() {
    let seconds = 10;
    const timerInterval = setInterval(() => {
        timerElement.textContent = `Next refresh in: ${seconds} seconds`;
        seconds--;
        
        if (seconds < 0) {
            clearInterval(timerInterval);
            updateImages();
            startTimer();
        }
    }, 1000);
}

// Initialize
window.addEventListener('DOMContentLoaded', async () => {
    await updateImages();
    startTimer();
});