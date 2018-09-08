'''
Aditya's implementation of tic-tac-toe. Assumption 1: Turns alternate even across games.
An implication is that loser of a game gets the first chance in the next game.
Assumption 2: A player sticks with his/her symbol, either "x" or "o" throughout the session even across games.
'''

from tkinter import *
from collections import namedtuple

grid_size = 3
buttons = [[None for x in range(grid_size)] for x in range(grid_size)]
Tic_Tac_Toe_Symbol = namedtuple('Tic_Tac_Toe_Symbol', ['base_symbol', 'ui_symbol_unicode', 'win_highlight_color'])
tuple_alternating_symbols = (Tic_Tac_Toe_Symbol("x", '\N{multiplication x}', '#3E2129'), 
    Tic_Tac_Toe_Symbol("o", '\N{large circle}', '#214129'))
button_highlight_default = '#99AA99'
turn = False
game_over = False

def reset_game(top_window):
    '''
    Destroy message window from previous game and start new game
    '''
    global game_over
    game_over = False
    for button_row in buttons:
        for button in button_row:
            button.configure(text=" ", highlightbackground=button_highlight_default)
    top_window.destroy()

def show_message(title, label, button_text):
    '''
    Show message window with desired title, main message and button
    '''
    top_window = Toplevel(tk)
    top_window.title(title)
    Label(top_window, text=label).grid()
    Button(top_window, text=button_text, command=lambda:reset_game(top_window)).grid()
    top_window.protocol(name="WM_DELETE_WINDOW", func=lambda:reset_game(top_window))

def check_list_for_same_symbol(list_buttons, symbol):
    '''
    Check whether list of buttons passed to this function has same symbol.
    If yes, highlight those buttons and show message about the win.
    '''
    global game_over
    if any(button["text"] != symbol.ui_symbol_unicode for button in list_buttons):
        return False
    for button in list_buttons:
        button.configure(highlightbackground=symbol.win_highlight_color)
    show_message('Game Over', f'Player {symbol.ui_symbol_unicode}, you just won a game!', 'Ok')
    game_over = True
    return True

def check_winner(symbol):
    '''
    Check whether player with given symbol has won the game. If so, give indication in UI as such.
    '''
    for button_row in buttons:
        if check_list_for_same_symbol(button_row, symbol):
            return
    for col in range(grid_size):
        col_buttons = [buttons[row][col] for row in range(grid_size)]
        if check_list_for_same_symbol(col_buttons, symbol):
            return
    forward_diag_buttons = [buttons[i][i] for i in range(grid_size)]
    if check_list_for_same_symbol(forward_diag_buttons, symbol):
        return
    reverse_diag_buttons = [buttons[i][grid_size - i - 1] for i in range(grid_size)]
    if check_list_for_same_symbol(reverse_diag_buttons, symbol):
        return
        
def check_tie():
    '''
    Check whether we hit a tie situation. Also provide indication in UI as such.
    '''
    if any(buttons[i][j]["text"] == " " for i in range(grid_size) for j in range(grid_size)):
        return
    show_message('Game Over', 'You fought well, it is a tie!', 'Ok')
    game_over = True

def checker(button):
    '''
    Process the next button click, i.e., next move in the game.
    '''
    if game_over:
        return
    global turn

    if button["text"] == " ":
        button["text"] = tuple_alternating_symbols[int(turn)].ui_symbol_unicode
        turn = not turn

    for symbol in tuple_alternating_symbols:
        check_winner(symbol)
    if not game_over:
        check_tie()

if __name__ == "__main__":
    tk = Tk()
    tk.title("Tic Tac Toe")

    for row in range(grid_size):
        for col in range(grid_size):
            buttons[row][col] = Button(tk, text=" ", font=('Times 26 bold'), height=4, width=8,
                                       command=lambda row=row, col=col:checker(buttons[row][col]),
                                    highlightbackground=button_highlight_default)
            buttons[row][col].grid(row=row, column=col, sticky=S+N+E+W)

    top_window_about = Toplevel(tk)
    top_window_about.title('About')
    Label(top_window_about, text="Tic Tac Toe v1.0\n\nby\n\nAditya Mavlankar\n\n\nQA tested by Aneesh and Aditya\non Mac OSX 10.11.6").grid()
    top_window_about.focus_force()

    tk.mainloop()

