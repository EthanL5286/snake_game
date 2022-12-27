from tkinter import *
import random
import time

#cheat code for manually setting the speed of the game to max speed
def superSpeed(event):
    global speed
    speed=10

#cheat code for allowing the player to manually grow their snake
def instantGrow(event):
    growSnake()

#replaces the golden snitch when caught
def catchSnitch():
    global goldenSnitch, goldenSnitchX, goldenSnitchY
    canvas.move(goldenSnitch, (goldenSnitchX*(-1)), (goldenSnitchY*(-1)))
    goldenSnitchX=random.randint(0,width-(snakeSize*2))
    goldenSnitchY=random.randint(0,height-(snakeSize*2))
    canvas.move(goldenSnitch, goldenSnitchX, goldenSnitchY)

#moves the golden snitch in a random location every game tick
def moveSnitch():
    global goldenSnitch, goldenSnitchX, goldenSnitchY
    canvas.move(goldenSnitch, (goldenSnitchX*(-1)), (goldenSnitchY*(-1)))
    direction=random.randint(0,4)
    if direction==0 and goldenSnitchX<(width-(snakeSize*2)):
        goldenSnitchX=goldenSnitchX+snakeSize

    elif direction==1 and goldenSnitchX>snakeSize:
        goldenSnitchX=goldenSnitchX-snakeSize
    elif direction==2 and goldenSnitchY<height-(snakeSize*2):
        goldenSnitchY=goldenSnitchY+snakeSize
    elif direction==3 and goldenSnitchY>snakeSize:
        goldenSnitchY=goldenSnitchY-snakeSize
    canvas.move(goldenSnitch, goldenSnitchX, goldenSnitchY)

#Spawns the golden snitch
def placeSnitch():
    global goldenSnitch, goldenSnitchX, goldenSnitchY
    goldenSnitch = canvas.create_rectangle(0,0, snakeSize, snakeSize, fill="gold")
    goldenSnitchX=random.randint((snakeSize*2),width-(snakeSize*2))
    goldenSnitchY=random.randint((snakeSize*2),height-(snakeSize*2))
    canvas.move(goldenSnitch, goldenSnitchX, goldenSnitchY)

#displays the leaderboard
def displayLeaderboard():
    leaderboard=open("leaderboard.txt", "r")
    leaderboard=leaderboard.read()
    canvas.create_text(width/2, (height/2)-30, fill="white", font="Times 20 italic bold", text=leaderboard)
    canvas.create_text(width/2, (height/2)+100, fill="white", font="Times 20 italic bold", text="Press enter to return to menu")

    canvas.pack()



#updates the leaderboard if a new high score is reached
def leaderboard():
    global score
    leaderboard=open("leaderboard.txt", "r")
    leaderboard=leaderboard.read()
    leaderboard=leaderboard.split()
    for i in range(1, len(leaderboard),2):
        score_list.append(leaderboard[i])
    for i in range(0, len(leaderboard),2):
        player_list.append(leaderboard[i])

    leaderboard=open("leaderboard.txt", "w")
    update=False
    for i in range(0, len(score_list)):
        if update==True:
            leaderboard.write(player_list[i-1])
            leaderboard.write(" ")
            leaderboard.write(score_list[i-1])
            leaderboard.write("\n")
        elif int(score_list[i])<=score:
            leaderboard.write(username)
            leaderboard.write(": ")
            leaderboard.write(str(score))
            leaderboard.write("\n")
            update=True
        else:
            leaderboard.write(player_list[i])
            leaderboard.write(" ")
            leaderboard.write(score_list[i])
            leaderboard.write("\n")

#Adds an element to the snake when it has eaten food
def growSnake():
    global snake
    global speed
    speed=float(speed-0.5)
    if speed<=10:
        speed=10
    lastElement=len(snake)-1
    lastElementPos = canvas.coords(snake[lastElement])
    snake.append(canvas.create_rectangle(0, 0, snakeSize, snakeSize, fill="#FDF3F3"))
    if direction=="left":
        canvas.coords(snake[lastElement+1], lastElementPos[0]+snakeSize, lastElementPos[1], lastElementPos[2]+snakeSize, lastElementPos[3])
    elif direction=="right":
        canvas.coords(snake[lastElement+1], lastElementPos[0]-snakeSize, lastElementPos[1], lastElementPos[2]-snakeSize, lastElementPos[3])
    elif direction=="up":
        canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1]+snakeSize, lastElementPos[2], lastElementPos[3]+snakeSize)
    else:
        canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1]-snakeSize, lastElementPos[2], lastElementPos[3]-snakeSize)
    global score
    global txt
    score=score+10
    txt="Score:" + str(score)
    canvas.itemconfigure(scoreText, text=txt)



#Collision detection function
def overlapping(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False

#Moves the food when overlapping=True
def moveFood():
    global food, foodX, foodY
    canvas.move(food, (foodX*(-1)), (foodY*(-1)))
    foodX = random.randint(0,width-snakeSize)
    foodY = random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)

#Movement of snake
def moveSnake():
    global snake
    global speed
    global gameState
    moveSnitch()
    canvas.pack()
    positions=[]
    positions.append(canvas.coords(snake[0]))
    if hardMode==True:
        if positions[0][0]<0 or positions[0][2]>width or positions[0][3]>height or positions[0][1]<0:
            gameState="Over"

    else:

        if positions[0][0]<0:
            canvas.coords(snake[0], width, positions[0][1], width-snakeSize, positions[0][3])
        elif positions[0][2]>width:
            canvas.coords(snake[0], 0-snakeSize, positions[0][1], 0, positions[0][3])
        elif positions[0][3]>height:
            canvas.coords(snake[0], positions[0][0], 0-snakeSize, positions[0][2], 0)
        elif positions[0][1]<0:
            canvas.coords(snake[0], positions[0][0], height, positions[0][2], height-snakeSize)
    positions.clear()
    positions.append(canvas.coords(snake[0]))
    if direction=="left":
        canvas.move(snake[0], -snakeSize, 0)
    elif direction=="right":
        canvas.move(snake[0], snakeSize, 0)
    elif direction=="up":
        canvas.move(snake[0], 0, -snakeSize)
    elif direction=="down":
        canvas.move(snake[0], 0, snakeSize)
    sHeadPos=canvas.coords(snake[0])
    foodPos=canvas.coords(food)
    snitchPos=canvas.coords(goldenSnitch)
    if overlapping(sHeadPos, foodPos):
        moveFood()
        growSnake()
    if overlapping(sHeadPos, snitchPos):
        catchSnitch()
        for i in range(0,5):
            growSnake()

    for i in range(1, len(snake)):
        if overlapping(sHeadPos, canvas.coords(snake[i])):
            gameState="Over"
            break

    if gameState=="Over":
        window.destroy()

    else:
        for i in range(1, len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake)-1):
            canvas.coords(snake[i+1], positions[i][0], positions[i][1], positions[i][2], positions[i][3])
        window.after(int(speed), moveSnake)


#Spawns the food in
def placeFood():
    global food, foodX, foodY
    food = canvas.create_rectangle(0,0, snakeSize, snakeSize, fill="steelblue")
    foodX=random.randint(0,width-snakeSize)
    foodY=random.randint(0,height-snakeSize)
    canvas.move(food, foodX, foodY)

#Key bindings
def leftKey(event):
    global direction
    direction = "left"
def rightKey(event):
    global direction
    direction = "right"
def upKey(event):
    global direction
    direction = "up"
def downKey(event):
    global direction
    direction = "down"

def returnKey(event):
    window.destroy()

def newGameKey(event):
    global gameState
    global hardMode
    hardMode=False
    window.destroy()
    gameState="Game"

def continueKey(event):
    global gameState
    global hardMode
    hardMode=False
    window.destroy()
    gameState="Game"
    global continued
    continued=True

def leaderboardKey(event):
    global gameState
    window.destroy()
    gameState="Leaderboard"

def endKey(event):
    global gameState
    window.destroy()
    gameState="End"

def pause(event):
    global gameState
    gameInfo=open("gameInfo.txt", "w")
    gameInfo.write(str(score))
    gameInfo.close()
    gameSpeed=open("gameSpeed.txt", "w")
    gameSpeed.write(str(speed))
    gameSpeed.close()
    window.destroy()
    gameState="Menu"

def bossMode(event):
    global gameState
    gameInfo=open("gameInfo.txt", "w")
    gameInfo.write(str(score))
    gameInfo.close()
    window.destroy()
    gameState="Boss"

def hardModeKey(event):
    global gameState
    global hardMode
    hardMode=True
    window.destroy()
    gameState="Game"



#Window start up routine
def setWindowDimensions(w,h):
    window=Tk()
    window.title("Snake Game")
    ws=window.winfo_screenwidth()
    hs=window.winfo_screenheight()
    x=(ws/2)-(w/2)
    y=(hs/2)-(h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


global width
global height
width=1280
height=720

#Lets the user choose a username and key bindings
loop=True
global username
while loop==True:
    username=input("Please input a username without any spaces: ")
    if username.find(" ")==-1:
        loop=False
    else:
        loop=True
loop=True
while loop==True:
    key_bindings=input("Which keys would you like to use to play: 1) Arrow keys or 2) WASD keys: ")
    if key_bindings=="1":
        keys="Arrow"
        loop=False
    elif key_bindings=="2":
        keys="WASD"
        loop=False
    else:
        loop=True






#gameState loop so that the game can change between states while playing
global gameState
gameState="Menu"
continued=False
while True:

    #menu screen
    if gameState=="Menu":
        window=setWindowDimensions(width, height)
        canvas=Canvas(window, bg="black", width=width, height=height)
        canvas.create_text(width/2, (height/2)-20, fill="white", font="Times 20 italic bold", text="Press 1 to start new game")
        canvas.create_text(width/2, (height/2), fill="white", font="Times 20 italic bold", text="Press 2 to continue a paused game")
        canvas.create_text(width/2, (height/2)+20, fill="white", font="Times 20 italic bold", text="Press 3 to start Hard Mode - walls are boundaries and no saves or cheats!")
        canvas.create_text(width/2, (height/2)+40, fill="white", font="Times 20 italic bold", text="Press 4 to view the leaderboard")
        canvas.create_text(width/2, (height/2)+60, fill="white", font="Times 20 italic bold", text="Press 5 to exit the game")

        canvas.bind("1", newGameKey)
        canvas.bind("2", continueKey)
        canvas.bind("3", hardModeKey)
        canvas.bind("4", leaderboardKey)
        canvas.bind("5", endKey)
        canvas.focus_set()

        canvas.pack()
        window.mainloop()

    #shows the leaderboard
    if gameState=="Leaderboard":
        window=setWindowDimensions(width, height)
        canvas=Canvas(window, bg="black", width=width, height=height)
        displayLeaderboard()
        canvas.bind("<Return>", returnKey)
        canvas.focus_set()

        displayLeaderboard()
        canvas.pack()
        window.mainloop()
        gameState="Menu"

    #exits the game when the player choses
    if gameState=="End":
        exit()

    #runs when the player loses
    if gameState=="Over":
        window=setWindowDimensions(width, height)
        canvas=Canvas(window, bg="black", width=width, height=height)
        canvas.create_text(width/2, height/2, fill="white", font="Times 20 italic bold", text="Game Over!")
        canvas.create_text(width/2, (height/2)+30, fill="white", font="Times 20 italic bold", text="Press enter to continue")

        canvas.bind("<Return>", returnKey)
        canvas.focus_set()

        canvas.pack()
        window.mainloop()
        leaderboard()
        gameState="Menu"
        gameInfo=open("gameInfo.txt", "w")
        gameInfo.write("0")
        gameInfo.close()
        global score
        score=0

    #Boss mode for when the user pretends they are working
    if gameState=="Boss":
        window=setWindowDimensions(width,height)
        canvas=Canvas(window, bg="black", width=width, height=height)
        img = PhotoImage(file="BossMode.PNG")
        bgImage=Label(window, image=img)
        bgImage.place(x=0, y=0, width=width, height=height)
        canvas.bind("<Return>", returnKey)
        canvas.focus_set()
        canvas.pack()
        window.mainloop()
        gameState="Menu"

    #main game loop
    if gameState=="Game":
        window=setWindowDimensions(width,height)

        canvas=Canvas(window, bg="black", width=width, height=height)


        global snake
        snake=[]
        global snakeSize
        snakeSize=15
        snake.append(canvas.create_rectangle(snakeSize,snakeSize, snakeSize * 2, snakeSize * 2, fill="white" ))

        score=0
        global score_list
        score_list=[]
        global player_list
        player_list=[]
        global txt
        global speed
        speed=90
        if keys=="Arrow":
            canvas.bind("<Left>", leftKey)
            canvas.bind("<Right>", rightKey)
            canvas.bind("<Up>", upKey)
            canvas.bind("<Down>", downKey)
        else:
            canvas.bind("<a>", leftKey)
            canvas.bind("<d>", rightKey)
            canvas.bind("<w>", upKey)
            canvas.bind("<s>", downKey)
        if hardMode==False:
            canvas.bind("<space>", pause)
            canvas.bind("<Return>", bossMode)
            canvas.bind("<g>", instantGrow)
            canvas.bind("<p>", superSpeed)
        canvas.focus_set()

        direction="right"

        if continued==True:
            gameInfo=open("gameInfo.txt", "r")
            gameInfo=gameInfo.read()
            score=int(gameInfo)
            txt="Score:" + str(score)
            scoreText = canvas.create_text(width/2, 10, fill="black", font="Times 20 italic bold", text=txt)
            snakeLength=int(score/10)
            for i in range(0, snakeLength):
                growSnake()

            score=int(snakeLength*10)
            gameSpeed=open("gameSpeed.txt", "r")
            gameSpeed=gameSpeed.read()
            speed=float(gameSpeed)
            continued=False
        txt="Score:" + str(score)
        scoreText = canvas.create_text(width/2, 10, fill="white", font="Times 20 italic bold", text=txt)


        placeFood()
        placeSnitch()
        moveSnake()



        window.mainloop()
