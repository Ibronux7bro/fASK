function validateInvoice(invoiceData) {

    if (!invoiceData.customer_id) {
        return "Customer is required";
    }

    if (!invoiceData.items || invoiceData.items.length === 0) {
        return "Invoice must contain at least one product";
    }

    for (let i = 0; i < invoiceData.items.length; i++) {
        const item = invoiceData.items[i];

        if (!item.product_id) {
            return `Product ID is required at item ${i + 1}`;
        }

        if (!item.quantity || item.quantity <= 0) {
            return `Quantity must be greater than zero at item ${i + 1}`;
        }
    }

    return null; // no errors
}
