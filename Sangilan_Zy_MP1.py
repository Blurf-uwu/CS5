while True:
    total_shipping_cost = 0.00
    
    weight = float(input("weight in kg: "))
    if 0<=weight and 5>=weight:
        total_shipping_cost += 50.00
    elif 5 < weight and weight <= 10:
        total_shipping_cost += 100.00
    elif weight > 10:
        total_shipping_cost += 150.00
    else:
        print("invalid weight")
        continue
        
    destination = input("domestic or international?: ").capitalize()
    if (destination == "International"):
        total_shipping_cost += 7.50
    elif (destination == "Domestic"):
        total_shipping_cost += 0.00
    else:
        print("invalid destination")
        continue
    
    is_priority = input("is it a priority shipment? (yes/no): ").capitalize()
    if is_priority == "Yes":
        total_shipping_cost *= 1.20
    elif is_priority == "No":
        total_shipping_cost *= 1
    else:
        print("invalid priority choice")
        continue
    
    print(f'total shipping cost: {total_shipping_cost}')
    
    if input("type exit to exit: ").capitalize() == "Exit":
        print("Thank you for shipping with us!")
        break
    
    
    
        