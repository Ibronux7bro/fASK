// Invoice Create Frontend Integration
// Connects to existing backend APIs for invoice creation

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!window.api.checkAuth()) {
        return;
    }
    
    loadCustomersAndProducts();
    setupFormHandlers();
    
    // Add initial row
    addProductRow();
});

function loadCustomersAndProducts() {
    Promise.all([
        window.api.customers.getAll(),
        window.api.products.getAll()
    ])
    .then(([customers, products]) => {
        populateCustomerSelect(customers);
        populateProductSelect(products);
    })
    .catch(error => {
        window.api.showError(error.message);
    });
}

function populateCustomerSelect(customers) {
    const select = document.getElementById('customer_id');
    if (!select) return;
    
    select.innerHTML = '<option value="">-- Select Customer --</option>' +
        customers.map(customer => `
            <option value="${customer.id}">${customer.name} - ${customer.email}</option>
        `).join('');
}

function populateProductSelect(products) {
    // Store products for later use in new rows
    window.availableProducts = products;
    
    // Populate existing selects (like in the template)
    updateAllProductSelects();
}

function updateAllProductSelects() {
    if (!window.availableProducts) return;
    
    const selects = document.querySelectorAll('select[name="product_id[]"]');
    selects.forEach(select => {
        // Skip if already populated (check if length > 1)
        if (select.options.length > 2) return;
        
        const currentValue = select.value;
        select.innerHTML = '<option value="">-- Select Product --</option>' +
            window.availableProducts.map(product => `
                <option value="${product.id}" data-price="${product.price}" data-quantity="${product.quantity}">
                    ${product.name} - $${parseFloat(product.price).toFixed(2)} (Stock: ${product.quantity})
                </option>
            `).join('');
        if (currentValue) select.value = currentValue;
    });
}

function setupFormHandlers() {
    const form = document.getElementById('invoiceForm');
    if (!form) return;
    
    form.addEventListener('submit', handleFormSubmit);
    
    // Add event listeners for dynamic calculations
    document.addEventListener('change', function(e) {
        if (e.target.matches('select[name="product_id[]"]')) {
            handleProductChange(e.target);
        }
        if (e.target.matches('input[name="quantity[]"]')) {
            calculateRowTotal(e.target);
        }
    });
    
    document.addEventListener('input', function(e) {
        if (e.target.matches('input[name="quantity[]"]')) {
            calculateRowTotal(e.target);
        }
    });
}

function handleProductChange(select) {
    const selectedOption = select.options[select.selectedIndex];
    const row = select.closest('tr');
    const priceInput = row.querySelector('input[name="price[]"]');
    const stockInfo = row.querySelector('.stock-info');
    
    if (selectedOption.value) {
        const price = selectedOption.getAttribute('data-price');
        const stock = selectedOption.getAttribute('data-quantity');
        
        if (priceInput) priceInput.value = parseFloat(price).toFixed(2);
        if (stockInfo) {
            stockInfo.textContent = `Avail: ${stock}`;
            stockInfo.style.color = parseInt(stock) < 10 ? 'var(--danger-color)' : 'var(--text-secondary)';
        }
        
        calculateRowTotal(priceInput);
    } else {
        if (priceInput) priceInput.value = '';
        if (stockInfo) stockInfo.textContent = '';
        calculateRowTotal(priceInput);
    }
}

function calculateRowTotal(input) {
    const row = input.closest('tr');
    const quantity = parseFloat(row.querySelector('input[name="quantity[]"]').value) || 0;
    const price = parseFloat(row.querySelector('input[name="price[]"]').value) || 0;
    const totalInput = row.querySelector('input[name="row_total[]"]');
    
    if (totalInput) {
        totalInput.value = (quantity * price).toFixed(2);
    }
    
    calculateGrandTotal();
}

function calculateGrandTotal() {
    const rows = document.querySelectorAll('.product-rows .product-row');
    let grandTotal = 0;
    
    rows.forEach(row => {
        const total = parseFloat(row.querySelector('input[name="row_total[]"]').value) || 0;
        grandTotal += total;
    });
    
    const totalAmountInput = document.getElementById('totalAmount');
    if (totalAmountInput) {
        totalAmountInput.value = grandTotal.toFixed(2);
    }
    
    // Update display elements
    const grandTotalDisplay = document.getElementById('grandTotalDisplay');
    if (grandTotalDisplay) {
        grandTotalDisplay.textContent = '$' + grandTotal.toFixed(2);
    }
    
    const totalAmountDisplay = document.getElementById('totalAmountDisplay');
    if (totalAmountDisplay) {
        totalAmountDisplay.value = grandTotal.toFixed(2);
    }
}

function validateInventory() {
    const rows = document.querySelectorAll('.product-rows .product-row');
    const inventoryIssues = [];
    
    rows.forEach(row => {
        const productSelect = row.querySelector('select[name="product_id[]"]');
        const quantityInput = row.querySelector('input[name="quantity[]"]');
        
        if (productSelect.value && quantityInput.value) {
            const selectedOption = productSelect.options[productSelect.selectedIndex];
            const availableStock = parseInt(selectedOption.getAttribute('data-quantity'));
            const requestedQuantity = parseInt(quantityInput.value);
            
            if (requestedQuantity > availableStock) {
                const productName = selectedOption.textContent.split(' - ')[0];
                inventoryIssues.push(`${productName}: Requested ${requestedQuantity}, Available ${availableStock}`);
            }
        }
    });
    
    return inventoryIssues;
}

function handleFormSubmit(event) {
    event.preventDefault();
    
    // Validate inventory first
    const inventoryIssues = validateInventory();
    if (inventoryIssues.length > 0) {
        window.api.showError('Insufficient inventory:\n' + inventoryIssues.join('\n'));
        return;
    }
    
    const formData = new FormData(event.target);
    const customer_id = formData.get('customer_id');
    
    if (!customer_id) {
        window.api.showError('Please select a customer');
        return;
    }
    
    // Collect invoice items
    const items = [];
    const rows = document.querySelectorAll('.product-rows .product-row');
    
    rows.forEach(row => {
        const productSelect = row.querySelector('select[name="product_id[]"]');
        const quantityInput = row.querySelector('input[name="quantity[]"]');
        const priceInput = row.querySelector('input[name="price[]"]');
        
        if (productSelect.value && quantityInput.value) {
            items.push({
                product_id: parseInt(productSelect.value),
                quantity: parseInt(quantityInput.value),
                amount: parseFloat(quantityInput.value) * parseFloat(priceInput.value)
            });
        }
    });
    
    if (items.length === 0) {
        window.api.showError('Please add at least one product to the invoice');
        return;
    }
    
    const invoiceData = {
        customer_id: parseInt(customer_id),
        items: items
    };
    
    // Submit to backend
    const saveBtn = document.getElementById('saveBtn');
    const originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    saveBtn.disabled = true;
    
    window.api.invoices.create(invoiceData)
        .then(response => {
            window.api.showSuccess(response.message);
            setTimeout(() => {
                window.location.href = '/invoices';
            }, 1000);
        })
        .catch(error => {
            window.api.showError(error.message);
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        });
}

// Add row functionality
function addProductRow() {
    const template = document.querySelector('.product-row-template');
    const container = document.querySelector('.product-rows');
    
    if (!template || !container) return;
    
    // Clone the TR from TBODY
    const newRow = template.querySelector('tr').cloneNode(true);
    
    // Clear values
    newRow.querySelectorAll('select, input').forEach(field => {
        if (field.type === 'select-one') {
            field.selectedIndex = 0;
        } else {
            if (field.name === 'quantity[]') field.value = 1;
            else field.value = '';
        }
    });
    
    container.appendChild(newRow);
    
    // Populate select if products are loaded
    if (window.availableProducts) {
        const select = newRow.querySelector('select');
        updateAllProductSelects();
    }
}

function removeProductRow(button) {
    const row = button.closest('tr');
    const container = document.querySelector('.product-rows');
    
    if (container.children.length > 1) {
        row.remove();
        calculateGrandTotal();
    } else {
        window.api.showError('At least one product is required');
    }
}
