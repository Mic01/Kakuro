#Title: Kakuro
#Author: Michaiah Thoms
#Date: 16/05/2018
#Version: 3

#7.5 hours for achieved
#5.5 hours for merit
#7 hours for excellence
#20 Hours Total

#Import necessary modules
from tkinter import *
from random import *

#Create window, set up initial variables and create the menu
def main():
    global root, main_canvas, main_size, active_canvas

    root = Tk()
    root.title("Kakuro V3")
    #Prevent user from resizing window
    root.resizable(False, False)
    #Determines size of entire window and its contents based off of the users screen size
    main_size = (root.winfo_screenheight())-100
    print(main_size)
    #Sets where the window appears when the program runs
    root.geometry('%dx%d+%d+%d' % (main_size, main_size, root.winfo_screenwidth()/2-main_size/2, root.winfo_screenheight()/2-main_size/1.85))
    active_canvas = ""
    #Retrieve scores from their files
    getscores()

    main_canvas = Canvas(root, width=main_size, height=main_size, bg="white")
    main_canvas.pack()
    #Prevent auto-resizing to fit content
    main_canvas.pack_propagate(False)

    #Bind necessary keys to the main canvas for button functionality
    bindkeys(main_canvas)
    #Create the menu
    create_menu()

#Quit the program
def quit():
    root.destroy()

#Bind all necessary keys to supplied canvas
def bindkeys(canvas):
    #Enable python to use keyboard keys as well as mouse buttons
    canvas.focus_set()
    
    canvas.bind("<ButtonPress-1>", leftclickpress)
    canvas.bind("<ButtonRelease-1>", leftclickrelease)
    #Bind all keyboard keys to the keyboard function
    canvas.bind("<Key>", keyboard)

#Create the game menu
def create_menu():
    global active_canvas, buttons, board_canvas, timeron
    #Completely empty and reset the main canvas from any previous content
    timeron = False
    if active_canvas == "game" or active_canvas == "win":
        board_canvas.destroy()
    active_canvas = "menu"
    main_canvas.delete(ALL)
    buttons = []

    #Create title
    main_canvas.create_text(round(main_size/2), round(main_size/8), text="Kakuro", font="Franklin {} bold".format(round(70/800*main_size)))

    #Create the how to play, play, highscores and quit buttons for the menu
    y = round(210/800*main_size)
    for text, func in zip(["How To Play", "Play", "Highscores", "Quit"], [create_howtoplay, play, create_highscores, quit]):
        buttons.append(Button(main_canvas, round(250/800*main_size), y, round(300/800*main_size), text, func))
        y += round(main_size/6)
    for button in buttons:
        button.draw("white")

    #Create the text labelling this as a product of Flow Computing
    main_canvas.create_text((115/800)*main_size, main_size-((20/800)*main_size), text="@ 2018, Flow Computing LTD", font="Franklin {}".format(round(12/800*main_size)))

#Create the back and quit buttons at the top of every screen but the menu screen
def backquit():
    size = round(140/800*main_size)
    buttons.append(Button(main_canvas, 0, 0, size, "Back", create_menu))
    buttons.append(Button(main_canvas, main_size-size+4, 0, size, "Quit", quit))
    for button in buttons:
        button.draw("white")

#Create the highscores screen
def create_highscores():
    global buttons
    #Completely empty and reset the main canvas from any previous content
    main_canvas.delete(ALL)
    buttons = []
    backquit()
    getscores()

    #Create title
    main_canvas.create_text(round(main_size/2), round(main_size/8), text="Highscores", font="Franklin {} bold".format(round(70/800*main_size)))
    main_canvas.create_text(round(main_size/2), round(main_size/4), text="Score = Hours:Minutes:Seconds", font="Franklin {}".format(round(20/800*main_size)))

    #Create and populate the highscore table
    size = round(main_size/3)
    for scores, text, column in zip([escores, mscores, hscores], ["Easy", "Medium", "Hard"], range(1,4)):
        x = size*column
        y1 = main_size/3
        main_canvas.create_rectangle(x-size, y1, x, y1+size/3, width=3)
        main_canvas.create_text(x-size/2, y1+size/6, text=text, font="Franklin {} bold".format(round(30/800*main_size)))
        for score, row in zip(sorted(scores), range(2,7)):
            hours = 0
            mins = 0
            secs = score
            
            while secs >= 60:
                mins += 1
                secs -= 60
            while mins >= 60:
                hours += 1
                mins -= 60
     
            y2 = main_size/3+(size/3*row)
            main_canvas.create_rectangle(x-size, y2-size/3, x, y2)
            main_canvas.create_text(x-size/2, y2-size/6, text="{}\n{}:{}:{}".format(scores[score].title(), str(hours).zfill(2), str(mins).zfill(2), str(secs).zfill(2)), font="Arial {}".format(round(17/980*main_size)), justify=CENTER)

def create_howtoplay():
    global buttons
    #Completely empty and reset the main canvas from any previous content
    main_canvas.delete(ALL)
    buttons = []
    backquit()

    #Create title
    main_canvas.create_text(main_size/2, main_size/8, text="How to Play Kakuro", font="Franklin {} bold".format(round(50/800*main_size)))

    #Create instructions on how to play Kakuro
    text = """• Click on a white square to select it, click on the numbers along 
    the bottom or use the numbers on the keyboard to enter a number 
    into the selected square.

• The X button on the bottom and the backspace will empty the
    selected square.

• The numbers in each row and column have to add to the number
    in the triangle on each end of the row/column.

• The same number can't be used twice in the same equation.

• Only the numbers 1-9 can be used.

• Multiple numbers can be entered into a square at once for the
    purpose of note taking and will not be considered part of the
    equation

• The triangles holding the numbers for each equation will
    turn green when their equation is true and red if there is
    an error in the equation (total is wrong or multiple numbers)."""

    main_canvas.create_text(main_size/2, main_size/2.1, text=text, font="Arial {}".format(round(14/800*main_size)))
    imagefile = PhotoImage(file="howtoplay.gif")
    image = Label(image=imagefile, border=0)
    image.image = imagefile
    main_canvas.create_window(main_size/2, main_size-main_size/8, window=image)

def play():
    global buttons
    #Completely empty and reset the main canvas from any previous content
    main_canvas.delete(ALL)
    buttons = []
    backquit()

    #Create title
    main_canvas.create_text(main_size/2, main_size/5, text="Kakuro", font="Franklin {} bold".format(round(70/800*main_size)))

    #Create buttons for choosing a difficulty level
    y = round(280/800*main_size)
    for text, func in zip(["Easy", "Medium", "Hard"], [easy, medium, hard]):
        buttons.append(Button(main_canvas, 250/800*main_size, y, 300/800*main_size, text, func))
        y += round(160/800*main_size)
    for button in buttons:
        button.draw("white")

#Set difficulty of game to easy
def easy():
    global emh
    emh = "e"
    create_game()

#Set difficulty of game to medium
def medium():
    global emh
    emh = "m"
    create_game()

#Set difficulty of game to hard
def hard():
    global emh
    emh = "h"
    create_game()

#Create the game
def create_game():
    global active_canvas, main_canvas, buttons, wintest
    #Completely empty and reset the main canvas from any previous content
    active_canvas = "game"
    main_canvas.delete(ALL)
    buttons = []
    wintest = 0

    backquit()

    #Run the necessary functions to create the game
    create_board()
    create_numbuttons()
    generate_numbers()

#Creates the game board
def create_board():
    global squares, rows, columns, activesquare, selectedsquare, emh, board_canvas, timeron, hours, mins, secs, timertext, board_size
    timeron = True
    squares = []
    rows = []
    columns = []
    rowcount = 0
    colcount = 0
    hours = 0
    mins = 0
    secs = 0
    timertext = "00:00:00"

    board_size = round(673/800*main_size)
    board_canvas = Canvas(main_canvas, width=board_size, height=board_size, bg="white", highlightthickness=0)
    board_canvas.pack(pady = round(50/800*main_size))
    
    bindkeys(board_canvas)

    #Determine size of board and choose a board from the board files, based off of difficulty
    if emh == "e":
        size = round(112/800*main_size)
        boardfile = open("textfiles/eboards.txt", "r")
    elif emh == "m":
        size = round(67/800*main_size)
        boardfile = open("textfiles/mboards.txt", "r")
    elif emh == "h":
        size = round(48/800*main_size)
        boardfile = open("textfiles/hboards.txt", "r")

    boards = boardfile.readlines()
    for i in range(len(boards)):
        board = boards[i].strip().split(" ")
        templist = []
        for segment in board:
            templist.append(list(map(int, segment)))
        boards[i] = templist
    boardfile.close

    board = choice(boards)

    #Create the board using same method as Run Length Encoding aka. RLE
    rcount = 0
    for y, row in zip(range(2+size, round(690/800*main_size)-(2*size), size), board):
        rcount += 1

        x=2+size
        create_square = True

        ccount = 0
        for length in row:
            templist = []
            for i in range(length):
                ccount += 1
                if create_square:
                    tempvar = Square(board_canvas, size, x, y, rcount, ccount)
                    squares.append(tempvar)
                    templist.append(tempvar)
                x+=size

            #Assign Row Classes
            if len(templist) > 0:
                rows.append(RowColumn(board_canvas, size, "row", templist, rowcount))
                rowcount += 1

            #Alternate between creating or not creating a square, akin to RLE
            create_square = not create_square

    #Assign Column Classes
    tempcolumns = []
    for i in range(len(board)):
        tempcolumns.append([])

    for square in squares:
        tempcolumns[square.ycoord-1].append(square)

    for column in tempcolumns:
        count = 0
        templist = []
        
        for square in column:
            while True:
                count += 1
                if square.xcoord == count:
                    templist.append(square)
                    break
                else:
                    if len(templist) > 0:
                        columns.append(RowColumn(board_canvas, size, "column", templist, colcount))
                        colcount += 1
                        templist = []
                        
        if len(templist) > 0:
            columns.append(RowColumn(board_canvas, size, "column", templist, colcount))
            colcount += 1
            templist = []

    #Draw squares
    for square in squares:
        square.draw("white")

    #Error catching for user pressing numbers before selecting square
    activesquare = squares[0]
    selectedsquare = False

    #Start the timer
    timertext = main_canvas.create_text(round(main_size/2), 30, text="", font="Arial {}".format(round(30/800*main_size)))
    timer()

#Creates and runs the timer  above the game board, keeping track of the time taken
def timer():
    global secs, mins, hours, timertext
    if active_canvas == "game" or active_canvas == "win":
        #Updates the timer
        main_canvas.delete(timertext)
        time = "{}:{}:{}".format(str(hours).zfill(2), str(mins).zfill(2), str(secs).zfill(2))
        timertext = main_canvas.create_text(round(main_size/2), 30, text=time, font="Arial {}".format(round(30/800*main_size)))
        #Adds a second to the timer and changes the mins/hours variables accordingly
        if timeron:
            secs+=1
        
            if secs == 60:
                secs = 0
                mins += 1
            if mins == 60:
                mins = 0
                hours += 1
            #Repeats the function after 1 second
            main_canvas.after(1000, timer)
    
#Creates buttons 1-9 and X
def create_numbuttons():
    global numbuttons
    numbuttons = []
    size = round(67/800*main_size)
    
    for i in range(1,11):
        if i == 10:
            text = "X"
        else:
            text = i

        numbuttons.append(NumButton(main_canvas, size, i, text))

    for button in numbuttons:
        button.draw("white")

#Generates the totals that need to be met in triangles
def generate_numbers():
    try:
        for square1 in squares:
            randnum = choice(square1.potnumbers)
            square1.answer = randnum
            square1.potnumbers = []

            for rowcols in [rows, columns]:
                for rowcol in rowcols:
                    for square2 in rowcol.squares:
                        if square2.xcoord == square1.xcoord and square2.ycoord == square1.ycoord:
                            for square3 in rowcol.squares:
                                if randnum in square3.potnumbers:
                                    square3.potnumbers.remove(randnum)
                            break
                    else:
                        continue
                    break

        for rowcols in [rows, columns]:
            for rowcol in rowcols:
                rowcol.findanswer()
    #In the rare instance that an invalid set of numbers are generated it re-creates the game 
    except IndexError:
            board_canvas.destroy()
            create_game()
    
#Creates the win screen for the user to input their name to store their score
def create_win():
    global timeron, active_canvas, name, wintitle
    active_canvas = "win"
    bindkeys(board_canvas)
    timeron = False
    getscores()
    #Find sizes for everything
    size=round(300/800*board_size)
    x=round((board_size/2)-(size/2))
    y=round((board_size/2)-(size/6))
    bigfont = "Arial {}".format(round(36/300*size))
    smallfont = "Arial {}".format(round(13/300*size))
    #Create text and box
    board_canvas.create_rectangle(x, y, x+size, y+size/1.5, outline = "black", fill="lightgreen", width=4)
    wintitle = board_canvas.create_text(x+size/2, y+size/6, text="You Win!", font=bigfont)
    board_canvas.create_text(x+size/2, y+size/2.5, text="Enter your name (max 16 characters)\n            Press Enter to Submit", font=smallfont)
    #Create entry
    score_entry = Entry(board_canvas, font=smallfont)
    score_entry.bind("<Return>", submit_score)
    board_canvas.create_window(board_size/2, (board_size/2)+(size/2.5), window=score_entry, width=size-8)


#Stores the users score if it bests the top 5 times of the difficulty they played
def submit_score(event):
    global wintitle
    scorelist = [escores, mscores, hscores]
    name = event.widget.get().strip().lower()
    #Check that the inputted name is valid
    if 0 < len(name) < 17 and len([i for i in list(name.replace(" ","")) if i not in list("abcdefghijklmnopqrstuvwxyz")]) == 0:
        score = secs + mins*60 + hours*60*60
        if emh == "e":
            scoredict = 0
        elif emh == "m":
            scoredict = 1
        elif emh == "h":
            scoredict = 2
        #Adds a second to the users score if it is the same as another score to prevent errors
        while score in scorelist[scoredict]:
            score+=1
        #Adds users score to the current dictionary of scores    
        scorelist[scoredict][score]=name
        #Removes lowest score from the list of scores
        if len(scorelist[scoredict]) > 5: del scorelist[scoredict][sorted(scorelist[scoredict])[-1]]
        savescores()
        create_menu()
    #Tell the user their name is invalid
    else:
        board_canvas.itemconfig(wintitle, text="Invalid Name", fill="red")
        board_canvas.after(3000, resetwintitle)

#Changes the title of the win screen back to 'you win' after 3 seconds after it changes to 'invalid name'
def resetwintitle():
    global wintitle
    board_canvas.itemconfig(wintitle, text="You Win!", fill="black")

#Retrieve scores from their files
def getscores():
    global escores, mscores, hscores
    escores = {}
    mscores = {}
    hscores = {}
    scorelist = [escores, mscores, hscores]
    for difficulty, scores in zip(['e', 'm', 'h'], [escores, mscores, hscores]):
        scorefile = open("textfiles/{}scores.txt".format(difficulty), "r")
        templist = scorefile.readlines()
        for data in templist:
            data = data.split(" ")
            score = int(data.pop(-1))
            name = " ".join(data)
            scores[score] = name
        scorefile.close()
    #Ensures there is only 5 scores stored in the files
    for scoredict in scorelist:
        while len(scoredict) > 5:
            del scoredict[sorted(scoredict)[-1]]
    savescores()

#Saves any new scores to the score files
def savescores():
    for scoredict, scoreletter in zip([escores, mscores, hscores], ["e", "m", "h"]):
        file = open("textfiles/{}scores.txt".format(scoreletter), "w")
        for score in sorted(scoredict):
            file.write("{} {}\n".format(scoredict[score].lower(), score))
        file.close()

#React to the numkeys and backspace being pressed
def keyboard(event):
    key = event.char
    if key in ['1','2','3','4','5','6','7','8','9']:
        key=int(key)
        key=numbuttons[key-1]
        leftclick("press", key.x+1, key.y+1)
        leftclick("release", key.x+1, key.y+1)
    if key =="":
        key=numbuttons[-1]
        leftclick("press", key.x+1, key.y+1)
        leftclick("release", key.x+1, key.y+1)

#Different functions for leftclick press and release to create a 'pressed' button graphic
def leftclickpress(event):
    global clickx, clicky
    clickx = event.x
    clicky = event.y
    leftclick("press", clickx, clicky)

def leftclickrelease(event):
    leftclick("release", clickx, clicky)

#React to where the user clicked
def leftclick(state, x, y):
    global activesquare, selectedsquare, activecolour
    activecolour = "#d5e8d4"

    if active_canvas == "game":
        #Pressing numbutton to enter number into selected square, or X button to clear a square
        for button in numbuttons:
            if (button.x <= x <= button.x+button.size) and (button.y <= y <= button.y+button.size):
                if state == "press":
                    button.draw(activecolour)
                if state == "release":
                    button.draw("white")
                    
                    if selectedsquare:
                        if button.text == "X":
                            activesquare.clear()
                        else:
                            activesquare.addnum(button.text)

                        #Check whether row and column containing activesquare have a full equation
                        rows[activesquare.rowid].check()
                        columns[activesquare.columnid].check()
                break
                                
        #Selecting square to enter a number into it
        for square in squares:
            if (square.x <= x <= square.x+square.size) and (square.y <= y <= square.y+square.size):
                if state == "press":
                    selectedsquare = True
                    activesquare.draw("white")
                    square.draw(activecolour)
                    activesquare = square
                break

    for button in buttons:
        if (button.x <= x <= button.x+button.size) and (button.y <= y <= button.y+button.size/3):
            if state == "press":
                button.draw(activecolour)
            if state == "release":
                button.draw("white")
                button.func()
#Class used to create each button
class Button:
    def __init__(self, canvas, x, y, size, text, func):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.text = text
        self.func = func
    #Draw this button
    def draw(self, colour):
        size = self.size
        x = self.x
        y = self.y
        
        self.canvas.create_rectangle(x, y, x+size, y+size/3, fill=colour, width=4)
        self.canvas.create_text(x+size/2, y+size/6, text=self.text, font="Arial {}".format(round(36/300*size)))

#Class used to create each square on the game board
class Square:
    def __init__(self, canvas, size, x, y, xcoord, ycoord):
        self.canvas = canvas
        self.size = size
        self.x = x
        self.y = y
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.potnumbers = [1,2,3,4,5,6,7,8,9]
        self.numbers = []
        self.answer = 0
        self.rowid = 0
        self.columnid = 0
        if emh == "h":
            self.width = 1
        else:
            self.width = 2
    #Draw the square
    def draw(self, colour):
        size = self.size
        x = self.x
        y = self.y
        self.canvas.create_rectangle(x, y, x+size, y+size, fill=colour, outline="black", width=self.width)
        if len(self.numbers) == 1:
            self.canvas.create_text(x+size/2, y+size/2, text=self.numbers[0], font="Arial {}".format(round(size*(26/67))))
        if len(self.numbers) > 1:
            text = ["  ","  ","  ","  ","  ","  ","  ","  ","  "]
            for num in self.numbers:
                text[num-1] = num
            self.canvas.create_text(x+size/2, y+size/2, text="{} {} {}\n{} {} {}\n{} {} {}".format(text[0],text[1],text[2],text[3],text[4],text[5],text[6],text[7],text[8]), font="Arial {}".format(round(size*(14/67))))
    #Add/remove numbers from this square
    def addnum(self, num):
        if num in self.numbers:
            self.numbers.remove(num)
        else:
            self.numbers.append(num)
        self.numbers.sort()
        self.draw(activecolour)

    def clear(self):
        self.numbers=[]
        self.draw(activecolour)

#Class used to organise the squares into rows/columns, create the triangles, and find the answers
class RowColumn:
    def __init__(self, canvas, size, rowcol, squares, rowcolid):
        self.canvas = canvas
        self.size = size
        self.rowcol = rowcol
        self.squares = squares
        self.answer = 0
        self.rowcolid = rowcolid
        self.win = "n"
        #Determine border width of triangles based off of difficulty of game
        if emh == "h":
            self.width = 1
        else:
            self.width = 2
        #Distribute id's to the squares passed into this object
        for square in self.squares:
            if self.rowcol == "row":
                square.rowid = rowcolid
            if self.rowcol == "column":
                square.columnid = rowcolid 
    #Draw the triangles
    def draw(self, colour):
        size = self.size
        x=self.squares[0].x
        y=self.squares[0].y
        font="Arial {} bold".format(round(size*(12/67)))
        width = self.width
        answer = self.answer
        
        if self.rowcol == "row":
            self.canvas.create_polygon(x, y, x, y+size, x-size/2, y+size/2, fill=colour, outline="black", width=width)
            self.canvas.create_text(x-size/5, y+size/2, text=answer, font=font)
            x=self.squares[-1].x
            y=self.squares[-1].y
            self.canvas.create_polygon(x+size, y, x+size, y+size, x+size*1.5, y+size/2, fill=colour, outline="black", width=width)
            self.canvas.create_text(x+size*1.20, y+size/2, text=answer, font=font)

        if self.rowcol == "column":
            self.canvas.create_polygon(x, y, x+self.size, y, x+self.size/2, y-self.size/2, fill=colour, outline="black", width=width)
            self.canvas.create_text(x+self.size/2, y-self.size/5, text=answer, font=font)
            x=self.squares[-1].x
            y=self.squares[-1].y
            self.canvas.create_polygon(x, y+self.size, x+self.size, y+self.size, x+self.size/2, y+self.size*1.5, fill=colour, outline="black", width=width)
            self.canvas.create_text(x+self.size/2, y+self.size*1.20, text=answer, font=font)
    #Find the answer to put in the triangles
    def findanswer(self):
        for square in self.squares:
            self.answer += square.answer
        self.draw("#e6e6e6")
    #Check if the squares in this row/column add correctly to the answer
    def check(self):
        check = 0
        dupecheck = []
        run = True
        for square in self.squares:
            if len(square.numbers) > 1 or len(square.numbers) == 0:
                self.draw("#e6e6e6")
                self.wintest("n")
                run = False
            else:
                dupecheck.append(square.numbers[0])
                if dupecheck.count(square.numbers[0]) > 1:
                    self.draw("red")
                    self.wintest("n")
                    run = False
                    break
                check += square.numbers[0]
        if run:
            if check == self.answer:
                self.draw("lightgreen")
                self.wintest("y")
            else:
                self.draw("red")
                self.wintest("n")
    #Update the wintest variable depending on whether this row/column is correct or not
    def wintest(self, yn):
        global wintest
        if yn == "n":
            if self.win == "y":
                self.win = "n"
                wintest -= 1
        else:
            if self.win == "n":
                self.win = "y"
                wintest += 1
        if wintest == (len(rows)+len(columns)):
            create_win()

#Class used to create the buttons for inputting/deleting numbers along bottom of game board
class NumButton:
    def __init__(self, canvas, size, x, text):
        self.canvas = canvas
        self.size = size
        self.x = size*x
        self.text = text
        self.y = round(725/800*main_size)
    #Draw this button
    def draw(self, colour):
        x = self.x
        y = self.y
        size = self.size
        self.canvas.create_rectangle(x, y, x+size, y+size, width=2, fill=colour)
        self.canvas.create_text(x+size/2, y+size/2, text=self.text, font="Arial {} bold".format(round(26/800*main_size)))

#Run The Program
main()
