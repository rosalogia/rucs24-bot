def display_board(board):
    print(f' {board[0]} | {board[1]} | {board[2]}')
    print(f'-----------')
    print(f' {board[3]} | {board[4]} | {board[5]}')
    print(f'-----------')
    print(f' {board[6]} | {board[7]} | {board[8]}')
    print()


def check_win(board, player):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
    
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] == player:
            return True
    
    return False


def make_move(board, player, space):
    board[int(space)-1] = player


def remove_move(board, space):
    board[int(space)-1] = space


def valid_moves(board):
    moves = []
    for space in board:
        if space != 'X' and space != 'O':
            moves.append(space)
    
    return moves


def check_draw(board):
    if len(valid_moves(board)) == 0:
        return True
    else:
        return False


def compute_move(board, player, move):
    if check_win(board, 'X'):
        return -1
    if check_win(board, 'O'):
        return 1
    
    make_move(board, player, move)
    if check_draw(board):
        return 0

    if player == 'X':
        score = -2

        for move in valid_moves(board):
            score = max(score, compute_move(board, 'O', move))

            remove_move(board, move)
        
        return score
    
    else:
        score = 2
        for move in valid_moves(board):
            score = min(score, compute_move(board, 'X', move))
            
            remove_move(board, move)
        
        return score


board = [str(x) for x in range(1, 10)]

counter = 2
display_board(board)

while True:
    valid = valid_moves(board)

    if counter % 2 == 1:
        player_move = ''

        while player_move not in valid:
            player_move = input('Please enter a valid move => ')
        
        make_move(board, 'X', player_move)

    else:
        best_move = ''
        best_score = -2

        for move in valid:
            score = compute_move(board, 'O', move)
            remove_move(board, move)

            if score > best_score:
                best_move = move
                best_score = score
        
        make_move(board, 'O', best_move)
        display_board(board)
        print('Computer chose ' + best_move + ' with a score of ' + str(best_score))
    

    if check_win(board, 'O'):
        print('Sorry, you lost!')
        break
    elif check_win(board, 'X'):
        print('This will never be printed lol')
    elif check_draw(board):
        print("It's a draw!")
        break

    counter += 1



        
