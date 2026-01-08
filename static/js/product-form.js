document.addEventListener('DOMContentLoaded', function () {
    // Check authentication
    if (!window.api.checkAuth()) {
        return;
    }

    const form = document.getElementById('productForm');
    if (form) {
        // Handle form submission
        form.addEventListener('submit', handleProductSubmit);

        // If in edit mode (productId exists), fetch data
        const productId = document.getElementById('productId')?.value;
        if (productId) {
            loadProductData(productId);
        }
    }
});

function loadProductData(id) {
    // Show some loading indicator if needed
    window.api.products.getById(id)
        .then(product => {
            document.getElementById('name').value = product.name;
            document.getElementById('description').value = product.description || '';
            document.getElementById('price').value = product.price;
            document.getElementById('stock_quantity').value = product.quantity;
        })
        .catch(error => {
            window.api.showError('Failed to load product: ' + error.message);
        });
}

function handleProductSubmit(event) {
    event.preventDefault();

    // Validate inputs
    const name = document.getElementById('name').value.trim();
    const price = document.getElementById('price').value;
    const quantity = document.getElementById('stock_quantity').value || 0;

    if (!name || !price) {
        window.api.showError('Please fill in all required fields');
        return;
    }

    const startBtn = document.querySelector('.btn-save');
    const originalText = startBtn.innerHTML;
    startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    startBtn.disabled = true;

    const data = {
        name: name,
        description: document.getElementById('description').value.trim(),
        price: parseFloat(price),
        stock_quantity: parseInt(quantity)
    };

    const productId = document.getElementById('productId')?.value;
    let promise;

    if (productId) {
        // Update existing
        promise = window.api.products.update(productId, data);
    } else {
        // Create new
        promise = window.api.products.create(data);
    }

    promise
        .then(response => {
            window.api.showSuccess('Product saved successfully!');
            setTimeout(() => {
                window.location.href = '/products';
            }, 1000);
        })
        .catch(error => {
            window.api.showError(error.message);
            startBtn.innerHTML = originalText;
            startBtn.disabled = false;
        });
}
