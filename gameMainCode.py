import pygame
from pygame.locals import *
import random
import time
from datetime import datetime

def main():
    # Initialise screen and display game name
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption('Triple Letter Speed')
    
    # Fill background with plain color
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    # Prepare opening text
    font = pygame.font.Font(None, 36)
    drawInstructions(background, font, screen)
    drawCenteredText("Press the A key to begin", background, font, screen.get_size()[1]-80, screen)

    # Prepare rectangle for playerhealth
    playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    playerHealthColor = [0, 0, 255]
    BASEPLAYERPOS = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    BACKGROUNDCOLOR = (0,0,20)

    # Prepare rectangle for enemy health
    enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    enemyHealthColor = [0, 0, 255]
    BASEENEMYPOS = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)

    # Display everything for the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.key.set_repeat()

    # Prepares Starting configuration of variables for gameplay
    opening = True
    lettersPressed = resetPressed()
    turnPassed = True
    turnStartTime = datetime.now().timestamp()
    gameGoing = True
    score = 0
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and gameGoing:
                keyboardState = pygame.key.get_pressed()
                # Closes game if user hits delete (Developmental Artifact)
                if(keyboardState[127]):
                    return
                # Runs on the first button press and sets up the background and whatnot, also changes the flag of opening to false
                elif(opening and keyboardState[65+32]):
                    letters = grandReset(background, BACKGROUNDCOLOR, screen, font, opening)
                    opening = False
                    gameGoing = True
                    timeBetweenTurns = 3
                    playerHealthColor = [0,0,255]
                    enemyHealthColor = [0,0,255]
                    turnStartTime = datetime.now().timestamp()
                    score = 0
                    pygame.display.flip()
                    letters = turnReset(background, screen, font, BACKGROUNDCOLOR)
                    pygame.display.flip()
                    
                # Updates Health Values based on button pressed and strikes-through letters when pressed
                elif(not opening):
                    if(not(letters[0] == " ")):
                        if(keyboardState[ord(letters[0])+32] and (not(lettersPressed[0]))):
                            onLetterPress(lettersPressed, 1, background, screen, font)

                        elif(keyboardState[ord(letters[1])+32] and (not(lettersPressed[1]))):
                            onLetterPress(lettersPressed, 2, background, screen, font)

                        elif(keyboardState[ord(letters[2])+32] and (not(lettersPressed[2]))):
                            onLetterPress(lettersPressed, 3, background, screen, font)

                    # Displays a flag to the user that the turn has failed
                    else:
                        turnPassed = False
                        FailedSymbol = font.render("Turn Failed", 9, (255, 30, 30))
                        FailedSymbolPos = Rect(screen.get_width()/2-60, screen.get_height()-122, 30, 40)
                        background.blit(FailedSymbol, FailedSymbolPos)
                        screen.blit(background, (0,0))
                        pygame.display.flip()
                                  
        # Waits for the delay between moves to elapse and updates time before the next attack
        if(not(opening) and (gameGoing)):
            # Runs after turn timer
            if(turnStartTime + timeBetweenTurns < datetime.now().timestamp()):
                # Performs Turn, takes health from user if turn was failed and takes enemy health otherwise
                if(lettersPressed[0] and lettersPressed[1] and lettersPressed[2] and turnPassed):
                    if(enemyHealthColor[2]-40 >0):
                        enemyHealthPos = updateHealth(screen, background, enemyHealthPos, 40, BACKGROUNDCOLOR, screen.get_size()[1])
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEENEMYPOS)
                        enemyHealthColor = [enemyHealthColor[0]+40, 0, enemyHealthColor[2]-40]
                    else: # If enemy health is gone, resets enemy
                        enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
                        enemyHealthColor = [0, 0, 255]
                        timeBetweenTurns = timeBetweenTurns * 0.85
                    # Updates enemy health bar whether or not they were reset and draws to screen
                    pygame.draw.rect(background, enemyHealthColor, enemyHealthPos)
                    score = score + 1
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                    
                else:
                    if(playerHealthColor[2] - 15 > 0): # Takes user health if turn was failed
                        playerHealthPos = updateHealth(screen, background, playerHealthPos, 15, BACKGROUNDCOLOR, screen.get_size()[1])
                        playerHealthColor = [playerHealthColor[0]+15, 0, playerHealthColor[2]-15]
                        pygame.draw.rect(background, BACKGROUNDCOLOR, BASEPLAYERPOS)
                        pygame.draw.rect(background, playerHealthColor, playerHealthPos)
                        # Resets turn failed flag if a turn has been failed at this point, display no mess up yet otherwise
                        try:
                            FailedSymbol.fill(BACKGROUNDCOLOR)
                            background.blit(FailedSymbol, FailedSymbolPos)
                        except: 
                            print("No mess up yet")
                        screen.blit(background, (0,0))
                        pygame.display.flip()
                    else: #Displays end screen if user health has completely drained
                        background.fill((30, 30, 30))
                        gameGoing = False
                        drawInstructions(background, font, screen)
                        drawCenteredText("Your score was " +str(score) +" press A to play again", background, font, screen.get_size()[1]-80, screen)
                        screen.blit(background, (0, 0))
                        pygame.display.flip()

                if(gameGoing):
                    # Resets Screen Between turns once health has been updated for both parties also resets the list of letters pressed and the turnPassed flag
                    letters = turnReset(background, screen, font, BACKGROUNDCOLOR)
                    lettersPressed = resetPressed()
                    # Resets fail symbol
                    try:
                        FailedSymbol.fill(BACKGROUNDCOLOR)
                        background.blit(FailedSymbol, FailedSymbolPos)
                    except: 
                        print("No mess up yet")
                    pygame.display.flip()
                    turnStartTime = datetime.now().timestamp()
                    turnPassed = True
        elif((not gameGoing)): # Runs reset feature if A is pressed on game over screen
            keyboardState = pygame.key.get_pressed()
            if(keyboardState[65+32]):
                letters = updateLetters()
                letters = grandReset(background, BACKGROUNDCOLOR, screen, font, opening)
                playerHealthColor = [0,0,270]
                gameGoing = True
                timeBetweenTurns = 3
                turnStartTime = datetime.now().timestamp()
                score = 0
                playerHealthPos.height = screen.get_size()[1]//255*255
                enemyHealthPos.height = screen.get_size()[1]//255*255
                playerHealthColor = [0,0,255]
                enemyHealthColor = [0,0,255]
                pygame.display.flip()

# Returns the inputted box but shorter to account for damage 
def updateHealth(background, surface, box, change, color, screenHeight):
    temp = Rect(box.left, box.top, box.w, box.h-change*(screenHeight//255))
    pygame.draw.rect(background, color, box)
    background.blit(surface, temp)
    return temp

# Returns health completely restored for next enemy or consecutive runs of player
def resetHealth(background, surface, box, screenHeight):
    temp = Rect(box.left, box.top, box.w, (screenHeight//255*255))
    pygame.draw.rect(background, [0, 0, 255], box)
    background.blit(surface, temp)
    return temp

# Returns a new set of random letters
def updateLetters():
    temp = [" ", " ", " "]
    temp[0] = chr(random.randrange(65, 91))
    temp[1] = chr(random.randrange(65, 91))
    temp[2] = chr(random.randrange(65, 91))
    return temp  

# Resets values and dispalys new letters for new turn
def turnReset(background, screen, font, BACKGROUNDCOLOR):
    drawBottomTextCover(background, screen, BACKGROUNDCOLOR)
    letters = updateLetters()
    drawCenteredText("Press the " + letters[0] + " " + letters[1] + " " + letters[2] + " keys", background, font, screen.get_size()[1]-80, screen)
    screen.blit(background, (0, 0))
    return letters

# Resets pressed keys
def resetPressed():
    return [False, False, False]

# Resets when new game is started, displaying text and a quick "wait" for the next turn
def grandReset(background, BACKGROUNDCOLOR, screen, font, opening):
    drawInstructions(background, font, screen)
    background.fill(BACKGROUNDCOLOR)
    playerHealthPos = Rect(30, 30, 30, screen.get_size()[1]//255*255)
    enemyHealthPos = Rect(screen.get_size()[0]-60, 30, 30, screen.get_size()[1]//255*255)
    pygame.draw.rect(background, ((0, 0, 255)), playerHealthPos)
    pygame.draw.rect(background, (0, 0, 255), enemyHealthPos)
    if(not opening):
        drawText("Player Health", background, font, 60, screen.get_size()[1]/2 - 100, screen)
        drawText("Enemy Health", background, font, screen.get_size()[0]  /8*7, screen.get_size()[1]/2 - 100, screen)
        drawCenteredText("Wait a moment!", background, font, screen.get_size()[1]-80, screen)
    else:
        print("first reset")
    letters = updateLetters()
    screen.blit(background, (0,0))
    return letters

# Draws a set of centered instructions for use in the starting and game over screens
def drawInstructions(background, font, screen):
    drawCenteredText("This is a test of skill and luck", background, font, 0, screen)
    drawCenteredText("You will be given an increasingly smaller amount of time to press 3 buttons in order to attack ", background, font, 40, screen)
    drawCenteredText("Should you fail to press all three, you will lose health", background, font, 80, screen)
    drawCenteredText("You do not need to press them at the same time, just press them", background, font, 120, screen)

# Draws centered text a bit less painfully
def drawCenteredText(text, background, font, height, screen):
    tempText = font.render(text, 1, (180, 180, 180))
    tempTextRect = tempText.get_rect()
    tempTextPos = Rect(0, height, tempTextRect.w, tempTextRect.h)
    centerXPos = background.get_rect().centerx
    tempTextPos.centerx = centerXPos
    background.blit(tempText, tempTextPos)
    screen.blit(background, (0,0))
    

    
# Covers text to prepare for new set of letters and updates bottom edge damage indicators
def drawBottomTextCover(background, screen, BACKGROUNDCOLOR):
    cover = Rect(screen.get_size()[0]/2 - 50000, screen.get_size()[1]-100, 100000, 100)
    cover = pygame.draw.rect(background, BACKGROUNDCOLOR, cover)
    screen.blit(screen, cover)

# Makes letter covers for when letters are pressed
def makeLetterCover(letterNum, background, screen, font):
    letterCover = font.render("—", 9, (180, 180, 180))
    letterCoverPos = Rect(screen.get_width()/2-35 + 25 * letterNum, screen.get_height()-82, 30, 40)
    background.blit(letterCover, letterCoverPos)
    screen.blit(background, (0,0))

# Runs functions that happen when a letter is pressed
def onLetterPress(lettersPressed, letterNum, background, screen, font):
    lettersPressed[letterNum-1] = True
    makeLetterCover(letterNum, background, screen, font)
    pygame.display.flip()

# Runs the Game
if __name__ == '__main__': main()
