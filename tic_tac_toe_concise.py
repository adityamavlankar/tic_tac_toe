'''
Aditya's implementation of tic-tac-toe. Assumption 1: Turns alternate even across games.
An implication is that loser of a game gets the first chance in the next game.
Assumption 2: A player sticks with his/her symbol, either "x" or "o" throughout the session even across games.
'''

from tkinter import *
import tkinter.messagebox

grid_size = 3
buttons = [[None for x in range(grid_size)] for x in range(grid_size)]
win_highlight_color = {"x" : '#3E2129', "o" : '#214129'}
button_highlight_default = '#99AA99'
turn = True
game_over = False

def reset_game(topWindow):
    '''
    Destroy toast and start new game
    '''
    global game_over
    game_over = False
    for button_row in buttons:
        for button in button_row:
            button.configure(text = " ", highlightbackground=button_highlight_default)
    topWindow.destroy()

def show_message(title, label, button_text):
    '''
    Show toast with desired title, main message and button
    '''
    topWindow = Toplevel(tk)
    topWindow.title(title)
    Label(topWindow, text = label).grid()
    Button(topWindow, text = button_text, command=lambda:reset_game(topWindow)).grid()
    topWindow.protocol("WM_DELETE_WINDOW", lambda:reset_game(topWindow))    

def check_list_for_same_symbol(list_buttons, symbol):
    '''
    Check whether list of buttons passed to this function has same symbol.
    If yes highlight those buttons and show message about the win.
    '''
    global game_over
    for button in list_buttons:
        if button["text"] != symbol:
            return False
    for button in list_buttons:
        button.configure(highlightbackground=win_highlight_color[symbol])
    show_message('Game Over', "Winner " + symbol + ", you just won a game", 'Ok')
    game_over = True
    return True

def check_winner(symbol):
    '''
    Check whether player with given symbol has won the game. If so, give indication in UI as such.
    '''
    for button_row in buttons:
        if True == check_list_for_same_symbol(button_row, symbol):
            return
    for col in range(grid_size):
        col_buttons = []
        for row in range(grid_size):
            col_buttons.append(buttons[row][col])
        if True == check_list_for_same_symbol(col_buttons, symbol):
            return
    forward_diag_buttons = []
    for i in range(grid_size):
        forward_diag_buttons.append(buttons[i][i])
    if True == check_list_for_same_symbol(forward_diag_buttons, symbol):
        return
    reverse_diag_buttons = []
    for i in range(grid_size):
        reverse_diag_buttons.append(buttons[i][grid_size - i - 1])
    if True == check_list_for_same_symbol(reverse_diag_buttons, symbol):
        return
        
def check_tie():
    '''
    Check whether we hit a tie situation. Also provide indication in UI as such.
    '''
    for button_row in buttons:
        for button in button_row:
            if button["text"] == " ":
                return
    show_message('Game Over', "You fought well, it is a tie!", 'Ok')
    game_over = True

def checker(button):
    '''
    Process the next button click, i.e., next move in the game.
    '''
    if game_over == True:
        return
    global turn
    if button["text"] == " " and turn == True:
        button["text"] = "x"
        turn = False
    elif button["text"] == " " and turn == False:
        button["text"] = "o"
        turn = True

    check_winner("x")
    check_winner("o")
    if game_over == False:
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

    topWindowAbout = Toplevel(tk)
    topWindowAbout.title('About')
    Label(topWindowAbout, text="Tic Tac Toe v1.0\n\nby\n\nAditya Mavlankar\n\n\nQA tested by Aneesh and Aditya\non Mac OSX 10.11.6").grid()
    topWindowAbout.focus_force()

    tk.mainloop()

