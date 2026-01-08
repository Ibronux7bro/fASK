// API Base URL
const API_BASE = 'http://127.0.0.1:5000';

// Store current user info
let currentUser = null;

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Frontend validation
    if (!email || !password) {
        showError("All fields are required");
        return;
    }

    // Show loading
    showError("Logging in...");

    fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(data => {
                throw new Error(data.message || 'Login failed');
            });
        }
        return res.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("user", JSON.stringify(data.user));
            currentUser = data.user;
            
            window.location.href = "/invoices";
        } else {
            showError("Invalid login credentials");
        }
    })
    .catch(error => {
        showError(error.message || "Server error");
    });
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    currentUser = null;
    window.location.href = "/login";
}

function getCurrentUser() {
    if (!currentUser) {
        const userStr = localStorage.getItem("user");
        if (userStr) {
            currentUser = JSON.parse(userStr);
        }
    }
    return currentUser;
}

function getAuthToken() {
    return localStorage.getItem("token");
}

function isAuthenticated() {
    return !!getAuthToken();
}

// Auto-redirect if not authenticated
function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = "/login";
        return false;
    }
    return true;
}

// Make authenticated API calls
function authenticatedFetch(url, options = {}) {
    const token = getAuthToken();
    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };
    
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    
    return fetch(`${API_BASE}${url}`, {
        ...options,
        headers
    });
}

function showError(msg) {
    const errorElement = document.getElementById("error");
    if (errorElement) {
        errorElement.innerText = msg;
        errorElement.style.display = "block";
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorElement.style.display = "none";
        }, 5000);
    }
}

function showSuccess(msg) {
    const successElement = document.getElementById("success");
    if (successElement) {
        successElement.innerText = msg;
        successElement.style.display = "block";
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            successElement.style.display = "none";
        }, 3000);
    }
}
