import discord
from discord.ext import commands


async def display_board(ctx, board):
    """Displays the board by setting the string output and then sending it"""

    #Start with syntax highlighting and a line of -----
    output = '```py\n'
    output += '-'*29 + '\n'

    #Go through each grid space, add it in proper spot
    for i in range(6):
        output += '|'
        for j in range(7):
            if board[i][j] in ['X', 'O']:
                output += f"'{board[i][j]}'|"
            else:
                output += f' {board[i][j]} |'

        output += '\n' + '-'*29 + '\n'
    output += '```'

    #Finally, send output
    await ctx.send(output)


def check_win(player, board):
    """Checks if the given player has won"""

    #Check all horizontal lines
    for i in range(len(board)):
        for j in range(len(board[0])-4+1):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == player:
                return True
    
    #Check all vertical lines
    for i in range(len(board)-4+1):
        for j in range(len(board[0])):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == player:
                return True
    
    #Check diagonals in both directions
    for i in range(len(board)-4+1):
        for j in range(len(board[0])-4+1):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == player:
                return True
            
            if board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] == player:
                return True
    
    #If they still haven't won return false
    return False


def make_move(player, space, board):
    """Enters the given player into the given space"""

    #Convert move to int and subtract 1 for zero based indexing
    col = int(space) - 1

    #Check all rows from the bottom until there's an empty space, add player
    for row in range(5, -1, -1):
        if board[row][col] != 'X' and board[row][col] != 'O':
            board[row][col] = player
            break
    return


def remove_move(space, board):
    """Reverts a move for recursive backtracking"""

    #Set col
    col = int(space) - 1

    #Go through the row the other way, reset the space at the topmost X or O
    for row in range(6):
        if board[row][col] == 'X' or board[row][col] == 'O':
            if row == 0:
                board[row][col] = str(col + 1)
            else:
                board[row][col] = ' '
            break
    return


def valid_moves(board):
    """Returns a list of all valid moves currently"""

    #If the identification number is still at the top, append it
    valid = []
    for col in range(7):
        if board[0][col] == str(col+1):
            valid.append(str(col+1))
    #Return valid moves
    return valid


def check_draw(board):
    """Checks if the board is drawn"""

    #If there are no valid moves, it's a draw
    return len(valid_moves(board)) == 0


def heuristic(player, board):
    """Gives the player a 'score' based on the state of the board"""

    #Since the sample space is large, I'll go to a certain depth then evaluate with the heuristic
    #My custom heuristic involves the number of ways you can connect four and also rewards you for "threats"
    #The lower the threat, the more valuable, and my AI takes this into account
    #Thus, it's not a perfect AI, but the heuristic is pretty good so I haven't been able to beat it

    #Set opponent variable to whatever player is not
    opponent = 'X' if player == 'O' else 'O'

    #Each player starts with a score of 100
    score = 100

    #Check all horizontal lines of four
    for i in range(len(board)):
        for j in range(len(board[0])-4+1):

            #If blocked by the opponent, decrease score since that's one connection you can't make now
            if board[i][j] == opponent or board[i][j+1] == opponent or board[i][j+2] == opponent or board[i][j+3] == opponent:
                score -= 1

            #If not blocked, check if 2 or 3 of the spaces in the group of 4 are filled
            else:
                #line_score contains the number of spaces in this line the player has filled
                line_score = (board[i][j] == player) + (board[i][j+1] == player) + (board[i][j+2] == player) + (board[i][j+3] == player)

                #If it's 2, increment their score by the row + 1 since it starts at 0 (lower rows are higher indexes, and are more valuable)
                if line_score == 2:
                    score += i+1
                
                #If it's 3, increment their score by 3 times the (row + 1) since it's much more of a threat
                elif line_score == 3:
                    score += 3*(i+1)
    
    #Check all vertical lines of four
    for i in range(len(board)-4+1):
        for j in range(len(board[0])):
            if board[i][j] == opponent or board[i+1][j] == opponent or board[i+2][j] == opponent or board[i+3][j] == opponent:
                score -= 1
            else:
                line_score = (board[i][j] == player) + (board[i+1][j] == player) + (board[i+2][j] == player) + (board[i+3][j] == player)

                #Since they aren't in the same row, the actual "threat" is the lowest space
                if line_score == 2:
                    #This time I use (i+2)+1 since the lowest space in a vertical unobstructed line of 2 is 2 above i
                    score += i+2+1
                elif line_score == 3:
                    #Same story for 3, but now it's i+3
                    score += 3*(i+3+1)
    
    #Check all diagonals
    for i in range(len(board)-4+1):
        for j in range(len(board[0])-4+1):
            if board[i][j] == opponent or board[i+1][j+1] == opponent or board[i+2][j+2] == opponent or board[i+3][j+3] == opponent:
                score -= 1
            else:
                line_score = (board[i][j] == player) + (board[i+1][j+1] == player) + (board[i+2][j+2] == player) + (board[i+3][j+3] == player)

                #This time I need to find the lowest space (the actual threat) manually
                filled = [(board[i][j] == player), (board[i+1][j+1] == player), (board[i+2][j+2] == player), (board[i+3][j+3] == player)]

                #Keep checking for the lowest space, add to score as needed
                for num in range(3, -1, -1):
                    if not filled[num]:
                        if line_score == 2:
                            score += i+num+1
                            break
                        elif line_score == 3:
                            score += 3*(i+num+1)
                            break
            
            #Same thing for the other diagonal
            if board[i][j+3] == opponent or board[i+1][j+2] == opponent or board[i+2][j+1] == opponent or board[i+3][j] == opponent:
                score -= 1
            else:
                line_score = (board[i][j+3] == player) + (board[i+1][j+2] == player) + (board[i+2][j+1] == player) + (board[i+3][j] == player)
                filled = [(board[i][j+3] == player), (board[i+1][j+2] == player), (board[i+2][j+1] == player), (board[i+3][j] == player)]

                for num in range(3, -1, -1):
                    if not filled[num]:
                        if line_score == 2:
                            score += i+num+1
                            break
                        elif line_score == 3:
                            score += 3*(i+num+1)
                            break
    
    #Finally, return their heuristic score (should approximately depict how good/bad the position is)
    return score


def compute_move(player, move, depth, deepest, board):
    """Score a computer move based on whether it's winning, losing, drawn, or heuristic"""
    #The scale I'm using to score moves is 1000 for absolutely winning (any number bigger than the heuristic can reach is fine) and -1000 for losing
    
    #First, I make the move to test from there
    make_move(player, move, board)

    #If there's a win or draw on the board, return the corresponding number
    if check_win('X', board):
        return -1000
    if check_win('O', board):
        return 1000
    if check_draw(board):
        return 0

    #If I've reached my target depth, return the difference in heuristics, to see how much better or worse the computer is doing
    if depth == deepest:
        return heuristic('O', board) - heuristic('X', board)
    
    #If I'm evaluating a computer move
    if player == 'O':
        #Set score to a value higher than any evaluation, for use with min
        score = 2000

        #Go through all the valid moves for opponent
        for move in valid_moves(board):
            #Compute move from the opponent's perspective, set depth to 1 lower
            #Assume best possible opponent play, so update score to the min of these
            score = min(score, compute_move('X', move, depth+1, deepest, board))

            #Now we can remove that move
            remove_move(move, board)
        
        #Return that worst case scenario score
        return score
    
    #If I'm evaluating a human move
    else:
        #Set score to value lower than any evaluation, for use with max
        score = -2000

        #Assume best possible computer play, update score with max
        for move in valid_moves(board):
            score = max(score, compute_move('O', move, depth+1, deepest, board))
            remove_move(move, board)
        
        #Return that worst case scenario (from the human perspective) score
        return score


class ConnectFourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def connectfour(self, ctx):
        """Plays a game of Connect Four with the user (not unbeatable, but nobody's beat it yet)"""

        def check(m):
            """Quick check to make sure only the person in the game and channel can respond"""
            return m.channel == ctx.channel and m.author == ctx.author
        
        #The first row of board is just the numbers from 1 to 7 to identify the columns
        board = [[str(x) for x in range(1, 8)]]

        #The other 5 rows are just empty for now
        board.extend([' ' for x in range(7)] for y in range(5))

        #Parity of the counter determines whose move it is
        #Currently set to human
        counter = 0

        #Difficulty is 0 for easy, 1 for medium, 2 for hard
        difficulty = 1

        #Keeps track in case player wants to go back in training
        previous_best_move = ''
        previous_player_move = ''
        
        #Let the user select their difficulty
        await ctx.send("Easy, Medium, or Hard?")
        msg = await self.bot.wait_for('message', check=check)

        if (msg.content.lower() == 'easy'):
            difficulty = 0
        elif (msg.content.lower() == 'hard'):
            difficulty = 2

        #Let the user decide if they want training mode
        await ctx.send("Do you want to use training mode?")
        msg = await self.bot.wait_for('message', check=check)
        training = (msg.content.lower() == 'yes')

        #Ask the user if they want to go first and retrieve their message
        await ctx.send("Do you want to go first?")
        msg = await self.bot.wait_for('message', check=check)

        #If they say no, update the counter so the computer goes first
        if msg.content.lower() == 'no':
            counter = 1
        
        #Otherwise, show them the board for their move
        else:
            await display_board(ctx, board)

        #Keep going until the game ends
        while True:
            #I start by storing the valid moves
            valid = valid_moves(board)

            #If it's the human's move
            if counter % 2 == 0:
                #Set to empty for now
                player_move = ''

                #Keep going until they put in a valid move
                while player_move not in valid:

                    #If they enter q, they quit so I can exit
                    if player_move == 'q':
                        await ctx.send('Computer wins by resignation!')
                        return

                    #If they're in training mode, give options to go back and evaluate
                    if training:

                        #Decrements counter by 2, removes last 2 moves, displays new board
                        if player_move == 'b':
                            counter -= 2
                            remove_move(previous_best_move, board)
                            remove_move(previous_player_move, board)

                            await display_board(ctx, board)
                            break
                        
                        #Evaluates each move at a depth of 3 from the player's side and outputs
                        if player_move == 'e':
                            eval_str = ''
                            for move in valid:
                                eval_str += move + ': ' + str(-compute_move('X', move, 0, 3, board)) + '\n'
                                remove_move(move, board)
                            
                            await ctx.send(f'These only go to depth 3. They are not a perfect eval for sure.\n{eval_str}')
            
                        #Gives all the options for training mode
                        await ctx.send('Please enter a valid move, q to quit, b to take back your move, or e to see evaluations')
                        msg = await self.bot.wait_for('message', check=check)
                        player_move = msg.content
                    
                    #If not in training mode, only display those options
                    else:
                        #Prompt them for a valid move and store it
                        await ctx.send('Please enter a valid move or q to quit')
                        msg = await self.bot.wait_for('message', check=check)
                        player_move = msg.content
                
                #If they went back, restart the loop
                if player_move == 'b':
                    continue

                #Make the player move
                make_move('X', player_move, board)
                previous_player_move = player_move
            
            #If it's the computer's move
            else:
                #Set the best move and best score to default values
                best_move = ''
                best_score = -2000

                #Go through each valid move
                for move in valid:
                    #I compute the move, with depth equal to difficulty
                    score = compute_move('O', move, 0, difficulty, board)

                    #I can remove the move now
                    remove_move(move, board)

                    #Update best move and best score
                    if score > best_score:
                        best_move = move
                        best_score = score

                #Make the move and display the computer move
                make_move('O', best_move, board)
                await display_board(ctx, board)
                await ctx.send('Computer chose ' + best_move)

                #If training, evaluate the player's heuristic after computer move
                if training:
                    #Set previous best move for later, set player_score to really low value
                    previous_best_move = best_move
                    player_score = -2000

                    #Evaluate each move, keep the max eval
                    for move in valid:
                        player_score = max(player_score, -1*compute_move('X', move, 0, 3, board))
                        remove_move(move, board)

                    #Output the relative heuristics
                    if player_score > 0:
                        await ctx.send(f'You have an advantage of {player_score} heuristic points!')
                    elif player_score < 0:
                        await ctx.send(f'The computer has an advantage of {-player_score} heuristic points!')
                    else:
                        await ctx.send(f'You and the computer are even on heuristic points!')

            #Check for wins or draw and exit if there are any
            if check_win('O', board):
                await ctx.send('Sorry, you lost!')
                return
            elif check_win('X', board):
                await display_board(ctx, board)
                await ctx.send('You beat this thing? Thats insaneeeee')
                break
            elif check_draw(board):
                await ctx.send("It's a draw!")
                break
            
            #Increment counter
            counter += 1


def setup(bot):
    bot.add_cog(ConnectFourCog(bot))