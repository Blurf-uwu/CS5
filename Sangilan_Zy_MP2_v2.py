def calc_fare(time, dist):
    fare = 50.0 + (time * 2.0) + (distance * 13.50)
    return fare

def get_input(prompt,type):
    while True:
        ans = input(prompt)
        
        if ans.lower() == "end":
            return "end"

        try:
            val = type(ans)
            
            if type == float or type == int:
                if val <= 0:
                    print("error: negative or zero distance or time")
                    continue
            
            return val
        except ValueError:
            print("error: invalid value")

while True:
    rounds = get_input("enter number of trips or enter 'end' to exit: ", int)
    if rounds == "end":
        print("Thank you for riding with us")
        break

    total_time = 0.0
    total_distance = 0     
    total_fare = 0.0
    actual_trips = 0
    enditall = False
    
    for i in range(1, rounds+1):
        print(f'Ride no. {i}')

        time = get_input("time: ", float)
        if time == "end":
            enditall = True
            break
        
        distance = get_input("distance: ", float)
        if distance == "end":
            enditall = True
            break   
        
        fare = calc_fare(time, distance)
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