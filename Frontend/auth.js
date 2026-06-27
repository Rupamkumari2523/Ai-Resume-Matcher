// Initialize Supabase Client using centralized config
const supabaseClient = supabase.createClient(API_CONFIG.SUPABASE_URL, API_CONFIG.SUPABASE_ANON_KEY);

async function registerUser(email, password) {
    if (API_CONFIG.SUPABASE_ANON_KEY.includes("PASTE_YOUR") || API_CONFIG.SUPABASE_ANON_KEY.trim() === "") {
        return { success: false, message: "Pehle .env file mein apni API Key paste karein aur Flask server restart karein!" };
    }

    const { data, error } = await supabaseClient.auth.signUp({
        email: email,
        password: password,
    });

    if (error) return { success: false, message: error.message };
    return { success: true, message: "Account created! You can now log in." };
}

async function authenticateUser(email, password) {
    if (API_CONFIG.SUPABASE_ANON_KEY.includes("PASTE_YOUR") || API_CONFIG.SUPABASE_ANON_KEY.trim() === "") {
        return { success: false, message: "Pehle .env file mein apni API Key paste karein aur Flask server restart karein!" };
    }

    const { data, error } = await supabaseClient.auth.signInWithPassword({
        email: email,
        password: password,
    });

    if (error) return { success: false, message: error.message };
    return { success: true, message: "Logged in successfully!" };
}

async function checkAuth() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    if (!session) {
        window.location.replace("login.html");
        return null;
    }

    // Update nav profile text if exists
    const userProfile = document.getElementById('user-profile');
    if (userProfile && session.user.email) {
        const usernameDisplay = userProfile.querySelector('.username');
        const avatarDisplay = userProfile.querySelector('.avatar');
        if (usernameDisplay) usernameDisplay.textContent = session.user.email.split('@')[0];
        if (avatarDisplay) avatarDisplay.textContent = session.user.email.charAt(0).toUpperCase();
    }
    return session.user;
}

async function checkLoginRedirect() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    if (session) {
        // ✅ CHANGED: home.html → index.html
        window.location.replace("index.html");
    }
}

async function logout() {
    await supabaseClient.auth.signOut();
    // ✅ CHANGED: index.html → landing.html
    window.location.replace("landing.html");
}

async function loginWithGoogle() {
    const { data, error } = await supabaseClient.auth.signInWithOAuth({
        provider: 'google',
    });
    if (error) return { success: false, message: error.message };
    return { success: true };
}



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