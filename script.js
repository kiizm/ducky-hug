/**
 * DuckyHug Website - Main JavaScript
 * Handles book carousel and email form functionality
 */

// ====================================
// Book Carousel Functionality
// ====================================

const booksStack = document.getElementById('booksStack');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const bookCards = document.querySelectorAll('.book-card');

let currentIndex = 0;
const cardHeight = 330; // height + gap
const maxIndex = bookCards.length - 3; // Show 3 books at a time
let autoScrollInterval;
let isPaused = false;

/**
 * Update carousel position and button states
 */
function updateCarousel() {
    const offset = -currentIndex * cardHeight;
    booksStack.style.transform = `translateY(${offset}px)`;
    
    // Update button states
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= maxIndex;
}

/**
 * Move to next slide
 */
function nextSlide() {
    if (currentIndex < maxIndex) {
        currentIndex++;
        updateCarousel();
    } else {
        // Loop back to start
        currentIndex = 0;
        updateCarousel();
    }
}

/**
 * Move to previous slide
 */
function prevSlide() {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
    }
}

/**
 * Start auto-scroll functionality
 */
function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
        if (!isPaused) {
            nextSlide();
        }
    }, 5000); // Scroll every 4 seconds
}

/**
 * Stop auto-scroll
 */
function stopAutoScroll() {
    clearInterval(autoScrollInterval);
}

// Event listeners for carousel controls
nextBtn.addEventListener('click', () => {
    stopAutoScroll();
    nextSlide();
    startAutoScroll();
});

prevBtn.addEventListener('click', () => {
    stopAutoScroll();
    prevSlide();
    startAutoScroll();
});

// Pause auto-scroll on hover
booksStack.addEventListener('mouseenter', () => {
    isPaused = true;
});

booksStack.addEventListener('mouseleave', () => {
    isPaused = false;
});

// Start auto-scroll on page load (only on desktop)
if (window.innerWidth >= 1280) {
    startAutoScroll();
}

// ====================================
// Email Form Handling
// ====================================

const emailForm = document.getElementById('emailForm');
const formMessage = document.getElementById('formMessage');

emailForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const emailInput = this.querySelector('.email-input');
    const email = emailInput.value;

    // ========================================
    // INTEGRATE YOUR EMAIL SERVICE HERE
    // ========================================
    
    // Example for ConvertKit:
    /*
    fetch('https://api.convertkit.com/v3/forms/YOUR_FORM_ID/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            api_key: 'YOUR_PUBLIC_API_KEY',
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        // Show success message
        formMessage.style.display = 'block';
        formMessage.textContent = '🎉 Welcome to the Story Circle! Check your inbox for a special welcome message.';
        formMessage.style.color = '#2B5F6F';
        emailInput.value = '';
    })
    .catch(error => {
        // Show error message
        formMessage.style.display = 'block';
        formMessage.textContent = '❌ Oops! Something went wrong. Please try again.';
        formMessage.style.color = '#D32F2F';
    });
    */

    // Example for Mailchimp:
    /*
    fetch('YOUR_MAILCHIMP_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email_address: email,
            status: 'subscribed'
        })
    })
    .then(response => response.json())
    .then(data => {
        formMessage.style.display = 'block';
        formMessage.textContent = '🎉 Welcome to the Story Circle! Check your inbox for a special welcome message.';
        formMessage.style.color = '#2B5F6F';
        emailInput.value = '';
    })
    .catch(error => {
        formMessage.style.display = 'block';
        formMessage.textContent = '❌ Oops! Something went wrong. Please try again.';
        formMessage.style.color = '#D32F2F';
    });
    */

    // Temporary success message (remove when integrating real service)
    formMessage.style.display = 'block';
    formMessage.textContent = '🎉 Welcome to the Story Circle! Check your inbox for a special welcome message.';
    formMessage.style.color = '#2B5F6F';
    
    // Clear the input
    emailInput.value = '';

    // Hide message after 5 seconds
    setTimeout(() => {
        formMessage.style.display = 'none';
    }, 5000);
});

// ====================================
// Utility Functions
// ====================================

/**
 * Handle window resize events
 */
window.addEventListener('resize', () => {
    // Restart auto-scroll only on desktop
    if (window.innerWidth >= 1280 && !autoScrollInterval) {
        startAutoScroll();
    } else if (window.innerWidth < 1280) {
        stopAutoScroll();
    }
});
