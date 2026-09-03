def calculate_fare(distance, vehicle_type, is_peak_hour):
    """
    Calculates the estimated fare based on travel distance, vehicle type, 
    and peak hour status. Returns the total fare rounded to 2 decimal places.
    """
    if distance <= 5.00:
        base_fare = 80.00
    elif distance <= 15.00:
        base_fare = 150.00
    else:
        base_fare = 250.00

    vehicle_lower = vehicle_type.lower()
    if vehicle_lower == "sedan":
        surcharge = 0.00
    elif vehicle_lower == "suv":
        surcharge = 50.00
    elif vehicle_lower == "premium":
        surcharge = 100.00

    total_fare = base_fare + surcharge

    if is_peak_hour:
        total_fare *= 1.15

    return round(total_fare, 2)


while True:
    # 1. Distance Input & Validation
    raw_distance = input("Enter the travel distance in km: ")
    if raw_distance.lower() == "exit":
        break
        
    try:
        distance = float(raw_distance)
        if distance < 0:
            print("Error: Distance cannot be negative. Please try again.")
            continue
    except ValueError:
        print("Error: Invalid numeric input for distance. Please enter a number.")
        continue

    # 2. Vehicle Type Input & Validation
    vehicle_input = input("Enter vehicle type ('Sedan', 'SUV', 'Premium'): ")
    if vehicle_input.lower() == "exit":
        break
        
    if vehicle_input.lower() not in ["sedan", "suv", "premium"]:
        print("Error: Invalid vehicle type. Please enter 'Sedan', 'SUV', or 'Premium'.")
        continue

    # 3. Peak Hour Input & Validation
    peak_input = input("Is it peak hour? (Yes/No): ")
    if peak_input.lower() == "exit":
        break
        
    if peak_input.lower() not in ["yes", "no"]:
        print("Error: Invalid input for peak hour. Please enter 'Yes' or 'No'.")
        continue

    # Boolean conversion for peak hour
    is_peak = (peak_input.lower() == "yes")

    # Calculation and Output
    fare = calculate_fare(distance, vehicle_input, is_peak)
    print(f"The total estimated fare is: P{fare:.2f}")

print("[End Program]")