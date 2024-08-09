import string

def is_valid_password(password):
    if len(password) < 8:
        return False
    
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        return False
    
    return True

while True:
    user_password = input("Enter your password: ")
    
    if is_valid_password(user_password):
        # add confirm password code here as well the adments we did in our file.
        break  
    else:
        print("Password is invalid. Make sure it's at least 8 characters long and contains a special character.")