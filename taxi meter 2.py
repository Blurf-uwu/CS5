def get_float_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == "end":
            return None
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number or 'end'.")

def get_int_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == "end":
            return None
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer or 'end'.")

def run_taxi_meter():
    while True:
        rounds = get_int_input("enter number of trips or enter 'end' to exit: ")
        
        if rounds is None:
            print("Thank you for riding with us")
            break

        total_time = 0.0
        total_distance = 0.0
        total_fare = 0.0
        actual_trips = 0
        end_early = False
        
        for i in range(1, rounds + 1):
            print(f'Ride no. {i}')

            time = get_float_input("time: ")
            if time is None:
                end_early = True
                break
            
            distance = get_float_input("distance: ")
            if distance is None:
                end_early = True
                break   
            
            fare = 50.0 + (time * 2.0) + (distance * 13.50)
            print(f"Ride no. {i} fare: {fare:.2f}")
            
            total_time += time
            total_distance += distance
            total_fare += fare
            actual_trips += 1
            
        print("==============================")
        print(f'Trip ended. Summary for {actual_trips} trip/s')
        print(f'Total elapsed time: {total_time:.2f}')
        print(f'Total distance traveled: {total_distance:.2f}')
        print(f'Total Fare: {total_fare:.2f}')
        
        if end_early:
            print("Thank you for riding with us")
            break

run_taxi_meter()
