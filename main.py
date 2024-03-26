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
    """
    Calculate winnings based on the symbols matched.
    Loops through each bet line to compare symbols across columns.
    
    :param columns: Resulting symbols from the slot machine spin
    :param lines: Number of lines the user bet on
    :param bet: Bet amount per line
    :param values: Dictionary mapping symbols to their values
    :return: Total winnings and the winning lines
    """
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if symbol != column[line]:
                break  # Stops checking this line if symbols don't match
        else:
            # If all symbols in a line match, calculate winnings
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)  # Line numbers are 1-indexed for user readability
    return winnings, winnings_lines

def get_slot_machine_spin(rows, cols, symbols):
    """
    Generates a slot machine spin by randomly selecting symbols based on their configured frequency.
    
    :param rows: Number of rows in the slot machine
    :param cols: Number of columns in the slot machine
    :param symbols: Dictionary of symbols and their counts in each reel
    :return: A list of columns representing the slot machine's state
    """
    columns = []
    for _ in range(cols):
        column = []
        all_symbols = []
        for symbol, count in symbols.items():
            all_symbols += [symbol] * count
        random.shuffle(all_symbols)
        for _ in range(rows):
            value = random.choice(all_symbols)
            all_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    """
    Prints the state of the slot machine in a user-friendly format.
    
    :param columns: List of columns with their symbols to print
    """
    for row in range(ROWS):
        for i, column in enumerate(columns):
            end_char = " | " if i < len(columns) - 1 else ""
            print(column[row], end=end_char)
        print()  # Newline after each row

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

