function fetchPrice(select) {
    const selectedOption = select.options[select.selectedIndex];
    const price = selectedOption.getAttribute('data-price');
    const priceInput = select.closest('tr').querySelector('input[name="price[]"]');

    if (priceInput) {
        priceInput.value = price || 0;
        calculateRow(select);
    }
}

function calculateRow(input) {
    const row = input.closest('tr');
    const quantity = parseFloat(row.querySelector('input[name="quantity[]"]').value) || 0;
    const price = parseFloat(row.querySelector('input[name="price[]"]').value) || 0;
    const totalInput = row.querySelector('input[name="row_total[]"]');

    if (totalInput) {
        const total = quantity * price;
        totalInput.value = total.toFixed(2);
    }

    calculateTotals();
}

function calculateTotals() {
    // Use .product-row to match edit.html
    const rows = document.querySelectorAll('.product-row');
    let subtotal = 0;

    rows.forEach(row => {
        const rowTotal = parseFloat(row.querySelector('input[name="row_total[]"]').value) || 0;
        subtotal += rowTotal;
    });

    // Matches create.html logic (Total Items Amount)
    const grandTotal = subtotal;

    // Update displays
    const totalAmountDisplay = document.getElementById('totalAmountDisplay'); // Master section input
    const grandTotalDisplay = document.getElementById('grandTotalDisplay');   // Footer text
    const totalAmountInput = document.getElementById('totalAmount');          // Hidden input

    if (totalAmountDisplay) totalAmountDisplay.value = grandTotal.toFixed(2);
    if (grandTotalDisplay) grandTotalDisplay.textContent = '$' + grandTotal.toFixed(2);
    if (totalAmountInput) totalAmountInput.value = grandTotal.toFixed(2);
}

function addRow() {
    const tbody = document.querySelector('#detailsTable tbody');
    // Use .product-row
    const firstRow = tbody ? tbody.querySelector('tr.product-row') : null;

    if (!tbody || !firstRow) {
        // Fallback or alert if no rows exist to clone from
        console.warn('No rows to clone');
        return;
    }

    const newRow = firstRow.cloneNode(true);

    const productSelect = newRow.querySelector('select[name="product_id[]"]');
    if (productSelect) {
        productSelect.selectedIndex = 0;
    }

    newRow.querySelectorAll('input').forEach(input => {
        if (input.name === 'quantity[]') {
            input.value = 1;
        } else {
            input.value = '';
        }
    });

    // Clear price if it was set
    const priceInput = newRow.querySelector('input[name="price[]"]');
    if (priceInput) priceInput.value = '';

    tbody.appendChild(newRow);
    calculateTotals();
}

function removeRow(button) {
    const row = button.closest('tr');
    const tbody = row ? row.parentNode : null;

    if (!row || !tbody) {
        return;
    }

    if (tbody.querySelectorAll('tr.product-row').length > 1) {
        row.remove();
        calculateTotals();
    } else {
        alert('At least one product row is required');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    calculateTotals();
});
