import random

# Global constants for game configuration
MAX_LINES = 3  # Max number of lines a user can bet on, impacts game strategy
MAX_BET = 100  # Max bet amount per line, defines the betting range
MIN_BET = 1    # Min bet amount per line, ensures a minimum betting threshold

# Slot machine dimensions
ROWS = 3  # Number of rows in the slot machine, part of the game's visual layout
COLUMNS = 3  # Number of columns, determines the complexity of the game

# Symbol configuration with count per reel, affects game odds
symbol_count = {
    "A": 2,  # Symbol 'A' appears twice in every reel
    "B": 4,  # Symbol 'B' appears four times
    "C": 6,  # Symbol 'C', six times
    "D": 8,  # Symbol 'D', eight times, making it the most common symbol
}

# Value of each symbol, determines the payout
symbol_value = {
    "A": 5,  # Highest value
    "B": 4,
    "C": 3,
    "D": 2,  # Lowest value
}

def check_winnings(columns, lines, bet, values):
    winnings = 0  # Initialize total winnings to zero
    winnings_lines = []  # Initialize a list to keep track of winning lines
    
    # Iterate through each line the player bet on
    for line in range(lines):
        # Get the symbol in the first column of the current line
        symbol = columns[0][line]
        
        # Check if the same symbol is present in all columns of the current line
        for column in columns:
            # If a symbol in the current column does not match, break out of the loop
            if symbol != column[line]:
                break
        else:
            # If all symbols in the line match, calculate winnings
            winnings += values[symbol] * bet  # Add winnings based on the symbol's value and the bet
            winnings_lines.append(line + 1)  # Record the winning line, adjusting for 1-indexing
    
    # Return the total winnings and the list of winning lines
    return winnings, winnings_lines

def get_slot_machine_spin(rows, cols, symbols):
    # Initialize the structure to hold the spin result for each column
    columns = []

    # Loop over each column the slot machine should have
    for _ in range(cols):
        # Initialize an empty list to hold the symbols for the current column
        column = []

        # Create a list that contains all symbols according to their frequency
        all_symbols = []
        for symbol, count in symbols.items():
            all_symbols += [symbol] * count  # Add 'symbol' 'count' times

        # Randomly pick a symbol for each row in the current column
        for _ in range(rows):
            value = random.choice(all_symbols)  # Randomly choose a symbol
            all_symbols.remove(value)  # Remove the chosen symbol to avoid repeat picks within the column
            column.append(value)  # Add the chosen symbol to the current column

        # Once the column is filled with symbols, add it to the 'columns' list
        columns.append(column)

    # Return the result, which is a list of columns, each containing 'rows' number of symbols
    return columns

def print_slot_machine(columns):
    # Iterate through each row to print symbols across columns
    for row in range(len(columns[0])):
        # Initialize a variable to hold the symbols for the current row
        row_symbols = []
        
        # Collect symbols from each column in the current row
        for i, column in enumerate(columns):
            # Append the symbol to the row_symbols list
            row_symbols.append(column[row])
            
            # For all but the last column, add a separator
            if i != len(columns) - 1:
                row_symbols.append(" | ")
        
        # Join all symbols and separators into a single string
        row_str = "".join(row_symbols)
        
        # Print the formatted string representing the current row of the slot machine
        print(row_str)

def deposit():
    """
    Handles user input for depositing money into the slot machine.
    Validates the input to ensure it's a positive integer.
    
    :return: The deposited amount as an integer
    """
    while True:
        amount_str = input("What would you like to deposit? $")
        if amount_str.isdigit():
            amount = int(amount_str)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

def get_number_of_lines():
    """
    Prompts the user to select the number of lines to bet on.
    Ensures the choice is within the allowed range.
    
    :return: Number of lines chosen by the user
    """
    while True:
        lines_str = input(f"Enter the number of lines to bet (1 - {MAX_LINES}): ")
        if lines_str.isdigit():
            lines = int(lines_str)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

def get_bet():
    """
    Asks the user for the bet amount per line.
    Validates that the bet is within the min and max bet range.
    
    :return: The bet amount as an integer
    """
    while True:
        amount_str = input("What would you like to bet on each line? $")
        if amount_str.isdigit():
            amount = int(amount_str)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a number.")

def spin(balance):
    """
    Executes a single spin of the slot machine.
    Calculates the total bet, updates the balance based on winnings, and prints the outcome.
    
    :param balance: Current user balance before the spin
    :return: Net result of the spin (winnings minus total bet)
    """
    lines = get_number_of_lines()
    bet = get_bet()
    total_bet = bet * lines
    if total_bet > balance:
        print(f"You do not have enough to bet that amount, your current balance is ${balance}.")
        return 0
    print(f"You are betting ${bet} on {lines} lines. Total bet is = ${total_bet}.")
    slots = get_slot_machine_spin(ROWS, COLUMNS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines", *winning_lines)
    return winnings - total_bet

def main():
    """
    Main function to run the slot machine game.
    Manages the game loop, including deposits, spins, and quitting.
    """
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit): ")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"You left with ${balance}")

if __name__ == "__main__":
    main()

