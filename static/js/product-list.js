document.addEventListener('DOMContentLoaded', function () {
    // Check authentication
    if (!window.api.checkAuth()) {
        return;
    }

    loadProducts();
});

function loadProducts() {
    window.api.products.getAll()
        .then(data => {
            renderProductList(data);
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}

function renderProductList(products) {
    const tbody = document.querySelector('.product-table tbody');
    if (!tbody) return;

    if (products.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    <i class="fas fa-box-open"></i>
                    <p>No products found. <a href="/products/create">Add your first product</a></p>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = products.map(product => `
        <tr>
            <td>${product.id}</td>
            <td><strong>${product.name}</strong></td>
            <td>${product.description || 'N/A'}</td>
            <td>$${parseFloat(product.price).toFixed(2)}</td>
            <td>${product.quantity}</td>
            <td>
                ${window.api.canUpdate() ? `
                    <a href="/products/edit/${product.id}" class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </a>
                ` : ''}
                ${window.api.canDelete() ? `
                    <button class="action-btn btn-delete" onclick="deleteProduct(${product.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    window.api.products.delete(productId)
        .then(response => {
            window.api.showSuccess('Product deleted successfully');
            loadProducts();
        })
        .catch(error => {
            window.api.showError(error.message);
        });
}
