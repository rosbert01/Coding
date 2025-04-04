from turtle import *
import colorsys as cs
bgcolor('black')
tracer(100)
pensize(3)
h = 0

def draw(ang, n):
    circle(5+n, 90)
    left(ang)
    circle(5+n, 0)
goto(-10,0)  
for i in range(700):
    c = cs.hsv_to_rgb(h,1,1) 
    pencolor(c)
    h +=0.005
    penup()
    draw(90, i)
    draw(180, i/2)
    pendown()
    fillcolor('black')
    begin_fill()
    draw(1/2, i-i)
    draw(180, i/2)
    draw(90, i)
    end_fill()
    draw(60, i/2)
done() 