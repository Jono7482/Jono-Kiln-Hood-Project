from tkinter import *
import math

c = Canvas(width=800, height=600)
c.pack()

# a square
# xy = [(50, 50), (150, 50), (150, 150), (50, 150)]
xy = ([15.0, 465.0], [15.0, 446.3333333333333], [99.0, 353.0], [173.66666666666669, 353.0], [257.6666666666667, 446.3333333333333], [257.6666666666667, 465.0])
print(xy)

polygon_item = c.create_polygon(xy, fill="#ccc", outline="black", width=2)

center = xy[0][0] + ((xy[5][0] - xy[0][0])/2), xy[2][1] + ((xy[0][1] - xy[2][1])/2)


print(center)

def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0 # cannot determine angle

def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)

def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    offset = complex(center[0], center[1])
    newxy = []
    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    c.coords(polygon_item, *newxy)

c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)

mainloop()