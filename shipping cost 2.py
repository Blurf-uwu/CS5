def get_weight_cost():
    """Prompts user for package weight and returns the base shipping cost."""
    weight = float(input("Weight in kg: "))
    if 0 <= weight <= 5:
        return 50.00
    elif 5 < weight <= 10:
        return 100.00
    elif weight > 10:
        return 150.00
    else:
        print("Invalid weight.")
        return None


def get_destination_cost():
    """Prompts user for destination and returns the destination surcharge."""
    destination = input("Domestic or International?: ").capitalize()
    if destination == "International":
        return 7.50
    elif destination == "Domestic":
        return 0.00
    else:
        print("Invalid destination.")
        return None


def apply_priority(cost):
    """Prompts user for priority choice and returns the final adjusted cost."""
    is_priority = input("Is it a priority shipment? (yes/no): ").capitalize()
    if is_priority == "Yes":
        return cost * 1.20
    elif is_priority == "No":
        return cost
    else:
        print("Invalid priority choice.")
        return None


def calculate_shipping_cost():
    """Calculates and returns the total shipping cost, or None on invalid input."""
    weight_cost = get_weight_cost()
    if weight_cost is None:
        return None

    destination_cost = get_destination_cost()
    if destination_cost is None:
        return None

    total = weight_cost + destination_cost

    total = apply_priority(total)
    if total is None:
        return None

    return total


def main():
    """Main loop: runs the shipping cost calculator until the user exits."""
    while True:
        total = calculate_shipping_cost()

        if total is not None:
            print(f"Total shipping cost: PHP {total:.2f}")

        if input("Type 'exit' to quit, or press Enter to continue: ").capitalize() == "Exit":
            print("Thank you for shipping with us!")
            break


main()
