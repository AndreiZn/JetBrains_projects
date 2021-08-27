# write your code here
def print_grid(UI):
    print('---------')
    print('| ' + UI[0] + ' ' + UI[1] + ' ' + UI[2] + ' |')
    print('| ' + UI[3] + ' ' + UI[4] + ' ' + UI[5] + ' |')
    print('| ' + UI[6] + ' ' + UI[7] + ' ' + UI[8] + ' |')
    print('---------')   

def check_game_state(UI):
    game_state = 1
    num_X = sum([UI[i] == 'X' for i in range(len(UI))])
    num_O = sum([UI[i] == 'O' for i in range(len(UI))])
    if abs(num_X - num_O) > 1:
        print('Impossible')
        game_state = 0
    else:
        fl_X, fl_O = False, False
        if (UI[0] == 'X' and UI[1] == 'X' and UI[2] == 'X'):
            fl_X = True
        if (UI[3] == 'X' and UI[4] == 'X' and UI[5] == 'X'):
            fl_X = True
        if (UI[6] == 'X' and UI[7] == 'X' and UI[8] == 'X'):
            fl_X = True
        if (UI[0] == 'X' and UI[3] == 'X' and UI[6] == 'X'):
            fl_X = True
        if (UI[1] == 'X' and UI[4] == 'X' and UI[7] == 'X'):
            fl_X = True
        if (UI[2] == 'X' and UI[5] == 'X' and UI[8] == 'X'):
            fl_X = True
        if (UI[0] == 'X' and UI[4] == 'X' and UI[8] == 'X'):
            fl_X = True
        if (UI[2] == 'X' and UI[4] == 'X' and UI[6] == 'X'):
            fl_X = True
            
        if (UI[0] == 'O' and UI[1] == 'O' and UI[2] == 'O'):
            fl_O = True
        if (UI[3] == 'O' and UI[4] == 'O' and UI[5] == 'O'):
            fl_O = True
        if (UI[6] == 'O' and UI[7] == 'O' and UI[8] == 'O'):
            fl_O = True
        if (UI[0] == 'O' and UI[3] == 'O' and UI[6] == 'O'):
            fl_O = True
        if (UI[1] == 'O' and UI[4] == 'O' and UI[7] == 'O'):
            fl_O = True
        if (UI[2] == 'O' and UI[5] == 'O' and UI[8] == 'O'):
            fl_O = True
        if (UI[0] == 'O' and UI[4] == 'O' and UI[8] == 'O'):
            fl_O = True
        if (UI[2] == 'O' and UI[4] == 'O' and UI[6] == 'O'):
            fl_O = True
            
        if fl_X and fl_O:
            print('Impossible')
            game_state = 0
        else:
            if fl_X:
                print('X wins')
                game_state = 0
            elif fl_O:
                print('O wins')
                game_state = 0
            else:
                if num_X + num_O < 9:
                    print('Game not finished')
                else:
                    print('Draw')
                    game_state = 0
                    
    return game_state
    
UI = list('         ')
print_grid(UI)
     
# UI = list(input('Enter the coordinates:'))

game_on = 1
while game_on:

    coord_read = False
    symbols = ['X', 'O']
    
    while not coord_read:
        coord = input('Enter the coordinates:').split()
        fl = True # correct input
        for c in coord:
            if c.isdigit():
                pass
            else:
                fl = False
                print('You should enter numbers!')
        if fl:
            coord = [int(coord[i]) for i in range(len(coord))]
            if coord[0] < 1 or coord[0] > 3 or coord[1] < 1 or coord[1] > 3:
                print('Coordinates should be from 1 to 3!')
            else:
                line_coord = 3*(coord[0] - 1) + coord[1] - 1
                if UI[line_coord] == 'X' or UI[line_coord] == 'O':
                    print('This cell is occupied! Choose another one!') 
                else:
                    coord_read = True
                    num_X = sum([UI[i] == 'X' for i in range(len(UI))])
                    num_O = sum([UI[i] == 'O' for i in range(len(UI))])
                    UI[line_coord] = symbols[(num_X + num_O) % 2]
                    print_grid(UI)

    game_on = check_game_state(UI)
