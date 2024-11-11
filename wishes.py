import turtle
import random

def draw_text(text):
    # Set up the turtle
    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.color("blue")
    turtle.write(text, align="center", font=("Arial", 36, "bold"))

def draw_background():
    # Draw a colorful background
    turtle.bgcolor("lightyellow")
    for _ in range(36):
        # Set a random color
        turtle.color(random.random(), random.random(), random.random())
        turtle.begin_fill()
        turtle.circle(100)
        turtle.right(10)
        turtle.end_fill()

def main():
    turtle.speed(0)  # Fastest drawing speed
    draw_background()
    draw_text("Happiest Wishes!")
    
    turtle.hideturtle()  # Hide the turtle after drawing
    turtle.done()  # Finish the drawing

# Run the main function
main()
