import turtle as tr

layar = tr.Screen()

tr.setup(700, 700)
layar.bgcolor('#000000')
tr.pencolor('#540d6e')
tr.speed(15500)
tr.tracer(1000)
tr.pensize(1)

warna_bunga = ('red', 'green', 'white', 'yellow')

for i in range(3):
    for n in range(400):
        tr.color(warna_bunga[n % 4])
        tr.circle(190 - n / 2, 90)
        tr.left(90)
        tr.circle(190 - n / 2, 90)
        tr.color(warna_bunga[n % 4])
        
    tr.left(30)

layar.exitonclick()