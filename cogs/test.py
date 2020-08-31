#Checks if the inputted player has won
def check_win(player, board):
    #These are all the winning lines/combinations
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
    
    #For each one, if all 3 of those positions are the player's character, he's won
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] == player:
            return True

    #If I get to the end and he hasn't won, I can return false
    return False


#Simply makes a move given a player and their move
def make_move(player, space, board):
    
    #Convert space to int, and decrement for 0 based indexing, set to player
    board[int(space)-1] = player


#Resets a move (will use for recursive backtracking)
def remove_move(space, board):

    #Set that board space back to its number
    board[int(space)-1] = space


#Returns a list of all valid moves in the position
def valid_moves(board):
    moves = []

    #Go through each space, if it's not X or O, append it
    for space in board:
        if space != 'X' and space != 'O':
            moves.append(space)
    
    #Return moves at the end
    return moves


#Checks if there's a draw on the board
def check_draw(board):

    #If no valid moves, true, otherwise false
    return len(valid_moves(board)) == 0


#Recursive backtracking to score a move from the computer's perspective
#Moves are scored 1 for definitely winning, 0 for can be drawn, and -1 for can be lost
def compute_move(player, move, board):
    
    #Make the move inputted, and if it's a draw now return 0
    make_move(player, move, board)

    #If X won, return -1 or loss, and if computer won, return 1 or win, draw is 0
    if check_win('X', board):
        return -1
    if check_win('O', board):
        return 1
    if check_draw(board):
        return 0

    #If currently testing a computer move
    if player == 'O':

        #Set score higher than 1, for use with the min command later
        score = 2

        #For each valid move left
        for move in valid_moves(board):

            #Compute that move from the player's perspective, and update score if it's less
            #I use min since if the player CAN reach a win as a result of this, I want to assume the worst case
            score = min(score, compute_move('X', move, board))
            
            #When I'm done, I can remove the move (hence, recursive backtracking)
            remove_move(move, board)
        
        #Now, I can return the final score of the move
        return score

    #If currently testing a player move
    else:
        #lower than -1 for the max command
        score = -2

        #Once again go through all moves, this time use max, assume best possible computer play
        for move in valid_moves(board):
            score = max(score, compute_move('O', move, board))

            remove_move(move, board)
        
        #Finally return score
        return score
    
    #I'll have to remove the initial move after the command is executed


print(compute_move('O', '4', ['X', 'O', 'X', '4', 'O', '6', 'O', 'X', 'X']))