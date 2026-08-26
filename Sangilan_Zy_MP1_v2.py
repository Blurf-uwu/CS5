def get_weight():
    while True:
        try:
            weight = float(input("Weight in kg: "))
            if weight < 0:
                print("Error: Weight cannot be negative. Please try again.")
            else:
                return weight
        except ValueError:
            print("Error: Please enter a valid number for the weight.")


def calculate_weight_cost(weight):
    if 0 <= weight <= 5:
        return 50.00
    elif 5 < weight <= 10:
        return 100.00
    elif weight > 10:
        return 150.00
    else:
        raise ValueError(f"Unexpected weight value: {weight}")


def get_destination():
    while True:
        destination = input("Domestic or International?: ").strip().capitalize()
        if destination in ("Domestic", "International"):
            return destination
        print("Error: Please enter 'Domestic' or 'International'.")


def calculate_destination_cost(destination):
    if destination == "International":
        return 7.50
    return 0.00


def get_priority():
    while True:
        choice = input("Is it a priority shipment? (yes/no): ").strip().capitalize()
        if choice in ("Yes", "No"):
            return choice == "Yes"
        print("Error: Please enter 'yes' or 'no'.")


def apply_priority_surcharge(cost, is_priority):
    if is_priority:
        return cost * 1.20
    return cost


def calculate_total_shipping_cost():
    weight = get_weight()
    cost = calculate_weight_cost(weight)

    destination = get_destination()
    cost += calculate_destination_cost(destination)

    is_priority = get_priority()
    cost = apply_priority_surcharge(cost, is_priority)

    return cost


def main():
    print("=== Shipping Cost Calculator ===")
    while True:
        try:
            total = calculate_total_shipping_cost()
            print(f"Total Shipping Cost: PHP {total:.2f}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

        again = input("Type 'exit' to quit, or press Enter to calculate again: ").strip().capitalize()
        if again == "Exit":
            print("Thank you for shipping with us!")
            break


main()
