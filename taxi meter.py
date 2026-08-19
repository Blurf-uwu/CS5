while True:
    rounds = input("enter number of trips or enter 'end' to exit: ")
    if rounds.lower() == "end":
        print("Thank you for riding with us")
        break
    rounds = int(rounds)

    total_time = 0.0
    total_distance = 0     
    total_fare = 0.0
    actual_trips = 0
    enditall = False
    
    for i in range(1, rounds+1):
        print(f'Ride no. {i}')

        time = input("time: ")
        if time.lower() == "end":
            enditall = True
            break
        time = float(time)
        
        distance = input("distance: ")
        if distance.lower() == "end":
            enditall = True
            break   
        distance = float(time)
        
        fare = 50.0 + (time * 2.0) + (distance * 13.50)
        print(f"Ride no. {i} fare: {fare:.2f}")
        
        total_time += time
        total_distance += distance
        total_fare += fare
        actual_trips += 1
        
    print("==============================")
    print(f'Trip ended. Summary for {actual_trips} trip/s')
    print(f'Total elapsed time: {total_time}')
    print(f'Total distance traveled: {total_distance}')
    print(f'Total Fare: {total_fare:.2f}')
    
    if enditall:
        print("Thank you for riding with us")
        break