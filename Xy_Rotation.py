from tkinter import *
import GetSize


canvaswidth, canvasheight, canvasoffset = 800, 600, 15
wt, lt, ht, draft, face = float(52), float(60.5), float(24), "Updraft", "Top"
tpoints = GetSize.create_points(wt, lt, draft, "Top")
scale, lengthdif = GetSize.find_scale(canvaswidth, canvasheight, tpoints, ht, canvasoffset)
topshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, scale, tpoints, "top", canvasoffset, lengthdif)


c = Canvas(width=canvaswidth, height=canvasheight)
c.pack()

xy = topshape
polygon_item0 = c.create_polygon(xy[0:4], fill="#ccc", outline="black", width=2)
# xy1 = topshape[4:8]
polygon_item1 = c.create_polygon(xy[4:8], fill="#ccc", outline="black", width=2)
print(xy)
line_item0 = c.create_line(xy[0], xy[4], width=2)
line_item1 = c.create_line(xy[1], xy[5], width=2)
line_item2 = c.create_line(xy[2], xy[6], width=2)
line_item3 = c.create_line(xy[3], xy[7], width=2)

center = xy[0][0] + ((xy[3][0] - xy[0][0])/2), xy[1][1] + ((xy[0][1] - xy[1][1])/2)


def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    print("event x", event.x)
    print("event y", event.y)
    print("ccan event x", c.canvasx(event.x))
    print("ccan event y", c.canvasy(event.y))
    # print("center = ", center)
    # print("dx = ", dx)
    # print("dy = ", dy)
    # print("complex dx/dy = ", complex(dx, dy))
    # print("abs complex = ", abs(complex(dx, dy)))
    # print("devide them = ", complex(dx, dy) / abs(complex(dx, dy)))
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0  # cannot determine angle


def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)


def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    print("getangle = ", getangle(event))
    print("angle = ", angle)
    # offset = complex(center[0], center[1])
    # newxy = []
    # for x, y in xy:
    #     print(complex(x, y))
    #     v = angle * (complex(x, y) - offset) + offset
    #     print(v)
    #     newxy.append(v.real)
    #     newxy.append(v.imag)
    # c.coords(polygon_item0, *newxy[0:8])
    # c.coords(polygon_item1, *newxy[8:16])
    # c.coords(line_item0, *newxy[0:2], *newxy[8:10])
    # c.coords(line_item1, *newxy[2:4], *newxy[10:12])
    # c.coords(line_item2, *newxy[4:6], *newxy[12:14])
    # c.coords(line_item3, *newxy[6:8], *newxy[14:16])


c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)


mainloop()
