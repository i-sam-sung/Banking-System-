import string

# Global variables
file_name = 'user data.txt'
user_data = {
    "username": [],
    "fullname": [],
    "role": [],
    "password": [],
    "balance": []
}

# Color Scheme
# RED    => "\033[31m",
# GREEN  => "\033[32m",
# YELLOW => "\033[33m",
# PURPLE => "\033[35m",
# WHITE  => "\033[37m",
# CYAN   => "\033[36m",
# BLUE BACKGROUND  => "\033[44m",
# CYAN BACKGROUND   => "\033[46m",

# reset
# RESET  => "\033[0m",

# bold
# BOLD    => "\033[1m"
# BOLD OFF => "\033[22m"

# Print functions with color formatting
def printError(message):
    print("\n" + "\033[31m" + message + "\033[0m")

def printSuccess(message):
    print("\n" + "\033[32m" + message + "\033[0m")

def printTableHeading(message):
    print("\n" + "\033[46m" + message + "\033[0m")

def printQuestion(message):
    print("\033[37m" + "\033[1m" + message + "\033[0m" + "\n")

def printTitle(message):
    print("\n" + "\033[36m" + "\033[1m" + message + "\033[22m" + "\033[0m" + "\n")

def printWithProjectColor(message):
    print("\n" + "\033[35m" + "------" + "\033[1m" + message + "\033[22m" + "------" + "\033[0m")

# Function to get a valid integer input from the user
def integerInput(prompt):
    while True:
        try:
            given_str = input("\033[44m" + prompt + "\033[0m" + " ")
            if not given_str.strip():  # Check for non-empty input
                printError("Input cannot be empty. Please enter a valid option.")
                continue
            converted_int = int(given_str)
            return converted_int
        except ValueError:
            printError("Invalid input. Please enter a number.")

# Function to get a valid string input from the user
def stringInput(prompt):
    while True:
        given_str = input("\033[37m" + prompt + "\033[0m" + " ")
        if not given_str.strip():  # Check for non-empty input
            printError("Input cannot be empty. Please enter a valid option.")
        else:
            return given_str.strip()
        
# Function to read user data from file
def readUserData():
    global user_data
    with open(file_name, 'r') as file:
        lines = file.readlines()
    for i in range(0, len(lines), 6):
        user = lines[i].strip()
        fullname = lines[i + 1].strip() 
        user_role = lines[i + 2].strip()
        passs = lines[i + 3].strip()
        bal = lines[i + 4].strip()
        user_data['username'].append(user)
        user_data['fullname'].append(fullname)
        user_data['role'].append(user_role)
        user_data['password'].append(passs)
        user_data['balance'].append(bal)


# Function to write user data to file
def writeUserData():
    global user_data
    with open(file_name, 'w') as file:
        for i in range(len(user_data["username"])):
            file.write(user_data["username"][i] + '\n')
            file.write(user_data["fullname"][i] + '\n')
            file.write(user_data["role"][i] + '\n')
            file.write(user_data["password"][i] + '\n')
            file.write(user_data["balance"][i] + '\n')
            file.write('\n')

# Function to get a valid choice from a predefined range
def choiceInput(prompt, input_range):
    printQuestion("\nEnter the desired option:")
    print(prompt + "\n")
    choice = integerInput(f"Enter (1-{input_range}):")
    while choice not in range(1, input_range + 1):
        printError(f"Please enter a number between 1 and {input_range}")
        printQuestion("Enter the desired option:")
        print(prompt + "\n")
        choice = integerInput(f"Enter (1-{input_range}):")
    return choice

# Function to append new user data to the file and update the global dictionary
def appendData(username, fullname, role, password):
    global user_data
    user_data["username"].append(username)
    user_data["fullname"].append(fullname)
    user_data["role"].append(role)
    user_data["password"].append(password)
    user_data["balance"].append('0')
    writeUserData()

# Function to delete a user based on username
def deleteUser():
    global user_data
    username = stringInput("Enter the username from above list to delete:")
    while username not in user_data['username']:
        printError("Username does not exist.")
        username = stringInput("Please enter a different username:")

    # Remove user data from the global dictionary
    user_to_delete_index = user_data["username"].index(username)
    user_data["username"].remove(user_data["username"][user_to_delete_index])
    user_data["role"].remove(user_data["role"][user_to_delete_index])
    user_data["password"].remove(user_data["password"][user_to_delete_index])
    user_data["balance"].remove(user_data["balance"][user_to_delete_index])
    user_data["fullname"].remove(user_data["fullname"][user_to_delete_index])
 
    writeUserData()

    printSuccess(f"{username} deleted successfully")


# Function to handle user login
def login():
    global user_data
    print("\n")
    username = stringInput("Enter username:")
    while username not in user_data['username']:
        printError("The provided username does not exist")
        username = stringInput("Enter username:")
    index = user_data['username'].index(username)
    
    role = stringInput("Enter your role (admin|user):")
    while role != user_data['role'][index]:
        printError(f"are you {role}?")
        role = stringInput("Enter your role (admin|user):")
        index = user_data['username'].index(username)
    
    password = stringInput("Enter Password:")
    while password != user_data['password'][index]:
        printError("Incorrect password.")
        password = stringInput("Enter Password:")
    
    printSuccess(f"Login successful! Your current balance is {user_data['balance'][index]}")
    return index

# Function to check if the password is strong
def isNotValidPassword(password):
    if len(password) < 8:
        printError("Password is not 8 characters long")
        return True
    
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        printError("Please include a special character in the password")
        return True
    
    return False

# Function to check if the username is valid
def isNotValidUsername(username):
    global user_data
    if ' ' in username:
        printError("Spaces are not allowed in the username.")
        return True
    if username in user_data['username']:
        printError("Username already exists. Please enter a different username")
        return True
    if not username.islower():
        printError("Uppercase letters are not allowed.")
        return True
    return False

# Function to handle user sign up
def signUp():
    global user_data
    print("\n")
    username = stringInput("Enter your new username:")
    while isNotValidUsername(username):
        username = stringInput("Enter your new username:")

    fullname = stringInput("Enter your full name:")

    role = stringInput("Enter your role (admin|user):")
    while not (role == "admin" or role == "user"):
        printError("Please enter a valid role")
        role = stringInput("Enter your role (admin|user):")
    
    password = stringInput("Enter new password:")
    while isNotValidPassword(password):
        password = stringInput("Enter new password:")
    
    confirm = stringInput("Confirm Password:")
    while password != confirm:
        printError("Password does not match.")
        password = stringInput("Enter password again:")
        confirm = stringInput("Confirm Password:")

    appendData(username, fullname, role, password)
    printSuccess("You are now successfully registered.")

# Function to display user information
def displayInfo(index):
    global user_data
    printTitle("Your Information")
    print("Username: ", user_data["username"][index])
    print("Full Name: ", user_data["fullname"][index])
    print("Balance: ", user_data["balance"][index])
    print("Role: ", user_data["role"][index])

# Function to display user information
def aboutHUBank():
    print("""
        About Us:
        Welcome to HU Bank!

        We’re a passionate team of developers from the LEAP course at our university, dedicated
        to creating a seamless banking experience. Our goal is to simplify financial
        management, making it easier for you to handle your finances with confidence.

        What We Offer:
        Account Management: Effortlessly manage your account details, balance, and transactions.
        Admin Feature: View and Delete users without effort.
        Transactions: Perform deposits, withdrawals, and transfers.
        User-Friendly Interface: Designed with you in mind for a smooth and intuitive experience.
        
        Creators
        This project was developed by:

        - Samee Saqib
        - M. Hasan Shahid
        - Abdullah Naeem
        Thank you for choosing HU Bank!
""")
# Function to display information of all users
def displayInfoOfAllUsers():
    global user_data
    displayTable("No.","Full name", "Username", "Balance", "Role", isTitle=True)
    for i in range(len(user_data["username"])):
        displayTable(i + 1,user_data["fullname"][i], user_data["username"][i], user_data["balance"][i], user_data["role"][i])

# Function to format data in a tabular form
def displayTable(row1, row2, row3, row4,row5, isTitle=False):
    formatted_row = '{:<5} {:<20} {:<15} {:>15} {:>8}'
    if isTitle:
        printTableHeading(formatted_row.format(row1, row2, row3, row4,row5))
    else:
        print(formatted_row.format(row1, row2, row3, row4,row5))

# Function to update the user's balance
def updateAmount(user_index, new_balance, other_user_index=-1, other_user_balance=0):
    global user_data
    user_data['balance'][user_index] = str(new_balance)
    if other_user_index != -1:
        user_data['balance'][other_user_index] = str(other_user_balance)
    writeUserData()

# Function to handle deposit operations
def deposit(user_index):
    deposit_amount = integerInput("Enter deposit amount:")
    if deposit_amount <= 0:
        printError("Invalid deposit amount. Please enter a positive value.")
        return
    current_balance = int(user_data['balance'][user_index])
    new_balance = current_balance + deposit_amount
    updateAmount(user_index, new_balance)
    printSuccess(f"Deposited {deposit_amount}. New balance is {new_balance}.")

# Function to handle withdrawal operations
def withdraw(user_index):
    withdraw_amount = integerInput("Enter withdrawal amount:")
    if withdraw_amount <= 0:
        printError("Invalid withdrawal amount. Please enter a positive value.")
        return
    current_balance = int(user_data['balance'][user_index])
    if withdraw_amount > current_balance:
        printError("Insufficient balance.")
        return
    new_balance = current_balance - withdraw_amount
    updateAmount(user_index, new_balance)
    printSuccess(f"Withdrew {withdraw_amount}. New balance is {new_balance}.")

# Function to handle money transfers between users
def transfer(user_index):
    print("")
    other_user = stringInput("Enter username of the recipient:")
    if other_user not in user_data['username']:
        printError("Recipient username does not exist.")
        return
    other_user_index = user_data['username'].index(other_user)
    transfer_amount = integerInput("Enter transfer amount:")
    if transfer_amount <= 0:
        printError("Invalid transfer amount. Please enter a positive value.")
        return
    current_balance = int(user_data['balance'][user_index])
    if transfer_amount > current_balance:
        printError("Insufficient balance.")
        return
    other_user_balance = int(user_data['balance'][other_user_index])
    new_balance = current_balance - transfer_amount
    new_other_user_balance = other_user_balance + transfer_amount
    updateAmount(user_index, new_balance, other_user_index, new_other_user_balance)
    printSuccess(f"Transferred {transfer_amount} to {other_user}. Your new balance is {new_balance}.")

# Main function to execute the banking system operations
def main():
    global user_data
    # Display project welcome message
    printWithProjectColor("Welcome to HU Bank")

    # Initialize user data by reading from the file
    readUserData()
    try:
        while True:
            selection = choiceInput("1. Log In \n2. Sign Up \n3. About \n4. Exit", 4)
            if selection == 1:
                user_index = login()
            elif selection == 2:
                signUp()
                continue  # Go back to the main loop after sign-up
            elif selection == 3:
                aboutHUBank()
                continue  # Go back to the main loop after about
            elif selection == 4:
                printWithProjectColor("Thank you for using HU Bank")
                exit()

            while user_index != -1:
                command = choiceInput("1. Display Information \n2. Deposit \n3. Withdraw \n4. Transfer \n5. Display All Users Information \n6. Delete User \n7. Exit", 7)
                if command == 1:
                    displayInfo(user_index)
                elif command == 2:
                    deposit(user_index)
                elif command == 3:
                    withdraw(user_index)
                elif command == 4:
                    transfer(user_index)
                elif command == 5:
                    if user_data["role"][user_index] == "admin":
                        displayInfoOfAllUsers()
                    else:
                        printError("You are unauthorized to view such information. Please login as admin.")
                elif command == 6:
                    if user_data["role"][user_index] == "admin":
                        deleteUser()
                    else:
                        printError("You are unauthorized to delete users. Please login as admin.")
                elif command == 7:
                    printWithProjectColor("Thank you for using HU Bank")
                    break
    except KeyboardInterrupt:
        print("\n")
        printWithProjectColor("Thank you for using HU Bank")
        exit()

if __name__ == "__main__":
    main()
