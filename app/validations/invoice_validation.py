class InvoiceValidation:
    """
    Validation layer for Invoice operations
    This validation is executed BEFORE any CRUD logic
    """

    @staticmethod
    def create_invoice_validation(data):
        errors = []

        # Required: customer_id
        if 'customer_id' not in data or not data['customer_id']:
            errors.append("Customer is required")

        # Required: items
        if 'items' not in data or not isinstance(data['items'], list):
            errors.append("Invoice items are required")
        elif len(data['items']) == 0:
            errors.append("Invoice must contain at least one product")

        # Validate each item (detail)
        if 'items' in data and isinstance(data['items'], list):
            for index, item in enumerate(data['items']):

                if 'product_id' not in item or not item['product_id']:
                    errors.append(f"Product ID is required at item {index + 1}")

                if 'quantity' not in item:
                    errors.append(f"Quantity is required at item {index + 1}")
                else:
                    if not isinstance(item['quantity'], int):
                        errors.append(f"Quantity must be an integer at item {index + 1}")
                    elif item['quantity'] <= 0:
                        errors.append(f"Quantity must be greater than zero at item {index + 1}")

        return errors

    @staticmethod
    def update_invoice_validation(data):
        errors = []

        # Only status update allowed
        allowed_status = ['pending', 'paid', 'cancelled']

        if 'status' not in data:
            errors.append("Invoice status is required")
        elif data['status'] not in allowed_status:
            errors.append("Invalid invoice status")

        return errors
