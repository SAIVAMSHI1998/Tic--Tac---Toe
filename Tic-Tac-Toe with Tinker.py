import tkinter as tk
from tkinter import messagebox
import random

# Main window
window = tk.Tk()
window.title("Tic Tac Toe")

# Globals
current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]
game_mode = None  # 'single' or 'two'

def select_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.destroy()
    draw_board()

def draw_board():
    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", width=10, height=4,
                               font=("Helvetica", 24),
                               command=lambda r=i, c=j: on_click(r, c))
            button.grid(row=i, column=j)
            buttons[i][j] = button

def check_winner():
    for i in range(3):
        # Check rows
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        # Check columns
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    
    # Check diagonals
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
            return

        if game_mode == 'two':
            current_player = "O" if current_player == "X" else "X"
        elif game_mode == 'single':
            current_player = "O"
            window.after(500, computer_move)

def computer_move():
    global current_player
    empty_cells = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        buttons[row][col]["text"] = current_player

        winner = check_winner()
        if winner:
            if winner == "Draw":
                messagebox.showinfo("Tic Tac Toe", "It's a Draw!")
            else:
                messagebox.showinfo("Tic Tac Toe", f"Player {winner} Wins!")
            reset_game()
            return
        current_player = "X"

def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            if btn:
                btn.destroy()
    draw_board()

# --- Mode selection UI ---
mode_frame = tk.Frame(window)
tk.Label(mode_frame, text="Choose Game Mode:", font=("Helvetica", 16)).pack(pady=10)
tk.Button(mode_frame, text="Single Player", width=20, height=2,
          command=lambda: select_mode('single')).pack(pady=5)
tk.Button(mode_frame, text="Two Player", width=20, height=2,
          command=lambda: select_mode('two')).pack(pady=5)
mode_frame.pack(pady=50)

# Start GUI
window.mainloop()
