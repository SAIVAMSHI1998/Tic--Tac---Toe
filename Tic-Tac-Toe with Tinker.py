import tkinter as tk
from tkinter import messagebox
import random
import copy

# Window
window = tk.Tk()
window.title("Tic Tac Toe")

current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]
game_mode = None  # 'single' or 'two'
difficulty = None  # 'easy', 'medium', 'hard'

def select_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.destroy()
    if game_mode == 'single':
        select_difficulty()
    else:
        draw_board()

def select_difficulty():
    global diff_frame
    diff_frame = tk.Frame(window)
    tk.Label(diff_frame, text="Select Difficulty:", font=("Helvetica", 16)).pack(pady=10)
    for level in ['Easy', 'Medium', 'Hard']:
        tk.Button(diff_frame, text=level, width=20, height=2,
                  command=lambda l=level.lower(): set_difficulty(l)).pack(pady=5)
    diff_frame.pack(pady=50)

def set_difficulty(level):
    global difficulty
    difficulty = level
    diff_frame.destroy()
    draw_board()

def draw_board():
    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", width=10, height=4,
                               font=("Helvetica", 24),
                               command=lambda r=i, c=j: on_click(r, c))
            button.grid(row=i, column=j)
            buttons[i][j] = button

def check_winner(board=None):
    board = board or [[btn["text"] for btn in row] for row in buttons]
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    if all(cell != "" for row in board for cell in row):
        return "Draw"
    return None

def on_click(row, col):
    global current_player

    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        winner = check_winner()

        if winner:
            show_result(winner)
            return

        if game_mode == 'two':
            current_player = "O" if current_player == "X" else "X"
        elif game_mode == 'single':
            current_player = "O"
            window.after(500, computer_move)

def computer_move():
    global current_player

    if difficulty == 'easy':
        move = random.choice(get_empty_cells())
    elif difficulty == 'medium':
        move = find_medium_move()
    elif difficulty == 'hard':
        _, move = minimax(get_board_state(), True)

    if move:
        row, col = move
        buttons[row][col]["text"] = current_player
        winner = check_winner()
        if winner:
            show_result(winner)
            return
        current_player = "X"

def get_empty_cells():
    return [(i, j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == ""]

def get_board_state():
    return [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]

def find_medium_move():
    board = get_board_state()
    for player in ["O", "X"]:
        for i, j in get_empty_cells():
            board_copy = copy.deepcopy(board)
            board_copy[i][j] = player
            if check_winner(board_copy) == player:
                return (i, j)
    return random.choice(get_empty_cells())

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return (1, None)
    elif winner == "X":
        return (-1, None)
    elif winner == "Draw":
        return (0, None)

    best_score = -float("inf") if is_maximizing else float("inf")
    best_move = None

    for i, j in [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]:
        board[i][j] = "O" if is_maximizing else "X"
        score, _ = minimax(board, not is_maximizing)
        board[i][j] = ""
        if is_maximizing and score > best_score:
            best_score, best_move = score, (i, j)
        elif not is_maximizing and score < best_score:
            best_score, best_move = score, (i, j)

    return best_score, best_move

def show_result(winner):
    result_win = tk.Toplevel(window)
    result_win.title("Game Over")
    result_win.geometry("250x150")
    result_win.resizable(False, False)

    msg = "It's a Draw!" if winner == "Draw" else f"Player {winner} Wins!"
    tk.Label(result_win, text=msg, font=("Helvetica", 14)).pack(pady=20)

    btn_frame = tk.Frame(result_win)
    btn_frame.pack()

    tk.Button(btn_frame, text="Play Again", width=10, command=lambda: [result_win.destroy(), reset_game()]).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Exit", width=10, command=window.destroy).grid(row=0, column=1, padx=10)

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
