from tkinter import *
import GetSize


canvaswidth, canvasheight, canvasoffset = 800, 600, 15
wt, lt, ht, draft, face = float(52), float(60.5), float(24), "Updraft", "Top"
tpoints = GetSize.create_points(wt, lt, draft, "Top")
scale, lengthdif = GetSize.find_scale(canvaswidth, canvasheight, tpoints, ht, canvasoffset)
topshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, scale, tpoints, "top", canvasoffset, lengthdif)
print(topshape)


c = Canvas(width=canvaswidth, height=canvasheight)
c.pack()

# a square
# xy = [(50, 50), (150, 50), (150, 150), (50, 150)]
# xy = ([15.0, 465.0], [15.0, 446.3333333333333], [99.0, 353.0], [173.66666666666669, 353.0], [257.6666666666667, 446.3333333333333], [257.6666666666667, 465.0])
# print(xy)
xy = topshape[0:4]
polygon_item = c.create_polygon(xy, fill="#ccc", outline="black", width=2)
xy1 = topshape[4:8]
polygon_item2 = c.create_polygon(xy1, fill="#ccc", outline="black", width=2)


# center = xy[0][0] + ((xy[5][0] - xy[0][0])/2), xy[2][1] + ((xy[0][1] - xy[2][1])/2)
center = xy[0][0] + ((xy[3][0] - xy[0][0])/2), xy[1][1] + ((xy[0][1] - xy[1][1])/2)

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

    newxy1 = []
    for x, y in xy1:
        v = angle * (complex(x, y) - offset) + offset
        newxy1.append(v.real)
        newxy1.append(v.imag)
    c.coords(polygon_item2, *newxy1)



c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)


mainloop()