document.addEventListener('DOMContentLoaded', () => {
    const authContainer = document.getElementById('auth-container');
    const goToSignup = document.getElementById('go-to-signup');
    const goToLogin = document.getElementById('go-to-login');

    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    const alertBox = document.getElementById('alert-box');

    function showAlert(message, type) {
        alertBox.textContent = message;
        alertBox.className = `alert ${type}`;
        alertBox.style.display = '';
    }

    const googleLoginBtn = document.getElementById('google-login-btn');
    const googleSignupBtn = document.getElementById('google-signup-btn');

    const handleGoogleAuth = async () => {
        // Google OAuth strict restriction check
        if (window.location.protocol === 'file:') {
            showAlert("Google Login requires a web server (like VS Code Live Server). It cannot run directly from a file:/// path.", "error");
            return;
        }
        const result = await loginWithGoogle();
        if (result && !result.success) {
            showAlert(result.message, 'error');
        }
    };

    if (googleLoginBtn) googleLoginBtn.addEventListener('click', handleGoogleAuth);
    if (googleSignupBtn) googleSignupBtn.addEventListener('click', handleGoogleAuth);

    goToSignup.addEventListener('click', () => {
        authContainer.classList.add('show-signup');
        alertBox.style.display = 'none';
        alertBox.className = 'alert';
    });

    goToLogin.addEventListener('click', () => {
        authContainer.classList.remove('show-signup');
        alertBox.style.display = 'none';
        alertBox.className = 'alert';
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        const result = await authenticateUser(email, password);
        if (result.success) {
            showAlert(result.message, 'success');
            setTimeout(() => {
                // ✅ CHANGED: home.html → index.html
                window.location.href = 'index.html';
            }, 800);
        } else {
            showAlert(result.message, 'error');
        }
    });

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;

        const result = await registerUser(email, password);
        if (result.success) {
            showAlert(result.message, 'success');
            // Auto switch to login
            setTimeout(() => {
                authContainer.classList.remove('show-signup');
                document.getElementById('login-email').value = email;
                document.getElementById('login-password').value = '';
                alertBox.style.display = 'none';
                alertBox.className = 'alert';
            }, 1500);
        } else {
            showAlert(result.message, 'error');
        }
    });
});