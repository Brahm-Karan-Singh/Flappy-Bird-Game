import random   #For generating random numbers
import sys       #We will use sys.exit to exit the program
import pygame
from pygame.locals import *     #Basic pygame imports

#Global Variables for the game
FPS = 32
SCREENWIDTH =590
SCREENHEIGHT = 560
SCREEN = pygame.display.set_mode(size=(SCREENWIDTH, SCREENHEIGHT))  #Pygame gives us the screen for our game with given height and width
BASEY = SCREENHEIGHT * 0.8      #Ground on the y axis will be 80% of screenheight
GAME_SPRITES = {}   #Dictionary for images used in the game
GAME_SOUNDS = {}    #Dictionary for sounds used in the game
PLAYER = 'gallery/sprites/bird.png'             #give relative path of image of player
BACKGROUND ='gallery/sprites/background.png'     #give relative path of image of background
PIPE = 'gallery/sprites/pipe.png'               #give relative path of image of pipe


def welcomeScreen():
    playerx=int(SCREENWIDTH//5)       #setting x coord of player from top left corner
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)   #setting y coord of player from top left corner
    messagex= 0  #setting x coord of message from top left corner
    messagey=0   #setting y coord of message from top left corner
    basex=0     #setting x coord of base from top left corner

    while True:
        # SCREEN.blit(GAME_SPRITES['background'],(0,0))   #blit means pasting of given picture at given coords
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
        SCREEN.blit(GAME_SPRITES['base'],(basex,BASEY))
        pygame.display.update()    #Updates the display screen and shows the images
        FPSCLOCK.tick(FPS)         #Sets the fps clock that it does not exceeds given fps
    # pygame.event.get()= Gets the event from the keyboard typed by the user
        for event in pygame.event.get():
        # event.type== Quit that is cross on right top or 
        #   event.type==KEYDOWN means that some key is pressed 
        #   event.key== Symbol of various keys . Check pygame documentation
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()     #Exits from the python function
        
            elif event.type==KEYDOWN and event.key==K_SPACE:
                return

            else:
                continue
                
        

def mainGame():
    score =0
    playerx= int(SCREENWIDTH/5)  #Can be error
    playery= int(SCREENWIDTH/2)#changed
    basex=0

    newpipe1= getRandomPipe()
    newpipe2= getRandomPipe()

    #Can be error
    #As we are blitting 2 pipes at a time thats why we have taken two upper pipes and called two times getRandomPipe function
    upperPipes=[
        {'x':(SCREENWIDTH+200) ,'y':newpipe1[0]['y']},
        {'x':(SCREENWIDTH+200)+(SCREENWIDTH/2) ,'y':newpipe2[0]['y']}
    ]

    lowerPipes=[
        {'x':(SCREENWIDTH+200) ,'y':newpipe1[1]['y']},
        {'x':(SCREENWIDTH+200)+(SCREENWIDTH/2) ,'y':newpipe2[1]['y']}
    ]

    pipeVelx = -4    #Velocity of pipe moving minus because moving backwords
    playerVely = -9      #Velocity of player moving
    playerMaxVely = 10   #Max Velocity of player moving
    playerMinVely = -8   #Min Velocity of player moving
    playerAccy = 1       #Acceleration of player moving

    playerFlapVely=-8     #Velocity while flapping
    playerFlapped=False   #When our bird or player will flap then it will become true

    while True:   #Game loop
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type ==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery >0:
                    playerVely=playerFlapVely #As the bird is flapping equate the velocity of flapping player to the players velocity
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
        
        crashTest = isCollide( playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return

        playerMidPos= playerx + GAME_SPRITES['player'].get_width()/2

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2

            if pipeMidPos <= playerMidPos <pipeMidPos+4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
             
             #IF the player is not flapping then increase its speed
        if playerVely<playerMaxVely and not playerFlapped:
            playerVely+=playerAccy
            
            # Make it false for next iteration otherwise player once pressed up key it will always be true
        if playerFlapped:
            playerFlapped=False

        playerHeight=GAME_SPRITES['player'].get_height()
        #Now time to change the playery so that it does not go below the base

        # BASEY-playerHeight-playery will become zero when player touches the base, you can check
        playery=playery + min(playerVely, BASEY-playerHeight-playery)

        #Move pipe to the left

        #Zip function-->
        # a=[1,2,3,4];b=[5,6,7,8] then zip(a,b)=[(1,5),(2,6),(3,7),(4,8)]
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            #Moving pipe to the left by adding minus value
            upperPipe['x']+=pipeVelx
            lowerPipe['x']+=pipeVelx

        #Adding a new pipe when our pipe is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #Deleting the pipe when crossed the leftmost  part of the screen
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        #Now lets blit our game sprites
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        SCREEN.blit(GAME_SPRITES['base'],(basex,BASEY))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        myDigits=[int(x) for x in list(str(score))] #Will return a list of my score
        width=0
        #Finding width of our total no. to find the centerpoint of the screen wrt to the digits
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        centreOfScreenx= (SCREENWIDTH - width)/2
         #Displaying our digits on screen
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(centreOfScreenx,SCREENHEIGHT*0.12))
            centreOfScreenx+=GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide( playerx,playery,upperPipes,lowerPipes):
    #Checking whether the player touches the ground or touches the upper part of the screen
    if playery>BASEY - 36 or playery<0:   #we minus 25 because the height of the player is 25
        GAME_SOUNDS['hit'].play()
        return True

    #Now check for both upper and lower pipes
    for pipe in upperPipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if (playery < (pipeHeight+pipe['y']) and abs(playerx - pipe['x'])<(GAME_SPRITES['pipe'][0].get_width()-2)):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if(((playery + GAME_SPRITES['player'].get_height())> pipe['y']) and abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    PIPEHEIGHT=GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    pipex= SCREENWIDTH + 10
    y2 = random.randrange( 0, int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset)) + offset
    y1=PIPEHEIGHT - y2 + offset   

    pipe=[
        {'x':pipex , 'y':-y1} , #FOR upper pipes
        {'x':pipex , 'y':y2}  #FOR lower pipes    
    ]
    return pipe


if __name__ == "__main__":
    #This will be the main function from where our game will start
    pygame.init()     #Initializes all modules of pygame
    FPSCLOCK = pygame.time.Clock()      #will control fps of game
    pygame.display.set_caption('Flappy Bird by Brahm Karan Singh')

    #Game images
    #We are making key of numbers and value will be a tuple of numbers with their paths
    GAME_SPRITES['numbers'] = (
        #It will load image and convert alpha func will make your photo optimised for our game and for quick blitting ie rendering your image on screen
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()

    GAME_SPRITES['pipe'] =(
         #It will rotate your image as we want two pipes. It takes two arguments --> image, angle of rotation
         pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
         pygame.image.load(PIPE).convert_alpha()
    )

    
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()
    
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()

#Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/sfx_die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/sfx_hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/sfx_point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/sfx_swooshing.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/sfx_wing.wav')

    while True:
        welcomeScreen()   #Shows welcome screen to the user until he presses a button
        mainGame()        #This is the main game function


