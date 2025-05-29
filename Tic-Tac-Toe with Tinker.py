import tkinter as tk
from tkinter import messagebox

# Initialize main window
window = tk.Tk()
window.title("Tic Tac Toe")

# Current player: X starts first
current_player = "X"

# Create buttons
buttons = [[None for _ in range(3)] for _ in range(3)]

# Function to check for a win or draw
def check_winner():
    # Rows, columns and diagonals
    for i in range(3):
        # Rows
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        # Columns
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    
    # Diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    # Check for draw
    for row in buttons:
        for btn in row:
            if btn["text"] == "":
                return None
    return "Draw"

# Button click handler
def on_click(row, col):
    global current_player

    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        winner = check_winner()

        if winner:
            if winner == "Draw":
                messagebox.showinfo("Tic Tac Toe", "It's a Draw!")
            else:
                messagebox.showinfo("Tic Tac Toe", f"Player {winner} Wins!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"

# Reset game
def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn["text"] = ""

# Create the 3x3 grid of buttons
for i in range(3):
    for j in range(3):
        button = tk.Button(window, text="", width=10, height=4,
                           font=("Helvetica", 24),
                           command=lambda r=i, c=j: on_click(r, c))
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Start the Tkinter event loop
window.mainloop()
