// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 70,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Lazy loading for images
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports the native lazy loading
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // If the browser doesn't support lazy loading, load a polyfill
        // This is just a placeholder - in a real implementation you would load a proper polyfill
        console.log('Browser does not support native lazy loading');
    }
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Reading progress bar
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }
    
    // Share buttons
    const shareButtons = document.querySelectorAll('.social-share a');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.open(this.href, 'share-dialog', 'width=626,height=436');
        });
    });
    
    // Search form validation and enhancement
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.classList.add('is-invalid');
                
                // Create error message if it doesn't exist
                let errorMessage = this.querySelector('.invalid-feedback');
                if (!errorMessage) {
                    errorMessage = document.createElement('div');
                    errorMessage.className = 'invalid-feedback';
                    errorMessage.textContent = 'Please enter a search term';
                    searchInput.parentNode.appendChild(errorMessage);
                }
            }
        });
    }
    
    // Comment form character counter
    const commentContent = document.querySelector('textarea[name="content"]');
    if (commentContent) {
        const maxLength = 1000; // Set your max length
        const counterElement = document.createElement('small');
        counterElement.className = 'form-text text-muted character-counter';
        counterElement.textContent = `0/${maxLength} characters`;
        commentContent.parentNode.appendChild(counterElement);
        
        commentContent.addEventListener('input', function() {
            const currentLength = this.value.length;
            counterElement.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength >= maxLength) {
                counterElement.classList.add('text-danger');
            } else {
                counterElement.classList.remove('text-danger');
            }
        });
    }
    
    // Back to top button
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Estimated reading time
    const articleContent = document.querySelector('.article-content');
    const readingTimeElement = document.getElementById('reading-time');
    
    if (articleContent && readingTimeElement) {
        const text = articleContent.textContent;
        const wordCount = text.split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / 200); // Assuming 200 words per minute reading speed
        readingTimeElement.textContent = `${readingTime} min read`;
    }
    
    // Newsletter form validation
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        const emailInput = newsletterForm.querySelector('input[type="email"]');
        
        newsletterForm.addEventListener('submit', function(e) {
            if (!emailInput.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                emailInput.classList.add('is-invalid');
            }
            
            newsletterForm.classList.add('was-validated');
        });
    }
    
    // Dark mode toggle (just a placeholder - would be implemented with user preferences)
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            
            // Save preference to localStorage
            const isDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDarkMode);
        });
        
        // Check for saved preference
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        if (savedDarkMode) {
            document.body.classList.add('dark-mode');
        }
    }
}); 