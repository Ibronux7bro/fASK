document.addEventListener('DOMContentLoaded', async () => {
    const customerId = document.getElementById('customer_id')?.value;
    const form = document.getElementById('customerForm');

    // If editing, load data
    if (customerId) {
        try {
            document.querySelector('.btn-save').textContent = 'Loading...';
            const customer = await window.api.customers.getById(customerId);

            document.getElementById('name').value = customer.name || '';
            document.getElementById('email').value = customer.email || '';
            document.getElementById('phone').value = customer.phone || '';
            document.getElementById('mobile').value = customer.mobile || '';
            document.getElementById('address').value = customer.address || '';

            document.querySelector('.btn-save').innerHTML = '<i class="fas fa-save"></i> Save Changes';
        } catch (error) {
            console.error(error);
            window.api.showError('Failed to load customer details');
            document.querySelector('.btn-save').textContent = 'Error';
        }
    }

    // Handle Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btn = document.querySelector('.btn-save');
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

        const data = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            mobile: document.getElementById('mobile')?.value, // Optional
            address: document.getElementById('address').value
        };

        try {
            if (customerId) {
                await window.api.customers.update(customerId, data);
                window.api.showSuccess('Customer updated successfully!');
            } else {
                await window.api.customers.create(data);
                window.api.showSuccess('Customer created successfully!');
            }

            setTimeout(() => {
                window.location.href = '/customers';
            }, 1000);

        } catch (error) {
            console.error(error);
            window.api.showError(error.message);
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    });
});
