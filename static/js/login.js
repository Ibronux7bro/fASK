function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleBtn = document.querySelector(".toggle-password i");

    if (!passwordInput || !toggleBtn) {
        return;
    }

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleBtn.classList.remove("fa-eye");
        toggleBtn.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        toggleBtn.classList.remove("fa-eye-slash");
        toggleBtn.classList.add("fa-eye");
    }
}

function handleLogin(event) {
    event.preventDefault();

    // Check if API is available
    if (typeof window.api === 'undefined') {
        console.error('API module not loaded');
        window.api.showError('Authentication system not ready. Please refresh the page.');
        return;
    }

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Show loading state
    const submitBtn = document.querySelector(".login-btn");
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Logging in...</span>';
    submitBtn.disabled = true;

    // Use new API for login
    window.api.auth.login(email, password)
        .then(response => {
            // Store token and user info
            window.api.setAuthToken(response.access_token);
            window.api.setCurrentUser(response.user);

            // Redirect to invoices page
            window.location.href = "/invoices";
        })
        .catch(error => {
            // Show error and reset button
            console.error('Login error:', error);
            window.api.showError(error.message || 'Login failed. Please try again.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
}

document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    if (emailInput) {
        emailInput.focus();
    }

    // Check if user is already logged in
    try {
        if (typeof window.api !== 'undefined' && window.api && window.api.isAuthenticated && window.api.isAuthenticated()) {
            window.location.href = "/invoices";
            return;
        }
    } catch (error) {
        console.error('Error checking authentication:', error);
    }

    document.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const form = document.getElementById("loginForm");
            if (form) {
                handleLogin(e);
            }
        }
    });
});
