// ================= CREATE SEED DATA =================
function createSeedData() {
    fetch("http://127.0.0.1:5000/api/seed", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            showMessage(data.message, "success");
            loadInvoices();
        } else if (data.error) {
            showMessage(data.error, "error");
        }
    })
    .catch(error => {
        console.error('Seed error:', error);
        showMessage("Failed to create test data", "error");
    });
}

// ================= LOGOUT =================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
}

// ================= TOKEN VALIDATION =================
function validateToken(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        // Check if token has old format (object subject) vs new format (string subject)
        if (typeof payload.sub === 'object') {
            console.log("Old token format detected, clearing token");
            localStorage.removeItem("token");
            window.location.href = "/login";
            return false;
        }
        return true;
    } catch (e) {
        console.log("Invalid token detected");
        localStorage.removeItem("token");
        window.location.href = "/login";
        return false;
    }
}

// ================= READ =================
function loadInvoices() {
    const token = localStorage.getItem("token");
    
    console.log("Token from localStorage:", token);
    
    if (!token) {
        console.log("No token found, redirecting to login");
        window.location.href = "/login";
        return;
    }
    
    // Validate token format
    if (!validateToken(token)) {
        return;
    }
    
    console.log("Making request with Authorization header:", "Bearer " + token);
    
    fetch("http://127.0.0.1:5000/api/invoices", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (res.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
        }
        if (!res.ok) {
            return res.json().then(err => {
                throw new Error(err.message || 'Unauthorized');
            });
        }
        return res.json();
    })
    .then(data => {
        console.log("Success! Data received:", data);
        const tableBody = document.getElementById("invoiceTableBody");
        const noDataMessage = document.getElementById("noDataMessage");
        
        // Clear existing content
        tableBody.innerHTML = "";
        
        if (data.length === 0) {
            noDataMessage.classList.remove("hidden");
            updateStatistics(0, 0, 0, 0);
            return;
        }
        
        noDataMessage.classList.add("hidden");
        
        let totalAmount = 0;
        let paidCount = 0;
        let pendingCount = 0;
        
        data.forEach(inv => {
            const row = document.createElement("tr");
            
            // Status badge class
            let statusClass = "status-pending";
            if (inv.status === "paid") {
                statusClass = "status-paid";
                paidCount++;
            } else if (inv.status === "cancelled") {
                statusClass = "status-cancelled";
            } else {
                pendingCount++;
            }
            
            totalAmount += inv.total_amount || 0;
            
            row.innerHTML = `
                <td>#${inv.id}</td>
                <td>Customer ${inv.customer_id}</td>
                <td>$${(inv.total_amount || 0).toFixed(2)}</td>
                <td><span class="status-badge ${statusClass}">${inv.status}</span></td>
                <td>
                    <div class="action-buttons-cell">
                        <button onclick="showEditModal(${inv.id}, '${inv.status}')" class="btn btn-sm btn-edit">
                            <i class="fas fa-edit"></i>
                            Edit
                        </button>
                        <button onclick="deleteInvoice(${inv.id})" class="btn btn-sm btn-delete">
                            <i class="fas fa-trash"></i>
                            Delete
                        </button>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
        
        // Update statistics
        updateStatistics(data.length, paidCount, pendingCount, totalAmount);
    })
    .catch(error => {
        console.error("Fetch error:", error);
        document.getElementById("error").innerText = "Failed to load invoices: " + error.message;
    });
}

// ================= UPDATE STATISTICS =================
function updateStatistics(total, paid, pending, amount) {
    document.getElementById("totalInvoices").textContent = total;
    document.getElementById("paidInvoices").textContent = paid;
    document.getElementById("pendingInvoices").textContent = pending;
    document.getElementById("totalAmount").textContent = "$" + amount.toFixed(2);
}

// ================= CREATE =================
function createInvoice(event) {
    event.preventDefault(); // Prevent form submission
    
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "/login";
        return;
    }
    
    const customerId = document.getElementById("customerId").value;
    const status = document.getElementById("status").value;
    
    if (!customerId) {
        showMessage("Customer ID is required", "error");
        return;
    }
    
    const invoiceData = {
        customer_id: parseInt(customerId),
        status: status || 'pending',
        items: [
            {
                product_id: 1,
                quantity: 1
            }
        ]
    };

    const error = validateInvoice(invoiceData);
    if (error) {
        showMessage(error, "error");
        return;
    }

    fetch("http://127.0.0.1:5000/api/invoices", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(invoiceData)
    })
    .then(res => {
        if (res.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
        }
        if (res.status === 400) {
            // Validation error - likely customer or product not found
            return res.json().then(err => {
                throw new Error(err.error || err.errors?.join(', ') || 'Invalid input data');
            });
        }
        if (!res.ok) {
            // Try to get error message from response
            return res.text().then(text => {
                try {
                    const err = JSON.parse(text);
                    throw new Error(err.message || err.error || 'Failed to create invoice');
                } catch (e) {
                    // If it's not JSON, it's probably HTML error page
                    throw new Error('Server error: ' + text.substring(0, 100) + '...');
                }
            });
        }
        return res.json();
    })
    .then(() => {
        showMessage("Invoice created successfully!", "success");
        
        // Clear the form
        document.getElementById("customerId").value = "";
        document.getElementById("status").value = "pending";
        
        // Refresh the invoice list to show the new invoice
        loadInvoices();
        
        // Update statistics
        updateStatistics();
    })
    .catch(error => {
        console.error('Create error:', error);
        showMessage("Failed to create invoice", "error");
    });
}

// ================= UPDATE =================
function updateInvoice(event) {
    event.preventDefault(); // Prevent form submission
    
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "/login";
        return;
    }
    
    const invoiceId = document.getElementById("updateInvoiceId").value;
    const status = document.getElementById("updateStatus").value;
    
    if (!invoiceId) {
        showMessage("Invoice ID is required", "error");
        return;
    }
    
    if (!status) {
        showMessage("Status is required", "error");
        return;
    }
    
    fetch(`http://127.0.0.1:5000/api/invoices/${invoiceId}`, {
        method: "PUT",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status })
    })
    .then(res => {
        if (res.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
        }
        if (res.status === 404) {
            throw new Error('Invoice not found. Please check the invoice ID.');
        }
        if (!res.ok) {
            return res.json().then(err => {
                throw new Error(err.message || 'Failed to update invoice');
            });
        }
        return res.json();
    })
    .then(() => {
        showMessage("Invoice updated successfully", "success");
        hideEditModal();
        loadInvoices();
    })
    .catch(error => {
        console.error('Update error:', error);
        showMessage("Failed to update invoice", "error");
    });
}

// ================= DELETE =================
function deleteInvoice(id) {
    const token = localStorage.getItem("token");
    
    if (!token) {
        window.location.href = "/login";
        return;
    }
    
    // Show confirmation dialog
    if (!confirm("Are you sure you want to delete this invoice?")) {
        return;
    }
    
    fetch(`http://127.0.0.1:5000/api/invoices/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (res.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
        }
        if (res.status === 404) {
            throw new Error('Invoice not found. It may have been already deleted.');
        }
        if (!res.ok) {
            throw new Error('Failed to delete invoice');
        }
        return res.json();
    })
    .then(() => {
        showMessage("Invoice deleted successfully", "success");
        loadInvoices();
    })
    .catch(error => {
        console.error('Delete error:', error);
        showMessage("Failed to delete invoice", "error");
    });
}

// ================= EDIT MODAL =================
function showEditModal(invoiceId, currentStatus) {
    const modal = document.getElementById("updateModal");
    const invoiceIdInput = document.getElementById("updateInvoiceId");
    const statusSelect = document.getElementById("updateStatus");
    
    invoiceIdInput.value = invoiceId;
    statusSelect.value = currentStatus;
    
    modal.classList.remove("hidden");
}

function hideEditModal() {
    const modal = document.getElementById("updateModal");
    if (modal) {
        modal.classList.add("hidden");
    }
}

function hideUpdateModal() {
    const modal = document.getElementById("updateModal");
    if (modal) {
        modal.classList.add("hidden");
    }
}

// ================= CREATE MODAL =================
function showCreateModal() {
    document.getElementById("createModal").classList.remove("hidden");
}

function hideCreateModal() {
    const modal = document.getElementById("createModal");
    if (modal) {
        modal.classList.add("hidden");
        // Reset form
        const form = document.getElementById("createInvoiceForm");
        if (form) {
            form.reset();
        }
    }
}

// ================= MESSAGE DISPLAY =================
function showMessage(message, type) {
    const successMsg = document.getElementById("successMessage");
    const errorMsg = document.getElementById("errorMessage");
    const successText = document.getElementById("successText");
    const errorText = document.getElementById("errorText");
    
    // Hide both messages first
    successMsg.classList.add("hidden");
    errorMsg.classList.add("hidden");
    
    if (type === "success") {
        successText.textContent = message;
        successMsg.classList.remove("hidden");
    } else {
        errorText.textContent = message;
        errorMsg.classList.remove("hidden");
    }
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        successMsg.classList.add("hidden");
        errorMsg.classList.add("hidden");
    }, 3000);
}
