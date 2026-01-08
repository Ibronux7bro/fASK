// Common frontend functionality
// Handles navigation, authentication checks, and UI updates

document.addEventListener('DOMContentLoaded', function() {
    // Update navigation with user info
    updateNavigation();
    
    // Add logout functionality
    setupLogout();
    
    // Check authentication on protected pages
    checkPageAuthentication();
});

function updateNavigation() {
    const user = window.api.getCurrentUser();
    if (!user) return;
    
    // Add user info to navigation
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const userNav = document.createElement('div');
        userNav.className = 'user-nav';
        userNav.innerHTML = `
            <span class="user-info">
                <i class="fas fa-user"></i>
                ${user.name} (${user.role})
            </span>
            <button onclick="logout()" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i> Logout
            </button>
        `;
        navbar.appendChild(userNav);
    }
    
    // Hide/show navigation items based on role
    updateNavigationPermissions();
}

function updateNavigationPermissions() {
    const user = window.api.getCurrentUser();
    if (!user) return;
    
    // Hide/show create buttons if user doesn't have create permission
    const createButtons = document.querySelectorAll('.btn-create');
    createButtons.forEach(btn => {
        if (window.api.hasPermission('create')) {
            btn.style.display = 'inline-flex';
        } else {
            btn.style.display = 'none';
        }
    });
}

// Call updateNavigationPermissions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    updateNavigationPermissions();
});

function setupLogout() {
    // Logout function is already defined in api.js
    // This is just a placeholder for any additional logout logic
}

function checkPageAuthentication() {
    // Pages that require authentication
    const protectedPages = ['/invoices', '/customers', '/products'];
    const currentPath = window.location.pathname;
    
    const isProtectedPage = protectedPages.some(page => currentPath.startsWith(page));
    const isLoginPage = currentPath === '/login' || currentPath === '/';
    
    if (isProtectedPage && !window.api.isAuthenticated()) {
        window.location.href = '/login';
        return;
    }
    
    if (isLoginPage && window.api.isAuthenticated()) {
        window.location.href = '/invoices';
        return;
    }
}

// Utility function to show loading state
function showLoading(element, text = 'Loading...') {
    if (element) {
        element.disabled = true;
        element.dataset.originalText = element.textContent;
        element.textContent = text;
    }
}

function hideLoading(element) {
    if (element && element.dataset.originalText) {
        element.disabled = false;
        element.textContent = element.dataset.originalText;
        delete element.dataset.originalText;
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Handle API errors globally
window.addEventListener('unhandledrejection', function(event) {
    if (event.reason && event.reason.message) {
        window.api.showError(event.reason.message);
        event.preventDefault();
    }
});

// Add CSS for status buttons and user navigation
const style = document.createElement('style');
style.textContent = `
    .user-nav {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .user-info {
        color: #667eea;
        font-weight: 500;
    }
    
    .logout-btn {
        background: #667eea;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: background 0.3s;
    }
    
    .logout-btn:hover {
        background: #5a6fd8;
    }
    
    .status-change {
        margin-left: 10px;
    }
    
    .btn-status {
        padding: 4px 8px;
        margin: 0 2px;
        border: none;
        border-radius: 3px;
        cursor: pointer;
        font-size: 12px;
        transition: background 0.3s;
    }
    
    .btn-paid {
        background: #28a745;
        color: white;
    }
    
    .btn-paid:hover {
        background: #218838;
    }
    
    .btn-cancelled {
        background: #dc3545;
        color: white;
    }
    
    .btn-cancelled:hover {
        background: #c82333;
    }
    
    .stock-info {
        font-size: 12px;
        color: #666;
        margin-left: 10px;
    }
    
    .product-rows {
        margin-top: 15px;
    }
    
    .product-row {
        margin-bottom: 10px;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #666;
    }
    
    .empty-state i {
        font-size: 48px;
        margin-bottom: 15px;
        color: #ddd;
    }
`;
document.head.appendChild(style);
