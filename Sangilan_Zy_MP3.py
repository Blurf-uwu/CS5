# prices for easier access
COFFEE_PRICE = 120.00
PASTRY_PRICE = 85.50
TEA_PRICE = 90.00

def calculate_subtotal(coffee_count, pastry_count, tea_count):
    """Calculates subtotal cost of ordered items before charges or discounts."""
    return (coffee_count * COFFEE_PRICE) + (pastry_count * PASTRY_PRICE) + (tea_count * TEA_PRICE)

def quantity_validator(prompt):
    """function to validate non-negative integer quantities."""
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("Error: Quantity cannot be negative. Please try again.")
                continue
            return val
        except ValueError:
            print("Error: Invalid number. Please enter an integer.")

while True:
    batch_input = input("Enter number of customer orders or 'end' to finish: ")
    
    if batch_input.lower() == "end":
        print("Thank you for using the KapeTayo POS!")
        break

    try:
        num_orders = int(batch_input)
        if num_orders <= 0:
            print("Error: Number of customer orders must be greater than 0.")
            continue
    except ValueError:
        print("Error: Invalid input. Please enter a valid number or 'end' to finish.")
        continue

    total_sales = 0.0
    customers_served = 0
    
    for customer_num in range(1, num_orders + 1):
        print(f"--- Customer #: {customer_num} ---")
        
        coffee_count = quantity_validator("Enter quantity for Coffee: ")
        pastry_count = quantity_validator("Enter quantity for Pastry: ")
        tea_count = quantity_validator("Enter quantity for Tea: ")
        
        while True:
            discount_input = input("Eligible for Senior/PWD discount? (yes/no): ").lower()
            if discount_input in ["yes", "no"]:
                is_eligible = (discount_input == "yes")
                break
            print("Error: Please enter 'yes' or 'no'.")

        subtotal = calculate_subtotal(coffee_count, pastry_count, tea_count)

        if is_eligible:
            discount = subtotal * 0.20
            grand_total = subtotal - discount
        else:
            service_charge = subtotal * 0.08
            grand_total = subtotal + service_charge

        # Receipt
        print("==================================")
        print(f"RECEIPT for Customer #{customer_num}")
        if coffee_count > 0:
            print(f"Coffee x{coffee_count}: P{coffee_count * COFFEE_PRICE:.2f}")
        if pastry_count > 0:
            print(f"Pastry x{pastry_count}: P{pastry_count * PASTRY_PRICE:.2f}")
        if tea_count > 0:
            print(f"Tea x{tea_count}: P{tea_count * TEA_PRICE:.2f}")
        print("----------------------------------")
        print(f"Subtotal: P{subtotal:.2f}")
        
        if is_eligible:
            print(f"Discount (20%): -P{discount:.2f}")
        else:
            print(f"Service (8%): P{service_charge:.2f}")
            
        print("----------------------------------")
        print(f"GRAND TOTAL: P{grand_total:.2f}")
        print("==================================")

        total_sales += grand_total
        customers_served += 1

    # Batch Summary
    print("==================================")
    print("BATCH SUMMARY")
    print(f"Customers Served: {customers_served}")
    print(f"Total Sales: P{total_sales:.2f}")
    print("==================================")
