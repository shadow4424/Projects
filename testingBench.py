from tkinter import *
import json
#Create a new window for the main game
maingame_window = Tk()
maingame_window.title("Ball Breaker")
maingame_window.geometry("1440x900") 


#Loading the Background using an Image
bg_image = PhotoImage(file = "assets/maingame_screen.png")    #Image File Path
maingame_window.bg_image = bg_image  #Stops the image from being removed from memory

#Generating the background image
game_canvas = Canvas(maingame_window, width=1440, height=900)  #Creating base for the paddle
game_canvas.create_image(0, 0, image=bg_image, anchor='nw')  #Set the background image on the canvas

#Create a label to display the score
score_label = Label(maingame_window, text="Score: ", font=("Arial", 16))
score_label.pack(side="bottom", anchor="sw")    #Puts the label bottom left of the screen    

#Label to tell user how to start
startgame_label = Label(maingame_window, text="Press the space bar to begin", font=("Arial", 18)) #Creating variable properties
startgame_label.place(relx=0.5, rely=0.5, anchor=CENTER)  #Displays the label on the window 

#Generating the paddle
player_paddle = game_canvas.create_rectangle(600, 800, 800, 775, fill="white")  #Creating the paddle on the window

#Generating the ball
game_ball = game_canvas.create_oval(700, 750, 720, 770, fill="white")  #Creating the ball on the window
game_canvas.pack()

def make_bricks(level_name):
        #Loads the brick configurations from the JSON file
        with open("levels/"+level_name, 'r') as f:
            data = json.load(f) #Variable that stores the data

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

level_name = "checkered_level.json"
make_bricks(level_name)


maingame_window.mainloop()  #Keeps the window open until the user closes it