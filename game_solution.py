#Importing libraries
from tkinter import * #Importing Tkinter
from tkinter import messagebox
import random
import json
import sys

###############################################################################################################Global Variables##############################################################################################################
window = Tk()   #Assigning "Window" as Tkinter
global username #Variable that will store the user's username
global control_scheme   #Variable that will store the user's control scheme choice (0 = Default, 1 = Alternative)
control_scheme = 0  #Default control scheme setting

global game_paused  #Variable that will store the game's paused state
game_paused = False 

global game_started #Variable that will store the game's started state
game_started = False

global ball_position, current_score    #Variable that will store game settings
current_score = 0

#Variable that will store the name of all the levels
global level1, level2, level3, current_level 
#level1 = "test_level.json"
level2 = "checkered_level.json"  
level1 = "circle_level.json"
level3 = "all_brick_level.json"

current_level = level1  #Variable that will update and store the current level

##############################################################################################################Reusable Functions##############################################################################################################
#Function that reads from a file and returns its contents
def read_file(file_name):
    file = open(file_name,'r')
    file_text = file.read()
    file.close()
    return file_text

#Loads the previous screen and destroys the current screen
def return_to_previous_screen(current_screen,previous_screen):
    previous_screen.deiconify()
    current_screen.destroy()

#Function that writes to a file
def write_file(file_name, text):
    file = open(file_name,'w')
    file.write(text)
    file.close()

##############################################################################################################Boss Key##############################################################################################################                    
def boss_key(current_window):
    current_window.withdraw()
    boss_key_window = Toplevel(current_window)
    boss_key_window.title("Boss Key")
    boss_key_window.geometry("1920x1080")
    boss_key_window.resizable(False,False)   #Window size cant be changed

    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/boss_key.png")    #Image File Path
    boss_key_window.bg_image = bg_image  #Stops the image from being removed from memory
    label_bg = Label(boss_key_window, image=bg_image)    #Creates a label for the image
    label_bg.pack()

    boss_key_window.bind("<Control-v>", lambda event: return_to_previous_screen(boss_key_window,current_window)) #Binds the escape key to the function return_to_previous_screen

    boss_key_window.focus_force()    #Makes the window the main focus
    boss_key_window.mainloop()

#Bind the boss_key function to the 'o' key for main menu screen
window.bind("<Control-c>", lambda event: boss_key(window)) #Binds the "o" key to the function boss_key

##############################################################################################################Main Menu##############################################################################################################
#Ran when the program is started
def main_menu():
    window.title("Brick Breaker Menu") #Window Name
    window.resizable(False,False)   #Window size cant be changed
    window.geometry("1440x900+250+50")    #Recommended Resolution for entire game

    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/mainMenu_ScreenBg.png")    #Image File Path
    label_bg = Label(window, image=bg_image)    #Creates a label for the image
    label_bg.pack()

    def cheat_sheet():
        messagebox.showinfo("Cheats", "Press 'b' to slow down the ball\nPress 'n' to allow the ball to bounce off the floor") #Creates a pop up with the contents of the file

    start_btn = Button(
        window, 
        text="Start Game", 
        height=2, 
        width=20, 
        font=("Open Sans",20), 
        command= lambda: new_player_screen())   #Button will start the game
    leaderboard_btn = Button(
        window, 
        text="LeaderBoard", 
        height=2, width=20, 
        font=("Open Sans",20), 
        command= leaderboard_screen)    #Button will open a pop up with the top 10 scores
    info_btn = Button(
        window, 
        text="How To Play", 
        height=2, width=20, 
        font=("Open Sans",20), 
        command = how_to_play_instructions)   #Button will open a pop up with instructions on how to play
    load_game_btn = Button(
        window, 
        text="Load Previous Save", 
        height=2, width=20, 
        font=("Open Sans",20), 
        command= lambda: game_screen(window,True)) #Button will load the most recent game save
    settings_btn = Button(
        window, 
        text="Settings", 
        height=2, width=20, 
        font=("Open Sans",20), 
        command = lambda:setting_screen(window))  #Button will open settings
    cheats_btn = Button(
        window, 
        text="Cheats", 
        height=1, width=5, 
        font=("Open Sans",10), 
        command=cheat_sheet)  #Button will open a pop up with the list of cheat codes
    quit_btn = Button(
        window, 
        text="Quit", 
        height=2, width=20, 
        command=window.quit, 
        font=("Open Sans",20))  #Button will close the whole program

    #Placing all the buttons
    start_btn.place(x=550, y=240)
    leaderboard_btn.place(x=550, y=350)
    info_btn.place(x=550, y=460)
    settings_btn.place(x=550, y=570)  
    load_game_btn.place(x=550, y=680)
    cheats_btn.place(relx=0.9, rely=0.9)
    quit_btn.place(x=550, y=790)  

    window.mainloop()   #Loads Window

##############################################################################################################How To Play##############################################################################################################
#A function that opens a pop up with instructions on how to play
def how_to_play_instructions():
    game_info_text = read_file("txt_files/game_Info.txt") #Reads from the file "gameInfo.txt" and stores it in a variable
    messagebox.showinfo("How To Play", game_info_text) #Creates a pop up with the contents of the file

##############################################################################################################Settings##############################################################################################################
#A function that opens a settings menu
def setting_screen(previous_screen):
    global keybind1_button, keybind2_button
    previous_screen.withdraw()   #Hides the main window

    #Function that updates the control scheme
    def update_controls(num, keybind1_button, keybind2_button):
        global control_scheme
        if num == 0:
            control_scheme = 0
            #Changes the color of the buttons to indicate which control scheme is selected
            keybind1_button.config(bg="green")  
            keybind2_button.config(bg="red")
        else:
            control_scheme = 1
            #Changes the color of the buttons to indicate which control scheme is selected
            keybind1_button.config(bg="red")
            keybind2_button.config(bg="green")
        messagebox.showinfo("Controls Changed", "Controls have been changed")  # Creates a pop up telling the user that the controls have been changed

    #Create a new window for settings
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("1440x900+250+50")
    settings_window.configure(bg='lightblue')
    settings_window.resizable(False,False)   #Window size cant be changed

    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/brick_background.png")    #Image File Path
    settings_window.bg_image = bg_image  #Stops the image from being removed from memory
    label_bg = Label(settings_window, image=bg_image)    #Creates a label for the image
    label_bg.pack()

    #Creates a new label
    setting_label = Label(settings_window, text="Settings", font=("Arial",50, "bold")) 
    setting_label.place(x=550, y=100)

    #Creates a button to choose keybind1
    keybind1_button = Button(
        settings_window, 
        text=("Set move left as 'a'\n  move right as 'd'"), 
        font=("Arial",15, "bold"), 
        width=30, height=2,
        command= lambda: update_controls(0, keybind1_button, keybind2_button))    #Button will set the control scheme to 0 (Default) when clicked on (lambda)
    keybind1_button.place(x=500, y=240)

    #Creates a button to choose keybind2
    keybind2_button = Button(
        settings_window, 
        text=("Set move left as 'left arrow'\n  move right as 'right arrow'"), 
        font=("Arial",15, "bold"),  
        width=30, height=2,
        bg="red", 
        command= lambda: update_controls(1, keybind1_button, keybind2_button))   #Button will set the control scheme to 1 (Alternative) when clicked on (lambda)
    keybind2_button.place(x=500, y=390)
    
    if control_scheme == 0:
        #Changes the color of the buttons to indicate which control scheme is selected
        keybind1_button.config(bg="green")  
        keybind2_button.config(bg="red")
    else:
        #Changes the color of the buttons to indicate which control scheme is selected
        keybind1_button.config(bg="red")
        keybind2_button.config(bg="green")

    #Creates button to return to previous screen
    return_button = Button(
        settings_window, 
        text="Return", 
        font=("Arial",15, "bold"), 
        width=30, height=2, 
        command= lambda: return_to_previous_screen(settings_window,previous_screen))    #Button will return to previous screen only when clicked on (lambda)
    return_button.place(x=500, y=540)


    #Bind the boss_key function to the 'o' key for settings screen
    settings_window.bind("<Control-c>", lambda event: boss_key(settings_window)) #Binds the "o" key to the function boss_key

    settings_window.focus_force()    #Makes the window the main focus
    settings_window.protocol("WM_DELETE_WINDOW", sys.exit) #Closes the program when the window is closed
    settings_window.mainloop()  #Loads the settings window

    

##############################################################################################################UserName Screen##############################################################################################################
def new_player_screen():
    window.withdraw()   #Hides the main window

    #Create a new window for username
    new_player_window = Toplevel(window)
    new_player_window.title("Select Username")
    new_player_window.geometry("1440x900+250+50")  #Makes a smaller window for the username screen so that the design is more compact
    new_player_window.resizable(False,False)   #Window size cant be changed


    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/brick_background.png")    #Image File Path
    new_player_window.bg_image = bg_image  #Stops the image from being removed from memory
    label_bg = Label(new_player_window, image=bg_image)    #Creates a label for the image
    label_bg.pack()

    #Creates a label
    name_label = Label(
        new_player_window, 
        text="Enter your name:", 
        font=("Arial", 24))
    name_label.place(relx=0.5, rely=0.1, anchor=CENTER)  #Centers the label

    #Creates an input box for the user to enter their name 
    name_input = Entry(new_player_window, font=("Arial", 24)) 
    name_input.place(relx=0.5, rely=0.4, anchor=CENTER)  #Centers the input box

    #Create a button to submit the player's name
    submit_button = Button(
        new_player_window, 
        text="Submit", 
        font=("Arial",15, "bold"), 
        width=30, height=2, 
        command= lambda: submit_username()) 
    submit_button.place(relx=0.5, rely=0.7, anchor=CENTER) #Centers the button
    
    #Creates button to return to previous screen
    return_button = Button(
        new_player_window, 
        text="Return", 
        font=("Arial",15, "bold"), 
        width=30, height=2, 
        command= lambda: return_to_previous_screen(new_player_window,window))    #Button will return to previous screen only when clicked on (lambda)
    return_button.place(relx=0.5, rely=0.9, anchor=CENTER) #Centers the button

    #Bind the boss_key function to the 'o' key for username screen
    new_player_window.bind("<Control-c>", lambda event: boss_key(new_player_window)) #Binds the "o" key to the function boss_key

    
    def submit_username():
        global username #Allows the variable to be used outside of the function
        username = name_input.get()
        if username and len(username) <= 8 and username.isalnum() == True:  #Check if the user has entered a name, name is appropriate length and only contains letters and numbers 
            game_screen(new_player_window,False)   #Loads the game screen
        else:
            instructions_text = read_file("txt_files/username_instructions.txt") #Reads from the file "username_instructions.txt" and stores it in a variable
            messagebox.showwarning("Invalid UserName", instructions_text) #Creates a pop up with the contents of the file
            error_label = Label(
                new_player_window, 
                text="Please enter a valid name", 
                font=("Arial", 16), fg="red")
            error_label.place(relx=0.5, rely=0.6, anchor=CENTER)  #Display an error message if the user has not entered a valid name
            
    new_player_window.focus_force()    #Makes the window the main focus
    new_player_window.protocol("WM_DELETE_WINDOW", sys.exit) #Closes the program when the window is closed
    new_player_window.mainloop()   #Loads the username window

##############################################################################################################Game Screen##############################################################################################################
def game_screen(previous_window,load_save):
    if previous_window != window:    #If the previous window is the main menu
        previous_window.destroy()   #Hides the previous window
    elif previous_window == window: #If the previous window is the main menu
        window.withdraw()   #Hides the main window

    global game_ended, score_label   #Variable that will store the game's ended state
    game_ended = False

    global enable_bounce
    enable_bounce = False
    #Create a new window for the main game
    maingame_window = Toplevel(window)
    maingame_window.title("Ball Breaker")
    maingame_window.geometry("1440x900+250+50") 
    maingame_window.resizable(False,False)   #Window size cant be changed

    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/maingame_screen.png")    #Image File Path
    maingame_window.bg_image = bg_image  #Stops the image from being removed from memory

    #Generating the background image
    game_canvas = Canvas(maingame_window, width=1440, height=900)  #Creating base for the paddle
    game_canvas.create_image(0, 0, image=bg_image, anchor='nw')  #Set the background image on the canvas

    ###################################Loading Levels###################################
    def make_bricks(level_name):
        global current_score, ball_speed_x, ball_speed_y, ball_position, username, paddle_position
        #Loads the brick configurations from the JSON file
        with open("levels/"+level_name, 'r') as f:                       #Information from https://www.youtube.com/watch?v=__mZO-53PPM#
            data = json.load(f) #Variable that stores the data

        if load_save == True:    #If the game has launched from save file
            ball_speed_x = data['ball_speed'][0] #Variable that stores the ball's speed in the x direction
            ball_speed_y = data['ball_speed'][1] #Variable that stores the ball's speed in the y direction
        current_score = data['score']   #Variable that stores the current score of the player
        ball_position = data['ball_position'] #Variable that stores the ball's position
        paddle_position = data['paddle_position'] #Variable that stores the paddle's position
        if data['username'] != "":    #If the username is not empty
            username = data['username'] #Variable that stores the username of the player



        grid = data['grid'] #Variable that stores the grid
        brick_width = 80    #Width of the bricks
        brick_height = 20   #Height of the bricks

        #Only deletes the bricks if the game has started
        game_canvas.delete("brick")

        #Loop that creates the bricks
        for row_index, row in enumerate(grid):  #Loop through each row (enumerate gives the index of the row)
            for column_index, brick in enumerate(row):  #Loop through each brick in the row (enumerate gives the index of the brick)
                #Only create the brick if it's valid(equal to 1)
                if brick['valid'] == 1:
                    #Gets the color of the brick from the dictionary in the JSON file
                    brick_color = brick['color']

                    #Creates the brick on the canvas
                    game_canvas.create_rectangle(column_index * brick_width, 
                                                row_index * brick_height, 
                                                (column_index + 1) * brick_width, 
                                                (row_index + 1) * brick_height, 
                                                fill=brick_color, tags = "brick")   #Each brick is given the tag "brick" so that they can be identified
    
    ###################################Load Save###################################
    #Function that loads the save file
    def start_savefile():
        global game_started, game_paused, pause_label

        game_started = True    #Set to false so that the game will not start automatically when the save is loaded
        game_paused = True  #Pause the game

        pause_label = Label(    #Tells the user how to continue the game
            maingame_window, 
            text="Press space to continue", 
            font=("Arial", 18))
        pause_label.place(relx=0.5, rely=0.5, anchor=CENTER)  #Displays the label on the window
        
        #Loads the save file
        make_bricks("save_file.json")   #Loads the bricks
    
    ###################################Identify Load Status###################################
    #Section to identify how to load the game

    if load_save == False:   #If the game has not launched from save file
        global ball_speed_x, ball_speed_y

        possible_speeds = [-8, -7, -6, -5, -4, 4, 5, 6, 7, 8] #List of possible speeds for the ball
        ball_speed_x = random.choice(possible_speeds)  #Speed of the ball in the x direction randomly chosen from the list
        #ball_speed_x = -9  #Sends ball into the first brick(For testing)
        ball_speed_y = -random.choice(possible_speeds)  #Speed of the ball in the y direction

        global default_speed_x, default_speed_y
        default_speed_x = ball_speed_x  #Variable that holds the default speed of the ball in the x direction
        default_speed_y = ball_speed_y  #Variable that holds the default speed of the ball in the y direction
        #Label to tell user how to start
        startgame_label = Label(
            maingame_window, 
            text="Press the space bar to begin", 
            font=("Arial", 18)) #Creating variable properties
        startgame_label.place(relx=0.5, rely=0.5, anchor=CENTER)  #Displays the label on the window

        make_bricks(level1) #Loads the first level when game window opened

    else:   #If the game has launched from save file
        start_savefile() #Loads the save file

    #Create a label to display the score
    score_label = Label(
        maingame_window, 
        text="Score: "+ str(current_score), 
        font=("Arial", 16))
    score_label.pack(side="bottom", anchor="sw")    #Puts the label bottom left of the screen    

    #Generating the paddle
    player_paddle = game_canvas.create_rectangle(paddle_position, fill="white")  #Creating the paddle on the window

    #Generating the ball
    game_ball = game_canvas.create_oval(ball_position, fill="white")  #Creating the ball on the window
    game_canvas.pack()

    #Creating return to main menu button
    exit_game_button = Button(
        maingame_window, 
        text="Exit and Save", 
        font=("Arial",10, "bold"), 
        width=20, height=1, 
        command= lambda: save_game())
    exit_game_button.place(relx=1.0, rely=1, anchor="se") #Places the button at the bottom right of the window
    
    ###################################Boss Key###################################
    maingame_window.bind("<Control-c>", lambda event: boss_key(maingame_window)) #Binds the "o" key to the function boss_key game continues to run in the background as you are not meant to play games during work hours     
    
    ###################################Load Next Level###################################
    #Function that loads the next level
    def next_level():
        global level1, level2, level3, current_level, game_started, game_paused, pause_label

        if current_level == level1: #If the current level is level 1
            current_level = level2  #Load level 2
        elif current_level == level2:   #If the current level is level 2
            current_level = level3  #Load level 3
        elif current_level == level3:   #If the current level is level 3
            current_level = level1  #Load level 1
        
        game_started = True    #Set to false so that the game will not start automatically when the next level is loaded
        game_paused = True  #Pause the game

        pause_label = Label(    #Tells the user how to continue the game
            maingame_window, 
            text="New Level\nPress space to continue", 
            font=("Arial", 18))
        pause_label.place(relx=0.5, rely=0.5, anchor=CENTER)  #Displays the label on the window

        maingame_window.bind("<space>", start_game)  #Rebind the space bar to the start_game function

        game_canvas.coords(player_paddle, 600, 800, 800, 775)   #Resets the paddle to its original position
        game_canvas.coords(game_ball, 700, 750, 720, 770)  # Resets the ball to its original position

        make_bricks(current_level) #Load the next level

    
    ###################################Save Game######################################
    #Function that saves the current game
    def save_game():
        global game_ended
        game_ended = True   #Stops the game

        #Function that creates the save file
        def create_save_file():                                     #Information from https://www.youtube.com/watch?v=__mZO-53PPM#
            global username, current_score, ball_speed_x, ball_speed_y, paddle_position
            num_rows = 25       #Number of rows in the grid
            num_columns = 18    #Number of columns in the grid
            brick_width = 80
            brick_height = 20
            grid = [[{'color': None, 'valid': 0} for _ in range(num_columns)] for _ in range(num_rows)]  #Defaults all possible bricks to be invalid so that 
                                                                                                         #Contents of the file is in the correct format

            bricks = list(game_canvas.find_withtag("brick"))  #Creates a list of all the bricks on the screen using their tag

            #Sort the bricks by their y-coordinate
            bricks.sort(key=lambda brick: game_canvas.coords(brick)[1])

            #Loop that gets the properties of each brick and adds it to the grid
            for brick in bricks:
                #Gets the position and colour of a brick
                position = game_canvas.coords(brick)
                colour = game_canvas.itemcget(brick, "fill")

                #Attempts to identify brick's row and column in the grid
                row_index = int(position[1] / brick_height)
                column_index = int(position[0] / brick_width)

                #Creates the dictionary that will contain the brick's properties
                brick_info = {
                    'color': colour,
                    'valid': 1
                }

                #Adds the brick's properties to the grid
                grid[row_index][column_index] = brick_info
            
            #Creates a dictionary that will be saved into the JSON file
            save_file = {
                "grid": grid,  # Grid containing the bricks and their properties
                "ball_position": game_canvas.coords(game_ball),  # Position of the ball
                "ball_speed": (ball_speed_x, ball_speed_y),  # Speed of the ball
                "score": current_score,  # Score of the player
                "username": username,   #Username of the player
                "paddle_position": paddle_position #Position of the paddle
            }

            #Creates the JSON file
            with open("levels/save_file.json", "w") as f:
                json.dump(save_file, f)

        create_save_file()  #Creates the save file

        quit_game() #Function that stops the game
            
    ###################################Runnning Game###################################
    #Function to start the game
    def start_game(event):
        maingame_window.unbind("<space>")  #Unbind the space bar

        global game_paused, game_started
        keybinds_mapping()  #Set the keybinds
        if game_started == False:  #If the game has not started yet
            startgame_label.destroy()   #Remove the label telling the user how to start
            game_started = True 
            game_paused = False
            ball_movement()  #Start the ball's movement
        else:  # If the game is paused
            game_paused = False
            if pause_label:  # If the pause label exists
                pause_label.destroy()  # Remove the pause label
            ball_movement()  # Resume the ball's movement
            maingame_window.unbind("<space>")  # Unbind the space bar

            
 
    #Function to toggle the pause state
    def toggle_ball(event=None):
        global game_paused 
        global pause_label
        game_paused = not game_paused #Inverts the value of paused
        
        if game_paused == True and game_started == True: #If the game is paused, open the settings screen
            pause_label = Label(
                maingame_window, 
                text="Press space to continue", 
                font=("Arial", 18))  # Create a new pause label
            pause_label.place(relx=0.5, rely=0.5, anchor=CENTER)  #Displays the label on the window 
            maingame_window.bind("<space>", start_game)  #Rebind the space bar to the start_game function
            setting_screen(maingame_window) #Open the settings screen
        elif game_paused == True and game_started == False: #If the game is paused but the game has not started yet
            maingame_window.bind("<space>", start_game)  #Rebind the space bar to the start_game function
            setting_screen(maingame_window) #Open the settings screen


    maingame_window.bind("<space>", start_game)   #Binds the space bar to the function start_game

    maingame_window.bind("<Escape>", lambda event: toggle_ball())  #Binds the escape key to the function toggle_ball
    
    maingame_window.bind("<FocusIn>", lambda event: keybinds_mapping()) #when the user clicks on the window, the keybinds will be updated
        
    def quit_game():
        global game_paused, game_started, current_score, current_level

        #Reset all variables
        current_score = 0
        game_started = False
        game_paused = False  
        current_level = level1 

    
        unbind_movement()   #Unbinds all keybinds
        maingame_window.unbind("<space>") #Unbinds the space bar
        maingame_window.unbind("<Escape>") #Unbinds the escape key

        for widget in maingame_window.winfo_children(): #Destroys all widgets on the screen
            widget.destroy() 

        return_to_previous_screen(maingame_window,window)

    ###################################Paddle Movement###################################
    def keybinds_mapping():
        unbind_movement()   #Unbinds the old keybinds
        maingame_window.bind("<b>", slow_speed) #Binds the b key to the function toggle_speed
        maingame_window.bind("<n>", bounce_bottom)   #Binds the space bar to the function start_game

        if control_scheme == 0: #If the user has chosen the default control scheme
            maingame_window.bind("<a>", move_left)
            maingame_window.bind("<d>", move_right)
        else:   #If the user has chosen the alternativ.e control scheme
            maingame_window.bind("<Left>", move_left)
            maingame_window.bind("<Right>", move_right)

    def unbind_movement():
        #Unbinds the old keybinds
        maingame_window.unbind("<a>")
        maingame_window.unbind("<d>")
        maingame_window.unbind("<Left>")
        maingame_window.unbind("<Right>")
        maingame_window.unbind("<b>")

    #Function that moves the paddle left
    def move_left(event):
        if game_paused: #Stops the paddle from moving when the game is paused
            return
        if game_canvas.coords(player_paddle)[0] > 0:  #Checks if the paddle is not at the left edge of the screen
            game_canvas.move(player_paddle, -25, 0)   #Moves the paddle left by 20 pixels
    
    #Function that moves the paddle right
    def move_right(event):
        if game_paused: #Stops the paddle from moving when the game is paused
            return
        if game_canvas.coords(player_paddle)[2] < 1440: #Checks if the paddle is not at the right edge of the screen
            game_canvas.move(player_paddle, 25, 0)    #Moves the paddle right by 20 pixels

    
    ###################################Ball Movement###################################
    def ball_movement():
        global game_ended, paddle_position
        if game_ended == False:  #If the game hasnt ended
            if game_paused == False and remaining_bricks() == True: #If the game is not paused and there are still bricks on the screen
                game_canvas.move(game_ball, ball_speed_x, ball_speed_y)    #Moves the ball by the speed in the x and y direction
                paddle_position = game_canvas.coords(player_paddle)    #Constantly updates the paddle's position
                collision_detection()   #Checks for collision of the ball with all objects
                window.after(10, ball_movement)  #Moves the ball every 10 milliseconds


    ###################################Score Tracking###################################
    #Function that updates the score label
    def score_tracking(): 
        global current_score
        score_label.config(text="Score: " + str(current_score))
    
    ###################################Game Over###################################
    #Function that stops the gmae and displays "Game Over" text
    def game_over():
        global game_paused
        game_paused = True  #Stops the game
        # Create a black rectangle
        game_canvas.create_rectangle(400, 245, 1000, 600, fill="black")  # Creates a bigger black rectangle for the lose game message        
        game_canvas.create_text(
            700, 442, 
            text=("Game Over \n" + username + " Scored " + str(current_score)), 
            font=("Arial", 50), fill="white")  #Display a game over message
        unbind_movement()   #Unbinds all keybinds
        maingame_window.unbind("<space>") #Unbinds the space bar
        maingame_window.unbind("<Escape>") #Unbinds the escape key

        exit_game_button.destroy()  #Removes the return to main menu button

        # Adds the user's score to the leaderboard
        leaderboard_list = read_file("leaderboard.csv").split("\n")  # Reads the leaderboard file and stores it in a list
        leaderboard_list = [line.split(",")[1:] for line in leaderboard_list if line]   # Split each line into a username and score, and convert the score to an integer

        for i in range(len(leaderboard_list)):  # Loop to convert the score to an integer
            leaderboard_list[i][1] = int(leaderboard_list[i][1])    

        # Add the current user's score to the leaderboard
        leaderboard_list.append([username, current_score])

        # Sorts the scores in descending order
        leaderboard_list.sort(key=lambda x: x[1], reverse=True)

        # Only keeps the top 10 scores
        leaderboard_list = leaderboard_list[:10]

        # Add the position on the leaderboard to each line
        for i in range(len(leaderboard_list)):
            leaderboard_list[i] = [i+1] + leaderboard_list[i]

        # Convert the list back into a string to write it back to the file
        leaderboard_string = "\n".join([",".join(map(str, line)) for line in leaderboard_list])
        write_file("leaderboard.csv", leaderboard_string)


        #Creates a button to return to the main menu
        return_button = Button(
            maingame_window, 
            text="Return to Main Menu", 
            font=("Arial",15, "bold"), 
            width=30, height=2, 
            command= lambda: quit_game())
        return_button.place(relx=0.5, rely=0.87, anchor=CENTER) #Centers the button

    ###################################Completing Game###################################
    #Function to check if all bricks have been destroyed
    def remaining_bricks():
        all_items = game_canvas.find_all()    #Adding all objects on screen into a tuple
        for item in all_items:  #Loop through every object
            if item != game_ball and item != player_paddle:  #Selection statement to identify that the object is a brick
                if game_canvas.type(item) == 'rectangle':  #If the item is a rectangle (brick)
                    return True  #There are still bricks on the canvas
        return False  #No remaining bricks on the canvas
    
    ###################################Cheats###################################
    #Function that slows down the ball
    def slow_speed(event):
        global ball_speed_x, ball_speed_y, default_speed_x, default_speed_y

        max_speed_x = default_speed_x / 32  #Variable that holds the maximum speed of the ball in the x direction
        max_speed_y = default_speed_y / 32  #Variable that holds the maximum speed of the ball in the y direction

        #Halves the current speed of the ball
        ball_speed_x = ball_speed_x / 2 
        ball_speed_y = ball_speed_y / 2
        
        #When the ball moves at a speed equal to the maximum speed, it will reset back to the default speed
        if ball_speed_x == max_speed_x:
            ball_speed_x = default_speed_x
        elif ball_speed_x == -max_speed_x:
            ball_speed_x = -default_speed_x

        #When the ball moves at a speed equal to the maximum speed, it will reset back to the default speed
        if ball_speed_y == max_speed_y:
            ball_speed_y = default_speed_y
        elif ball_speed_y == -max_speed_y:
            ball_speed_y = -default_speed_y
    
    #Function that bounces the ball off the bottom of the screen
    def bounce_bottom(event):
        print("Bounce Bottom")
        global enable_bounce
        enable_bounce = not enable_bounce #Inverts the value of enable_bounce

    ###################################Collision Detection###################################
    def collision_detection():
        #Variables will hold speed of the ball
        global ball_speed_x
        global ball_speed_y
        global current_score
        global enable_bounce

        if game_paused == False: #If the game is not paused

            
            ball_location = game_canvas.coords(game_ball)   #Gets the location of the ball
            paddle_location = game_canvas.coords(player_paddle) #Gets the location of the paddle

            #Check for collision against the walls
            if ball_location[0] <= 0 or ball_location[2] >= 1440:
                #Reverse the direction of the ball when it hits the left or right walls
                ball_speed_x = -ball_speed_x
            if ball_location[1] <= 0:
                #Reverse the direction of the ball when it hits the top wall
                ball_speed_y = -ball_speed_y


            #Check for collision between the paddle and ball
            if (paddle_location[0] < ball_location[2] and 
                paddle_location[2] > ball_location[0] and   #Checks if the ball is touching the paddle using the coordinates of both objects
                paddle_location[1] < ball_location[3] and 
                paddle_location[3] > ball_location[1]):   
                
                #Bounces the ball when a collision is detected with the paddle
                if ball_speed_y > 0 and ball_location[3] >= paddle_location[1]:  #Check when the ball bounces off the top of the paddle
                    ball_speed_y = -ball_speed_y
                else:   #Else it has bounced of the side of the paddle (Prevents ball from slipping inside the paddle)
                    ball_speed_y = -ball_speed_y
                    ball_speed_x = -ball_speed_x

            #Check for collision between the bricks and the balls
            overlap_items = game_canvas.find_overlapping(*ball_location)  #Variable holds all items that overlap the ball's coordinates
            for item in overlap_items:  #Loop to go through all items in list
                if item != game_ball and item != player_paddle:  #Selection statement to identify that the object is a brick
                    if game_canvas.type(item) == 'rectangle':  #Check to see if the item is a rectangle (brick)
                        brick_location = game_canvas.coords(item)   #Stores location of the brick in a variable

                        #Reverses the direction of the ball when it hits a brick
                        if (ball_location[0] < brick_location[2] 
                            and ball_location[2] > brick_location[0]    #Checks that any of the ball's edges has collided with the brick
                            and ball_location[1] < brick_location[3] 
                            and ball_location[3] > brick_location[1]): 

                            #Checks which side of the brick the ball has collided with
                            if ball_location[0] < brick_location[0] and ball_speed_x > 0:   #If it hits the left side of the brick
                                #Bounce sideways
                                ball_speed_x = -ball_speed_x
                            elif ball_location[2] > brick_location[2] and ball_speed_x < 0: #If it hits the right side of the brick
                                #Bounce sideways
                                ball_speed_x = -ball_speed_x
                            else:
                                #Bounce vertically if the ball hits the top or bottom of the brick
                                ball_speed_y = -ball_speed_y

                            #Remove the brick from the canvas
                            brick_color = game_canvas.itemcget(item, "fill")  #Identifies colour of the brick that has collided with the ball
                            if brick_color == "green":  #When brick is green changes to orange
                                game_canvas.itemconfig(item, fill="orange")
                            elif brick_color == "orange":  #When brick is orange changes to red
                                game_canvas.itemconfig(item, fill="red")
                            elif brick_color == "red":  #When brick is red brick is deleted
                                game_canvas.delete(item)  #Removes brick from screen
                            
                            current_score += 1 #Increases score by 1
                            score_tracking()  #Updates the score label

                            #Check if all bricks have been destroyed
                            if remaining_bricks() == False:
                                next_level() #function that stops the game

            #Check for collision with the bottom of the screen
            if enable_bounce == False and ball_location[3] >= 900: #If the ball has hit the bottom of the screen and cheat off
                game_over() #function that stops the game
            elif enable_bounce == True and ball_location[3] >= 900: #If the ball has hit the bottom of the screen and cheat on
                ball_speed_y = -ball_speed_y

    maingame_window.focus_force()    #Makes the window the main focus
    maingame_window.protocol("WM_DELETE_WINDOW", sys.exit) #Closes the program when the window is closed
    maingame_window.mainloop()   #Loads the main game window
                            
##############################################################################################################Leaderboard Screen##############################################################################################################
def leaderboard_screen():
    window.withdraw()   #Hides the main window

    #Create a new window for the leaderboard
    leaderboard_window = Toplevel(window)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("1440x900+250+50") 
    leaderboard_window.resizable(False,False)   #Window size cant be changed

    #Loading the Background using an Image
    bg_image = PhotoImage(file = "assets/brick_background.png")    #Image File Path
    leaderboard_window.bg_image = bg_image  #Stops the image from being removed from memory

    #Generating the background image
    leaderboard_canvas = Canvas(leaderboard_window, width=1440, height=900)  #Creating base for the paddle
    leaderboard_canvas.create_image(0, 0, image=bg_image, anchor='nw')  #Set the background image on the canvas
    leaderboard_canvas.pack()

    #Creating return to main menu button
    exit_leaderboard_button = Button(
        leaderboard_window, 
        text="Return to Main Menu", 
        font=("Arial",10, "bold"), 
        width=25, height=3, 
        command= lambda: return_to_previous_screen(leaderboard_window,window))
    exit_leaderboard_button.place(relx=1.0, rely=1, anchor="se") #Places the button at the bottom right of the window

    #Creating a label to display the leaderboard
    leaderboard_title_label = Label(
        leaderboard_window, 
        text="Leaderboard", 
        font=("Arial", 50))
    leaderboard_title_label.place(relx=0.5, rely=0.1, anchor=CENTER)  #Centers the label

    #Creating a rectangle for the leaderboard to displayed ontop of
    leaderboard_canvas.create_rectangle(200, 200, 1240, 800, fill="black")

    #Creating a label to display the leaderboard list onto the rectangle
    leaderboard_list = read_file("leaderboard.csv").split("\n")  #Reads the leaderboard file and stores it in a list
    leaderboard_list = [line.split(",") for line in leaderboard_list if line]   #Split each line into a position, username and score

    for i in range(len(leaderboard_list)):  #Loop to go through every score in leaderboard_list and convert the score to an integer
        leaderboard_list[i][2] = int(leaderboard_list[i][2])

    #Sorts the scores in descending order
    leaderboard_list.sort(key=lambda x: x[2], reverse=True)

    #Convert the list back into a string to display it in the label
    leaderboard_string = "Position\t\t\tUsername\t\t\tScore\n"  #Header line (\t is a tab)
    leaderboard_string += "\n".join([f"{line[0]}\t\t\t{line[1]}\t\t\t{line[2]}" for line in leaderboard_list])      #Adds each line in leaderbaord_list into the string

    display_leaderboard_text = Text(
        leaderboard_window, 
        width=90, height=25,    #Creates a text widget to display the leaderboard
        font=("Arial", 15), 
        fg="white", bg="black")    
    display_leaderboard_text.insert(INSERT, leaderboard_string) #Inserts the leaderboard string into the Text widget
    display_leaderboard_text.place(x=720, y=500, anchor=CENTER)  #Centers the Text widget
    display_leaderboard_text.config(state=DISABLED)  #Makes the leaderboard read-only so users can't edit it

    #Bind the boss_key function to the 'o' key for leaderboard screen
    leaderboard_window.bind("<Control-c>", lambda event: boss_key(leaderboard_window)) #Binds the "o" key to the function boss_key

    leaderboard_window.focus_force()    #Makes the window the main focus
    leaderboard_window.protocol("WM_DELETE_WINDOW", sys.exit) #Closes the program when the window is closed
    leaderboard_window.mainloop()   #Loads the leaderboard window
    

##############################################################################################################Running Code##############################################################################################################
main_menu() #Loads the Main Menu Screen











##############################################################################################################References#############################################################################################################
#https://docs.python.org/3/library/tkinter.html#
#https://docs.python.org/3/library/json.html#
#https://docs.python.org/3/library/stdtypes.html#list.sort#
#https://www.youtube.com/watch?v=__mZO-53PPM#