"""
CAESAR CIPHER 97->122
"""

def cipher(letter, shift):
    """
    This function converts a letter to its caesar cipher based on the shift given
    """
    
    if ord(letter)+shift>122: # condition to account for letters at the end of the alphabet
        return chr(96+(ord(letter)+shift-122))
    elif 97<=ord(letter)<122-shift:
        return chr(ord(letter)+shift)
    else:
        return letter 

message = input("Insert Message: ").lower()
while True:
    try:
        shift = int(input("Shift (1-25): "))
        if shift<1 or shift>25:
            print("Input a valid number")
            continue
        else:
            break
    except ValueError:
        print("Input a valid number")
ciphered = ""

# loop to convert each letter
for letter in message:
    ciphered+=cipher(letter,shift)

#print output
print(ciphered)