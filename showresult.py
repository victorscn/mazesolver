from maze import Maze
import turtle
import sys
import ast

if __name__ == '__main__':
    '''
    This function uses Python's turtle library to draw a picture of the maze
    given as an argument when running the script.
    '''

    # Create a maze based on input argument on command line.
    testmaze = Maze( str(sys.argv[1]) )
    # Open tester result
    f = open('tester.txt','rb')

    # Intialize the window and drawing turtle.
    window = turtle.Screen()
    wally = turtle.Turtle()
    wally.speed(0)
    wally.hideturtle()
    wally.penup()

    #Initializing maze solver turtle
    mouse = turtle.Turtle()
    mouse.speed(0)
    mouse.penup()
    mouse.color('red') 

    # maze centered on (0,0), squares are 20 units in length.
    sq_size = 20
    origin = testmaze.dim * sq_size / -2

    # iterate through squares one by one to decide where to draw walls
    for x in range(testmaze.dim):
        for y in range(testmaze.dim):
            if not testmaze.is_permissible([x,y], 'up'):
                wally.goto(origin + sq_size * x, origin + sq_size * (y+1))
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            if not testmaze.is_permissible([x,y], 'right'):
                wally.goto(origin + sq_size * (x+1), origin + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # only check bottom wall if on lowest row
            if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                wally.goto(origin + sq_size * x, origin)
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # only check left wall if on leftmost column
            if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                wally.goto(origin, origin + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

       

    moves = f.read()
    runs = moves.split('\n')

    for r in range(len(runs)):
        mouse.goto(origin + 10, origin + 10)
        mouse.pendown()
        runs[r] = runs[r].split('.')        
        runs[r].pop()
        if r!=0:
            mouse.color('green')
        runs[r] = [ast.literal_eval(d) for d in runs[r]]
        for k in range(len(runs[r])):
            mouse.goto(origin+ 10 + sq_size * runs[r][k][0], origin+10+sq_size * runs[r][k][1] )
        mouse.penup()

    window.exitonclick()