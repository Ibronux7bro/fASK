const API_BASE_URL = '/api';
const AUTH_URL = ''; // Backend registers auth routes at root, e.g. /login

const API = {
    // --- Authentication ---
    login: async (email, password) => {
        try {
            const response = await fetch(`${AUTH_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));
                return { success: true, user: data.user };
            } else {
                return { success: false, message: data.message || 'Login failed' };
            }
        } catch (error) {
            console.error('Login Error:', error);
            return { success: false, message: 'Network error occurred' };
        }
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    },

    getToken: () => {
        return localStorage.getItem('access_token');
    },

    getUser: () => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    getCurrentUser: () => {
        return API.getUser();
    },

    isAuthenticated: () => {
        const token = localStorage.getItem('access_token');
        return !!token;
    },

    checkAuth: () => {
        if (!API.isAuthenticated()) {
            window.location.href = '/login';
            return false;
        }
        return true;
    },

    // --- Permissions (Simple role-based for Frontend UI) ---
    hasPermission: (action) => {
        // Simplified check. Backend enforces real security.
        // Actions: 'create', 'update', 'delete'
        const user = API.getUser();
        if (!user) return false;
        if (user.role === 'Admin') return true;
        if (user.role === 'Sales Manager' && action !== 'delete') return true;
        if (user.role === 'Sales Representative' && action === 'read') return true;
        // Default to false for unknown cases
        return false;
    },

    canUpdate: () => {
        const user = API.getUser();
        return user && (user.role === 'Admin' || user.role === 'Sales Manager');
    },

    canDelete: () => {
        const user = API.getUser();
        return user && user.role === 'Admin';
    },

    canChangeInvoiceStatus: () => {
        const user = API.getUser();
        return user && (user.role === 'Admin' || user.role === 'Sales Manager');
    },

    // --- API Request Wrapper ---
    fetch: async (endpoint, options = {}) => {
        const token = localStorage.getItem('access_token');

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(endpoint, config);

            if (response.status === 401) {
                console.warn('Unauthorized access. Redirecting to login.');
                API.logout();
                return null;
            }

            return response;
        } catch (error) {
            console.error('API Request Failed:', error);
            throw error;
        }
    },

    // --- Domain Specific APIs ---
    invoices: {
        getAll: async () => {
            const response = await API.fetch(`${API_BASE_URL}/invoices`);
            if (response.ok) return await response.json();
            throw new Error('Failed to fetch invoices');
        },
        getById: async (id) => {
            const response = await API.fetch(`${API_BASE_URL}/invoices/${id}`);
            if (response.ok) return await response.json();
            throw new Error('Failed to fetch invoice details');
        },
        update: async (id, data) => {
            // Ensure data is clean (remove empty strings if validator hates them)
            // But InvoiceValidator handles 'status' string.
            // Check for numeric fields: customer_id
            if (data.customer_id) data.customer_id = parseInt(data.customer_id);

            const response = await API.fetch(`${API_BASE_URL}/invoices/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to update invoice');
        },
        updateStatus: async (id, status) => {
            const response = await API.fetch(`${API_BASE_URL}/invoices/${id}/status`, {
                method: 'PUT',
                body: JSON.stringify({ status })
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to update status');
        },
        delete: async (id) => {
            const response = await API.fetch(`${API_BASE_URL}/invoices/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to delete invoice');
        }
    },

    customers: {
        getAll: async () => {
            const response = await API.fetch(`${API_BASE_URL}/customers`);
            if (response.ok) return await response.json();
            throw new Error('Failed to fetch customers');
        },
        getById: async (id) => {
            const response = await API.fetch(`${API_BASE_URL}/customers/${id}`);
            if (response.ok) return await response.json();
            throw new Error('Failed to fetch customer details');
        },
        create: async (data) => {
            const response = await API.fetch(`${API_BASE_URL}/customers`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to create customer');
        },
        update: async (id, data) => {
            const response = await API.fetch(`${API_BASE_URL}/customers/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to update customer');
        },
        delete: async (id) => {
            const response = await API.fetch(`${API_BASE_URL}/customers/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) return await response.json();
            const err = await response.json();
            throw new Error(err.message || 'Failed to delete customer');
        }
    },

    products: {
        getAll: async () => {
            const response = await API.fetch(`${API_BASE_URL}/products`);
            if (response.ok) return await response.json();
            throw new Error('Failed to fetch products');
        }
    },

    // --- Helper to show alerts ---
    showAlert: (type, message) => {
        const alertDiv = document.getElementById(type === 'success' ? 'success' : 'error');
        if (alertDiv) {
            alertDiv.textContent = message;
            alertDiv.style.display = 'block';
            setTimeout(() => {
                alertDiv.style.display = 'none';
            }, 3000);
        } else {
            alert(`${type.toUpperCase()}: ${message}`);
        }
    },

    showError: (message) => API.showAlert('error', message),
    showSuccess: (message) => API.showAlert('success', message)
};

// Export globally
window.api = API;

// Auto-check auth on protected pages
if (window.location.pathname !== '/login' && window.location.pathname !== '/' && !API.isAuthenticated()) {
    if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
    }
}
