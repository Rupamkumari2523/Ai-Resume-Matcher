document.addEventListener("DOMContentLoaded", () => {
    // 1. Initial Intro Animation (Removes pre-load state)
    // Add brief delay to ensure styles are parsed before transitions fire
    setTimeout(() => {
        document.body.classList.remove('loading');
    }, 150);

    // 2. Intersection Observer for Scroll Animations
    // Detects when elements scroll into view and triggers their fade-up CSS classes
    const observerOptions = {
        root: null, // use viewport
        rootMargin: '0px',
        threshold: 0.15 // trigger when 15% of element is visible
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add visible class to trigger CSS transform + opacity fade
                entry.target.classList.add('visible');

                // Stop observing once animated (one-time animation)
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Grab all elements tagged for scroll reveal and observe them
    const revealElements = document.querySelectorAll('.fade-up-scroll');
    revealElements.forEach(el => scrollObserver.observe(el));
});
