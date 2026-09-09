""" 
Adapted from solution to LG 4.3.1 Navigate: 

num_tala=list()
while True:
inp=input(‘Ilagay ang numero:’)
if inp==’done’: break
value=float(inp)
num_tala.append(value)
ave=sum(num_tala)/len(num_tala)
print(‘Average:’,ave)

"""

while True:
    num_tala=list()
    while True: #input loop unit user is done listing numbers
        try:
            inp=input("Maglagay ng numero (fin kung tapos na and list): ")
            if inp.lower()=="fin": 
                break
            value=float(inp)
            num_tala.append(value)
        except ValueError:
            print("invalid input. please try again")
            continue
    try: # to account for user finalizing list without any input
        print(f"Maximum: {max(num_tala)}")
        print(f"Minimum: {min(num_tala)}")
    except ValueError:
        print("please input at least one number")
        continue
    
    # ask if user wants to end or start another instance
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