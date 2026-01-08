// Invoice List Frontend Integration
// Connects to existing backend invoice APIs

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!window.api.checkAuth()) {
        return;
    }
    
    loadInvoices();
});

function loadInvoices() {
    window.api.invoices.getAll()
        .then(data => {
            renderInvoiceList(data);
            // Update navigation permissions after loading
            if (typeof updateNavigationPermissions === 'function') {
                updateNavigationPermissions();
            }
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function renderInvoiceList(invoices) {
    const tbody = document.querySelector('.invoice-table tbody');
    if (!tbody) return;
    
    if (invoices.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-state">
                    <i class="fas fa-file-invoice"></i>
                    <p>No invoices found. <a href="/invoices/create">Create your first invoice</a></p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = invoices.map(invoice => `
        <tr>
            <td>${invoice.id}</td>
            <td>${invoice.invoice_date || 'N/A'}</td>
            <td>${invoice.customer_name || 'N/A'}</td>
            <td>$${parseFloat(invoice.total_amount).toFixed(2)}</td>
            <td>
                <a href="/invoices/view/${invoice.id}" class="action-btn btn-view">View</a>
                ${window.api.canUpdate() ? `
                    <a href="/invoices/edit/${invoice.id}" class="action-btn btn-edit">Update</a>
                ` : ''}
                ${window.api.canDelete() ? `
                    <a href="#" class="action-btn btn-delete" onclick="deleteInvoice(${invoice.id})">Delete</a>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function deleteInvoice(invoiceId) {
    if (!confirm('Are you sure you want to delete this invoice?')) {
        return;
    }
    
    // Note: Backend doesn't have DELETE endpoint for invoices in the current routes
    // This would need to be implemented on backend side
    window.api.showError('Delete functionality requires backend implementation');
}

function updateInvoiceStatus(invoiceId, newStatus) {
    if (!window.api.canChangeInvoiceStatus()) {
        window.api.showError('You do not have permission to change invoice status');
        return;
    }
    
    window.api.invoices.updateStatus(invoiceId, newStatus)
        .then(response => {
            window.api.showSuccess(response.message);
            loadInvoices(); // Reload the list
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

// Add status change buttons if user has permission
document.addEventListener('DOMContentLoaded', function() {
    if (window.api.canChangeInvoiceStatus()) {
        // Add status change functionality to invoice rows
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    addStatusChangeButtons();
                }
            });
        });
        
        const tbody = document.querySelector('.invoice-table tbody');
        if (tbody) {
            observer.observe(tbody, { childList: true });
            addStatusChangeButtons();
        }
    }
});

function addStatusChangeButtons() {
    const rows = document.querySelectorAll('.invoice-table tbody tr:not(.empty-state)');
    rows.forEach(row => {
        const actionsCell = row.querySelector('td:last-child');
        if (actionsCell && !actionsCell.querySelector('.action-buttons')) {
            const invoiceId = row.querySelector('td:first-child').textContent;
            const statusCell = row.querySelector('td:nth-child(5)'); // Status column if it exists
            
            // Create action buttons container
            const actionButtons = document.createElement('div');
            actionButtons.className = 'action-buttons';
            
            // View button
            const viewBtn = document.createElement('button');
            viewBtn.className = 'btn-view';
            viewBtn.innerHTML = '<i class="fas fa-eye"></i> View';
            viewBtn.onclick = () => viewInvoice(invoiceId);
            actionButtons.appendChild(viewBtn);
            
            // Edit button
            if (window.api.canUpdate()) {
                const editBtn = document.createElement('button');
                editBtn.className = 'btn-edit';
                editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit';
                editBtn.onclick = () => editInvoice(invoiceId);
                actionButtons.appendChild(editBtn);
            }
            
            // Delete button
            if (window.api.canDelete()) {
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn-delete';
                deleteBtn.innerHTML = '<i class="fas fa-trash"></i> Delete';
                deleteBtn.onclick = () => deleteInvoice(invoiceId);
                actionButtons.appendChild(deleteBtn);
            }
            
            // Status change buttons (if user has permission)
            if (statusCell) {
                const currentStatus = statusCell.textContent.trim();
                const statusButtons = createStatusButtons(invoiceId, currentStatus);
                statusCell.innerHTML = `${currentStatus} ${statusButtons}`;
            }
            
            actionsCell.innerHTML = '';
            actionsCell.appendChild(actionButtons);
        }
    });
}

function viewInvoice(invoiceId) {
    // Use API to get invoice details instead of direct navigation
    window.api.invoices.getById(invoiceId)
        .then(invoice => {
            // Create a modal or redirect with proper authentication
            showInvoiceModal(invoice);
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function showInvoiceModal(invoice) {
    // Create modal to show invoice details
    const modal = document.createElement('div');
    modal.className = 'invoice-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Invoice Details</h3>
                <button class="close-btn" onclick="closeInvoiceModal()">&times;</button>
            </div>
            <div class="modal-body">
                <p><strong>ID:</strong> ${invoice.id}</p>
                <p><strong>Customer:</strong> ${invoice.customer_name || 'N/A'}</p>
                <p><strong>Date:</strong> ${invoice.invoice_date || 'N/A'}</p>
                <p><strong>Status:</strong> <span class="status-${invoice.status}">${invoice.status}</span></p>
                <p><strong>Total:</strong> $${invoice.total_amount || '0.00'}</p>
                ${invoice.items ? `
                    <h4>Items:</h4>
                    <table class="items-table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Quantity</th>
                                <th>Price</th>
                                <th>Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${invoice.items.map(item => `
                                <tr>
                                    <td>${item.product_name || 'N/A'}</td>
                                    <td>${item.quantity || '0'}</td>
                                    <td>$${item.price || '0.00'}</td>
                                    <td>$${item.amount || '0.00'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : '<p>No items found</p>'}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function closeInvoiceModal() {
    const modal = document.querySelector('.invoice-modal');
    if (modal) {
        modal.remove();
    }
}

function editInvoice(invoiceId) {
    // Use API to get invoice details for editing
    window.api.invoices.getById(invoiceId)
        .then(invoice => {
            // Create edit modal or redirect with proper authentication
            showEditModal(invoice);
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function showEditModal(invoice) {
    // Create modal to edit invoice
    const modal = document.createElement('div');
    modal.className = 'invoice-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Edit Invoice</h3>
                <button class="close-btn" onclick="closeEditModal()">&times;</button>
            </div>
            <div class="modal-body">
                <form id="editInvoiceForm">
                    <input type="hidden" id="editInvoiceId" value="${invoice.id}">
                    
                    <div class="form-group">
                        <label for="editCustomer">Customer:</label>
                        <select id="editCustomer" required>
                            <option value="">Select Customer</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="editDate">Invoice Date:</label>
                        <input type="date" id="editDate" value="${invoice.invoice_date || ''}" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="editStatus">Status:</label>
                        <select id="editStatus" ${!window.api.canChangeInvoiceStatus() ? 'disabled' : ''}>
                            <option value="pending" ${invoice.status === 'pending' ? 'selected' : ''}>Pending</option>
                            <option value="paid" ${invoice.status === 'paid' ? 'selected' : ''}>Paid</option>
                            <option value="cancelled" ${invoice.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
                        </select>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn-save">Save Changes</button>
                        <button type="button" class="btn-cancel" onclick="closeEditModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Load customers for the dropdown
    loadCustomersForEdit();
    
    // Add form submit handler
    document.getElementById('editInvoiceForm').addEventListener('submit', handleEditSubmit);
}

function loadCustomersForEdit() {
    window.api.customers.getAll()
        .then(customers => {
            const select = document.getElementById('editCustomer');
            customers.forEach(customer => {
                const option = document.createElement('option');
                option.value = customer.id;
                option.textContent = customer.name;
                select.appendChild(option);
            });
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function handleEditSubmit(event) {
    event.preventDefault();
    
    const invoiceId = document.getElementById('editInvoiceId').value;
    const formData = {
        customer_id: document.getElementById('editCustomer').value,
        invoice_date: document.getElementById('editDate').value,
        status: document.getElementById('editStatus').value
    };
    
    window.api.invoices.update(invoiceId, formData)
        .then(response => {
            window.api.showSuccess('Invoice updated successfully!');
            closeEditModal();
            loadInvoices(); // Reload the list
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function closeEditModal() {
    const modal = document.querySelector('.invoice-modal');
    if (modal) {
        modal.remove();
    }
}

function deleteInvoice(invoiceId) {
    if (confirm('Are you sure you want to delete this invoice?')) {
        window.api.invoices.delete(invoiceId)
            .then(response => {
                window.api.showSuccess('Invoice deleted successfully!');
                loadInvoices(); // Reload the list
            })
            .catch(error => {
                window.api.showError(error.message);
            });
    }
}

function createStatusButtons(invoiceId, currentStatus) {
    if (!window.api.canChangeInvoiceStatus()) {
        return '';
    }
    
    let buttons = '';
    
    if (currentStatus === 'pending') {
        buttons = `
            <span class="status-change">
                <button onclick="updateInvoiceStatus(${invoiceId}, 'paid')" class="btn-status btn-paid">Mark Paid</button>
                <button onclick="updateInvoiceStatus(${invoiceId}, 'cancelled')" class="btn-status btn-cancelled">Cancel</button>
            </span>
        `;
    }
    
    return buttons;
}
