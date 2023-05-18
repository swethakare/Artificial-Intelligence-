import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
GREY = (105,105,105)
BLACK = (0,0,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000) # heuristic favourable for the maximizing player
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

clock = pygame.time.Clock()
def KeyBoard_Event():
    # Set up the input string
    
    myfont = pygame.font.SysFont("serif", 35)
    input_string = ""
    inputevent = 1
    while inputevent:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            inputevent = 0
                            return input_string
                        elif event.key == pygame.K_BACKSPACE:
                            input_string = input_string[:-1]
                        elif event.key == pygame.K_DELETE:
                            input_string = input_string[:-1]
                        else:
                            input_string += event.unicode
                        
        
        # Draw the input string on the Pygame screen
        input_text = myfont.render(input_string, True, WHITE)
        x = 40
        y = 550
        screen.blit(input_text, (x,y))
        # Clear the screen
        
        # Update the input string on the screen
        pygame.display.update()
    print(input_string)
    return input_string
# Define the function to draw the menu                    
    # Draw the menu
def choosingBoard_Colors():
    myfont = pygame.font.SysFont("serif", 25)
    colordict = {1:(230,219,172),2:(238,220,154),3:(249,224,118),4:(201,187,142),5:(223,201,138),
                 6:(250,226,156),7:(200,169,81),8:(243,234,175),9:(216,184,99),10:(227,183,120),
                 11:(231,194,125),12:(220,215,160),13:(227,197,101),14:(253,233,146),15:(189,165,93),
                 16:(218,193,124)}
    
    screen.fill(GREY)
    colorpallet(colordict)
    pygame.display.update()
   
    option = int(KeyBoard_Event())
    print(option)
    BoardColor = colordict[option]
    return BoardColor
    # DisplayBoardColor(option)

def colorpallet(colordict):
    myfont = pygame.font.SysFont("serif", 25)
    Colorchoose = myfont.render("Please choose colors from the pallet",True, WHITE)
    screen.blit(Colorchoose, (40,10))  
    
    Colorchoose1 = myfont.render("Press 1 - Tan",True, colordict[1])
    screen.blit(Colorchoose1, (40,50))
    
    Colorchoose2 = myfont.render("Press 2 - BEIGE",True, colordict[2])
    screen.blit(Colorchoose2, (400,50))
    
    Colorchoose3 = myfont.render("Press 3 - MACAROON",True, colordict[3])
    screen.blit(Colorchoose3, (40,100))
    
    Colorchoose4 = myfont.render("Press 4 - HAZEL WOOD",True, colordict[4])
    screen.blit(Colorchoose4, (400,100))
    
    
    Colorchoose6 = myfont.render("Press 5 - OAT",True, colordict[5])
    screen.blit(Colorchoose6, (400,150))
    
    Colorchoose7 = myfont.render("Press 6 - EGG NOG",True, colordict[6])
    screen.blit(Colorchoose7, (40,200))
    
    Colorchoose8 = myfont.render("Press 7 - FAWN",True, colordict[7])
    screen.blit(Colorchoose8, (400,200))
    
    Colorchoose9 = myfont.render("Press 8 - SUGAR COOKIE",True, colordict[8])
    screen.blit(Colorchoose9, (40,250))
    
    Colorchoose10 = myfont.render("Press 9 - SAND",True, colordict[9])
    screen.blit(Colorchoose10, (400,250))
    
    Colorchoose11 = myfont.render("Press 10 - SEPIA",True, colordict[10])
    screen.blit(Colorchoose11, (40,300))
    
    Colorchoose12 = myfont.render("Press 11 - LATTE",True, colordict[11])
    screen.blit(Colorchoose12, (400,300))
    
    Colorchoose13 = myfont.render("Press 12 - OYSTER",True, colordict[12])
    screen.blit(Colorchoose13, (40,350))
    
    Colorchoose14 = myfont.render("Press 13 - BISCOTTI",True, colordict[13])
    screen.blit(Colorchoose14, (400,350))
    
    Colorchoose15 = myfont.render("Press 14 - PARMESEAN",True, colordict[14])
    screen.blit(Colorchoose15, (40,400))
    
    Colorchoose16 = myfont.render("Press 15 - HAZELNUT",True, colordict[15])
    screen.blit(Colorchoose16, (400,400))
    
    Colorchoose5 = myfont.render("Press 16 - Sandcastle",True, colordict[16])
    screen.blit(Colorchoose5, (40,150))

def choosingPlayerName():
    # choosing player and agent's name
    myfont = pygame.font.SysFont("serif", 35)
    screen.fill(GREY)
    Colorchoose = myfont.render("Please give a name to the Player",True, WHITE)
    screen.blit(Colorchoose, (40,350))    
    pygame.display.update()
    pname = KeyBoard_Event()
    return pname
    

def choosingAgentName():
    # choosing player and agent's name
    myfont = pygame.font.SysFont("serif", 35)
    screen.fill(GREY)
    Colorchoose = myfont.render("Please give a name to the Agent",True, WHITE)
    screen.blit(Colorchoose, (40,350))    
    pygame.display.update()
    aname = KeyBoard_Event()
    return aname
    
def selectTurns(Aname,Pname):
    # choosing player and agent's name
    myfont = pygame.font.SysFont("serif", 35)
    screen.fill(GREY)
    Choosepturn = myfont.render("Start with agent or player ?"+Aname+" or " +Pname,True, WHITE)
    screen.blit(Choosepturn, (40,350)) 
    pygame.display.update()

    turn = KeyBoard_Event()
    return turn;


def choosingDepth():
    # choosing player and agent's name
    myfont = pygame.font.SysFont("serif", 35)
    screen.fill(GREY)
    chooseDepth = myfont.render("Please give depth between 1 to 5",True, WHITE)
    screen.blit(chooseDepth, (40,350))    
    pygame.display.update()
    depth = KeyBoard_Event()
    return depth


    
def draw_board(board,BoardColor):
    #choose a color for the board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BoardColor, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, GREY, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+2) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
options = ['Choose 1-16 for a unique color', 'Enter Player name', 'Enter Agent name','Select turns - P for player/A for agent','Exit']
selected_option = 0;
# draw_menu()
BoardColor = choosingBoard_Colors()
Pname = choosingPlayerName()
Aname = choosingAgentName()
Turn = selectTurns(Aname,Pname)
Deep = int(choosingDepth())


# print("Agent:"+Aname +"Pname:"+Pname)
draw_board(board,BoardColor)
pygame.display.update()
myfont = pygame.font.SysFont("serif", 35)

if Turn == Aname:
    turn = AI;
elif Turn == Pname:
    turn = PLAYER;
else:
    turn = random.randint(PLAYER, AI)
print(turn)

Movescnt = 0
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  # Get the start time
while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, GREY, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, GREY, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                Movescnt += 1
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        AIWIN = 0
                        label = myfont.render("Player " +Pname+ " wins!!", 1, BLACK)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board,BoardColor)


    # # Ask for Player 2 Input
    if turn == AI and not game_over:                
        Movescnt += 1
        #col = random.randint(0, COLUMN_COUNT-1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, Deep, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                AIWIN = 1
                label = myfont.render("Agent " +Aname+ " wins!!", 1, WHITE)
                screen.blit(label, (40,10))
                game_over = True

            print_board(board)
            draw_board(board,BoardColor)

            turn += 1
            turn = turn % 2
            
    clock.tick(60)
  
 
    end_time = pygame.time.get_ticks()  # Get the end time
    time_taken = (end_time - start_time) / 1000  # Convert to seconds
    if game_over:
        pygame.time.wait(3000)
        screen.fill(WHITE)
        outputscreen = myfont.render("OUTPUT SCREEN", 1, BLACK)
        screen.blit(outputscreen, (170,260))
        totalmoves = myfont.render("Total Moves to win the game: "+str(Movescnt), 1, BLACK)
        screen.blit(totalmoves, (40,300))
        if AIWIN:
           label = myfont.render("Agent " +Aname+ " wins!!", 1, BLACK)
           screen.blit(label, (40,350))
        else:
           label = myfont.render("Player " +Pname+ " wins!!", 1, BLACK)
           screen.blit(label, (40,350))
           
        TimeTaken = myfont.render("Total Time taken "+str(time_taken), 1, BLACK)
        screen.blit(TimeTaken, (40,410))
        pygame.display.update()
        
        pygame.time.wait(5000)
        

