#include <stdio.h>
import tkinter as tk
from tkinter import messagebox
import random
import copy
import os

# --- Themes ---
themes = {
    "light": {"bg": "#ffffff", "fg": "#000000", "btn_bg": "#f0f0f0", "btn_fg": "#000000"},
    "dark": {"bg": "#2b2b2b", "fg": "#ffffff", "btn_bg": "#444444", "btn_fg": "#ffffff"}
}
current_theme = "light"

# --- Game Variables ---
player_names = {"X": "Player X", "O": "Player O"}
scores = {"X": 0, "O": 0, "Draw": 0}
current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]
SAVE_FILE = "scores.txt"
game_mode = None
difficulty = None

# --- Theme Helpers ---
def apply_theme_to_widget(widget, theme):
    try:
        widget.configure(bg=theme["bg"])
        if "fg" in widget.config():
            widget.configure(fg=theme["fg"])
        if widget.winfo_class() == "Button":
            widget.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
    except:
        pass
    for child in widget.winfo_children():
        apply_theme_to_widget(child, theme)

def apply_theme(theme_name):
    theme = themes[theme_name]
    window.configure(bg=theme["bg"])
    for widget in window.winfo_children():
        apply_theme_to_widget(widget, theme)

# --- Game Logic ---
def ask_continue():
    if os.path.exists(SAVE_FILE):
        answer = messagebox.askyesno("Continue", "Do you want to continue your previous game?")
        if answer:
            load_scores()
            ask_game_mode()
        else:
            os.remove(SAVE_FILE)
            ask_game_mode()
    else:
        ask_game_mode()

def ask_game_mode():
    global mode_frame
    mode_frame = tk.Frame(window)
    tk.Label(mode_frame, text="Choose Game Mode", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(mode_frame, text="Single Player", width=20, command=lambda: select_mode('single')).pack(pady=5)
    tk.Button(mode_frame, text="Two Player", width=20, command=lambda: select_mode('two')).pack(pady=5)
    mode_frame.pack(pady=100)

def select_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.destroy()
    ask_player_names()

def ask_player_names():
    global name_frame
    name_frame = tk.Frame(window)
    tk.Label(name_frame, text="Enter Player Names", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(name_frame, text="Player X:").pack()
    x_entry = tk.Entry(name_frame)
    x_entry.pack()
    if game_mode == 'single':
        player_names["O"] = "Computer"
    else:
        tk.Label(name_frame, text="Player O:").pack()
        o_entry = tk.Entry(name_frame)
        o_entry.pack()
    def save_names():
        player_names["X"] = x_entry.get() or "Player X"
        if game_mode == 'two':
            player_names["O"] = o_entry.get() or "Player O"
        name_frame.destroy()
        if game_mode == 'single':
            ask_difficulty()
        else:
            draw_board()
    tk.Button(name_frame, text="Continue", command=save_names).pack(pady=10)
    name_frame.pack(pady=30)

def ask_difficulty():
    global diff_frame
    diff_frame = tk.Frame(window)
    tk.Label(diff_frame, text="Select Difficulty", font=("Helvetica", 16)).pack(pady=10)
    for level in ['Easy', 'Medium', 'Hard']:
        tk.Button(diff_frame, text=level, width=20, command=lambda l=level.lower(): set_difficulty(l)).pack(pady=5)
    diff_frame.pack(pady=50)

def set_difficulty(level):
    global difficulty
    difficulty = level
    diff_frame.destroy()
    draw_board()

def draw_board():
    global info_label, score_label
    board_frame = tk.Frame(window)
    board_frame.pack(expand=True, fill='both')
    for i in range(3):
        window.grid_rowconfigure(i, weight=1)
        for j in range(3):
            window.grid_columnconfigure(j, weight=1)
            btn = tk.Button(board_frame, text="", font=("Helvetica", 32), relief="raised")
            btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
            btn.config(command=lambda r=i, c=j: on_click(r, c))
            buttons[i][j] = btn

    for i in range(3):
        board_frame.grid_rowconfigure(i, weight=1)
        board_frame.grid_columnconfigure(i, weight=1)

    info_label = tk.Label(window, text="", font=("Helvetica", 16))
    info_label.pack(pady=5)
    score_label = tk.Label(window, text="", font=("Helvetica", 12))
    score_label.pack(pady=5)
    update_labels()
    apply_theme(current_theme)

def update_labels():
    info_label.config(text=f"{player_names[current_player]}'s turn ({current_player})")
    score_label.config(text=f"{player_names['X']} (X): {scores['X']}   {player_names['O']} (O): {scores['O']}   Draws: {scores['Draw']}")

def on_click(row, col):
    global current_player
    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        winner = check_winner()
        if winner:
            show_result(winner)
            return
        if game_mode == "two":
            current_player = "O" if current_player == "X" else "X"
        else:
            current_player = "O"
            update_labels()
            window.after(300, computer_move)
        update_labels()

def get_board_state():
    return [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]

def get_empty_cells():
    return [(i, j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == ""]

def check_winner(board=None):
    board = board or get_board_state()
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

def show_result(winner):
    scores[winner] += 1
    result = "It's a draw!" if winner == "Draw" else f"{player_names[winner]} wins!"
    update_labels()
    for row in buttons:
        for btn in row:
            btn.config(state="disabled")
    messagebox.showinfo("Game Over", result)
    reset_game()

def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn.config(text="", state="normal")
    update_labels()

def computer_move():
    global current_player
    move = None
    if difficulty == "easy":
        move = random.choice(get_empty_cells())
    elif difficulty == "medium":
        move = find_medium_move()
    elif difficulty == "hard":
        _, move = minimax(get_board_state(), True)

    if move:
        row, col = move
        buttons[row][col]["text"] = "O"
        winner = check_winner()
        if winner:
            show_result(winner)
            return
        current_player = "X"
        update_labels()

def find_medium_move():
    board = get_board_state()
    for player in ["O", "X"]:
        for i, j in get_empty_cells():
            temp = copy.deepcopy(board)
            temp[i][j] = player
            if check_winner(temp) == player:
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

    for i, j in get_empty_cells():
        board[i][j] = "O" if is_maximizing else "X"
        score, _ = minimax(board, not is_maximizing)
        board[i][j] = ""
        if is_maximizing and score > best_score:
            best_score, best_move = score, (i, j)
        elif not is_maximizing and score < best_score:
            best_score, best_move = score, (i, j)

    return best_score, best_move

def exit_and_save():
    with open(SAVE_FILE, "w") as f:
        f.write(f"{player_names['X']},{player_names['O']},{scores['X']},{scores['O']},{scores['Draw']}")
    window.destroy()

def load_scores():
    with open(SAVE_FILE, "r") as f:
        data = f.read().strip().split(",")
        player_names["X"], player_names["O"] = data[0], data[1]
        scores["X"], scores["O"], scores["Draw"] = map(int, data[2:])

# --- Start App ---
window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("900x900")
window.minsize(600, 600)
window.protocol("WM_DELETE_WINDOW", exit_and_save)

menu_bar = tk.Menu(window)
theme_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label="Light Theme", command=lambda: apply_theme("light"))
theme_menu.add_command(label="Dark Theme", command=lambda: apply_theme("dark"))
menu_bar.add_cascade(label="Theme", menu=theme_menu)
window.config(menu=menu_bar)

ask_continue()
window.mainloop()
