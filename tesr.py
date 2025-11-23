from graphics import *

win = GraphWin("My Window", 500, 500)
circle = Circle(Point(250, 250), 100)
circle.setFill("blue")
circle.draw(win)

while True:
    while True:
        move = circle.getCenter().getX() + 10
        if move != 0:
            circle.move(10, 0)
            False
            break

    while True:
        move = circle.getCenter().getX() - 10
        if move != 500:
            circle.move(-10, 0)
            False
            break

    