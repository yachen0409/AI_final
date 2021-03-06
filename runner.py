import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 16
WIDTH = 16
MINES = 40

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

NUM_COLOR = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128),
             (128, 0, 0), (0, 128, 128), (0, 0, 0), (128, 128, 128)]

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
#-------------------------OUR CODE------------------------------
autoplay = False
autoplaySpeed = 0.3
test = False
testCount = 0

win_num=0
lost_num=0
bigger_lost_num = 0
random = 0
scoreBoard = set()
lostBoard = set()
#-------------------------OUR CODE------------------------------

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

while True:
    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            if (i, j) in revealed:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                nearby = game.nearby_mines((i, j))
                if nearby:
                    neighbors = smallFont.render(
                        str(nearby),
                        True, NUM_COLOR[nearby - 1]
                    )
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = rect.center
                    screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    #test button
    testBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING + 280,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Test"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = testBtn.center
    pygame.draw.rect(screen, WHITE, testBtn)
    screen.blit(buttonText, buttonRect)

    #autoplay button
    autoplayBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, BOARD_PADDING,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    bText = "Autoplay" if not autoplay else "Stop"
    buttonText = mediumFont.render(bText, True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = autoplayBtn.center
    pygame.draw.rect(screen, WHITE, autoplayBtn)
    screen.blit(buttonText, buttonRect)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    #-------------------------OUR CODE------------------------------
    if test and testCount!=10000:
        if game.mines==flags:
            scoreBoard.add(len(ai.safes)*2)
            testCount+=1
            win_num+=1
            autoplay=True
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            if testCount % 100 == 0:
                print("No.", testCount," iteration------------------")
        elif lost:
            # if len(ai.safes) >= 10:
            #     lostBoard.add(len(ai.safes))
            # # else:
            # #     lostBoard.add(1)
            if len(ai.safes) >= 1:
                scoreBoard.add(len(ai.safes))
                lostBoard.add(len(ai.safes))
                bigger_lost_num += 1

            testCount+=1
            lost_num+=1
            autoplay=True
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            if testCount % 100 == 0:
                print("No.", testCount," iteration------------------")
    elif test:
        print("---------------------------------------------------------")
        print("Won rate=", win_num/10000)
        print("Average step(if lost)=", sum(lostBoard)/bigger_lost_num)
        print("total random step=", random)
        print("average score=", sum(scoreBoard)/len(scoreBoard))
        print("average score when loss=", sum(lostBoard)/len(lostBoard))
        print("---------------------------------------------------------")
        autoplay=False
        test = False
        testCount = 0
        break
    #-------------------------OUR CODE------------------------------

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()
        
        #-------------------------OUR CODE------------------------------
        #If test button clicked, make an AI move
        if testBtn.collidepoint(mouse):
            autoplay=True
            test = True
            
        # If autoplay button clicked, make an AI move
        if autoplayBtn.collidepoint(mouse):
            print("run in autoplay")
            if not lost:
                autoplay = not autoplay
            else:
                autoplay = False
            time.sleep(0.2)
            continue
        #-------------------------OUR CODE------------------------------
        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            print(move)
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            test = False
            testCount = 0
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    #-------------------------OUR CODE------------------------------                    
    if autoplay:
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                # print("No moves left to make.")
                autoplay = False
            else:
                random+=1
                # print("No known safe moves, AI making random move.")
        # else:
        #     print("AI making safe move.")

        # Add delay for autoplay
        if autoplay:
            time.sleep(autoplaySpeed)
    #-------------------------OUR CODE------------------------------
        
    # Make move and update AI knowledge
    def make_move(move):
        if game.is_mine(move):
            return True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
            if not nearby:
                # Loop over all cells within one row and column
                for i in range(move[0] - 1, move[0] + 2):
                    for j in range(move[1] - 1, move[1] + 2):

                        # Ignore the cell itself
                        if (i, j) == move:
                            continue

                        # Add to the cell collection if the cell is not yet explored
                        # and is not the mine already none
                        if 0 <= i < HEIGHT and 0 <= j < WIDTH and (i, j) not in revealed:
                            make_move((i, j))
    if move:
        if make_move(move):
            autoplay = False
            lost = True

    pygame.display.flip()