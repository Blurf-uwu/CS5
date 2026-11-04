def process_message(text: str, shift: int, censored_words: list) -> str:
    """Transforms, censors, and encrypts a message using list processing and ASCII shifts.

    Returns the transformed string.
    """
    code = ""
    
    for word in censored_words:
        word = word.lower()
    if text.lower() in censored_words:
        code = "*"*len(text)
    else:
        for letter in text:
            if letter.isupper():
                code += chr((ord(letter)-65+shift)%26+65)
            elif letter.islower():
                code += chr((ord(letter)-97+shift)%26+97)
            else:
                code+=letter

    return code

while True:
    
    new_msg = list()
    
    msg = input("Enter Message: ")
    if msg == "exit": break
    elif len(msg)==0:
        print("Message cannot be empty. Please enter a valid message.")
        continue
    msg = msg.split()
    
    try:
        shift = (input("Enter shift key: "))
        if shift == "exit": break
        shift = int(shift) 
    except ValueError:
        print("enter a valid integer")
        continue
    
    censored = input("Enter censored words (comma-separated, or Enter for none): ")
    if censored == "exit": break
    censored = censored.split(",")
    
    for word in msg:
        new_msg.append(process_message(word,shift,censored))
        
    print(" ".join(new_msg))

    
