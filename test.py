num_tala=list()
while True:
    while True:
        try:
            inp=input("Ilagay ang numero (done kung tapos na and list): ")
            if inp=="done": 
                break
            value=float(inp)
            num_tala.append(value)
        except ValueError:
            print("invalid input. please try again")
            continue

    ave=sum(num_tala)/len(num_tala)
    print("Average: ",ave)
    
    while True:
        try:
            tapos_na = input("Nais mo na bang huminto (y/n)? ").lower()
            if tapos_na == "y":
                break
            elif tapos_na == "n": 
                break
        except ValueError:
            print("invalid input. please try again")
            continue
    if tapos_na == "y": break