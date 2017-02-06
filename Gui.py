import random
from tkinter import *
from tkinter.ttk import Combobox

import GetSize
import Mesurements
import Iso_View
wt, lt, ht = 0, 0, 0
freeview = False
runonce = True


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="#aaa")

        self.parent = parent
        self.parent.title("Jono's Kiln Hood Creator")
        self.pack(fill=BOTH, expand=1)
        self.centerwindow()

    def centerwindow(self):

    # Setting up Window
        w = 800
        h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        xaxis = (sw - w) / 2
        yaxis = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, xaxis, yaxis))
        # self.parent.overrideredirect(1)  # Remove border
        # self.parent.attributes('-topmost', 1) # dunno
        # self.parent.attributes("-fullscreen", True) #fullscreen

    # Setting Grid
        self.columnconfigure(1, weight=1)  # column 1 and 2 stretch for canvas
        self.columnconfigure(2, weight=1)
        # for x in range(0, 12): # pad all rows
        #     self.rowconfigure(x, pad=1)
        self.rowconfigure(10, weight=1)  # Last row of canvas stretches
        self.rowconfigure(0, pad=8)
        self.rowconfigure(11, pad=8)
        self.rowconfigure(12, pad=8)

    # canvas
        canvas = Canvas(self, background="#fff")
        canvas.grid(row=1, column=1, columnspan=2, rowspan=10, padx=4, sticky=N+W+E+S)

        def mouseloc(event):
            # Mouse Location
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            return x, y

        def press(event):
            # starting x,y
            global start
            start = mouseloc(event)


        def motion(event):
            # calculate current xy relative to initial xy
            global start
            xy = mouseloc(event)
            movement = (start[0] - xy[0]) / (15.0000), (start[1] - xy[1]) / (15.0000)
            start = xy
            if freeview is True:
                draw_iso_canvas(movement)
            else:
                return

        canvas.bind("<Button-1>", press)
        canvas.bind("<B1-Motion>", motion)



    # input testing amounts
        def setdef():
            ltext.delete("1.0", END)
            ltext.insert("1.0", "60.5")
            wtext.delete("1.0", END)
            wtext.insert("1.0", "52")
            htext.delete("1.0", END)
            htext.insert("1.0", "24")
            stylecbox.set("Downdraft")

    # Make random size hoods
        def randsettings():
            ltext.delete("1.0", END)
            ltext.insert("1.0", random.randint(50, 100))
            wtext.delete("1.0", END)
            wtext.insert("1.0", random.randint(50, 100))
            htext.delete("1.0", END)
            htext.insert("1.0", random.randint(20, 60))
            randdraft = "Downdraft", "Updraft"
            stylecbox.set(randdraft[random.randint(0, 1)])
            if freeview == False:
                create_home()
            else:
                create_free()


    # Create floats from inputs
        def get_user_inputs():
            isfloat = bool(1)
            global wt, lt, ht
            global top
            global skirt
            top = 16
            skirt = 4
            try:
                lt = float(ltext.get("1.0", 'end-1c'))
            except ValueError:
                print("Length must be a number! ")
                isfloat = False
            try:
                wt = float(wtext.get("1.0", 'end-1c'))
            except ValueError:
                print("Width must be a number!")
                isfloat = False
            try:
                ht = float(htext.get("1.0", 'end-1c'))
            except ValueError:
                print("Height must be a number!")
                isfloat = False
            return wt, lt, ht, isfloat

    # Get points
        def get_points(wt, lt, ht, draft):
            fpoints = GetSize.create_points(wt, ht, draft, "Front")
            spoints = GetSize.create_points(lt, ht, draft, "Side")
            tpoints = GetSize.create_points(wt, lt, draft, "Top")
            hpoints = GetSize.create_points(wt, lt, draft, "Hole")
            return fpoints, spoints, tpoints, hpoints


    # Display objects on canvas
        def create_home():
            global freeview
            freeview = False
            Iso_View.reset_movement()
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            canvas.delete("all")
            draw_home_canvas(canvaswidth, canvasheight)

        def create_free():
            global freeview
            freeview= True
            defmovement = 0, 0
            Iso_View.reset_movement()
            draw_iso_canvas(defmovement)

        def draw_home_canvas(canvaswidth, canvasheight):
            global draft
            draft = stylecbox.get()
            wt, lt, ht, isfloat = get_user_inputs()
            if not isfloat:
                return
            fpoints, spoints, tpoints, hpoints = get_points(wt, lt, ht, draft)

            # Scale points to canvas
            offset = 15
            scale, lengthdif = GetSize.find_scale(canvaswidth, canvasheight, tpoints, ht, offset)

            frontshape = GetSize.locate_points_canvas(
                canvaswidth, canvasheight, scale, fpoints, "front", offset, lengthdif)
            sideshape = GetSize.locate_points_canvas(
                canvaswidth, canvasheight, scale, spoints, "side", offset, lengthdif)
            topshape = GetSize.locate_points_canvas(
                canvaswidth, canvasheight, scale, tpoints, "top", offset, lengthdif)
            holeshape = GetSize.locate_points_canvas(
                canvaswidth, canvasheight, scale, hpoints, "hole", offset, lengthdif)

            # Print front/side/top views to canvas
            canvas.create_polygon(frontshape, fill="#ccc", outline="black", width=2)
            canvas.create_polygon(sideshape, fill="#ccc", outline="black", width=2)
            canvas.create_polygon(topshape[0:4], fill="#ccc", outline="black", width=2)
            canvas.create_polygon(topshape[4:8], fill="#ccc", outline="black", width=2)
            canvas.create_line(topshape[0], topshape[4], width=2)
            canvas.create_line(topshape[1], topshape[5], width=2)
            canvas.create_line(topshape[2], topshape[6], width=2)
            canvas.create_line(topshape[3], topshape[7], width=2)
            canvas.create_oval(holeshape, width=2, fill="#fff")

            # Iso View
            isoscale = scale * .85  # temporary fix for oversized iso view
            isopoints = Iso_View.iso_points()
            movement = 0, 0
            for n in range(len(isopoints)):
                r, zdepth = Iso_View.rotate_face(isopoints[n], movement)
                shape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, r, "iso", offset, lengthdif)
                canvas.create_polygon(shape, fill="#ccc", outline="black", width=2)

            # get measurement locations
            frontcords = Mesurements.get_measurement_cords(frontshape)
            sidecords = Mesurements.get_measurement_cords(sideshape)
            # Get size arrays
            frontsizearray = Mesurements.size_array(wt, ht)
            sidesizearray = Mesurements.size_array(lt, ht)

            # print measurements to canvas
            for n in range(0, 4):
                canvas_id = canvas.create_text(frontcords[n])
                canvas.itemconfig(canvas_id, text=frontsizearray[n])
            for n in range(0, 4):
                canvas_id = canvas.create_text(sidecords[n])
                canvas.itemconfig(canvas_id, text=sidesizearray[n])
            return

        def draw_iso_canvas(movement):
            canvas.delete("all")
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            global draft
            draft = stylecbox.get()
            wt, lt, ht, isfloat = get_user_inputs()
            if not isfloat:
                return
            offset = 15
            isopoints = Iso_View.iso_points()



            scale, lengthdif = GetSize.find_iso_scale(canvaswidth, canvasheight, isopoints, ht, offset)
            isoscale = scale * .85  # temporary fix for oversized iso view
            isrotated = []
            isodepth = []
            for n in range(len(isopoints)):
                r, zdepth = Iso_View.rotate_face(isopoints[n], movement)
                shape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, r, "free", offset, lengthdif)
                isrotated.append(shape)
                isodepth.append(zdepth)


            todraw = Iso_View.draw_order(isrotated, isodepth)
            for n in range(len(todraw)):
                canvas.create_polygon(todraw[n], fill="#ccc", outline="black", width=2)
            global runonce
            if runonce:
                print("run once")
                runonce = False
                canvas_id = canvas.create_text(canvaswidth / 2, canvasheight / 8)
                canvas.itemconfig(canvas_id, font=("Courier", 20), text="Click and drag to rotate!")

    # Frame objects
        lbl = Label(self, text="Kiln Hoods Calculator", width=20)
        lbl.grid(row=0, column=1, columnspan=2)
        cbtn = Button(self, text="Create", width=10, command=create_home)
        cbtn.grid(row=10, column=0, sticky=N)

        fbtn = Button(self, text="Free View", width=10, command=create_free)
        fbtn.grid(row=11, column=0, sticky=N)


        dbtn = Button(self, text="Defaults", width=10, command=setdef)
        dbtn.grid(row=11, column=3, sticky=E)
        hbtn = Button(self, text="Random", width=10, command=randsettings)
        hbtn.grid(row=12, column=0)
        quit_button = Button(self, text="Quit", width=10, command=self.quit)
        quit_button.grid(row=12, column=3)

        llbl = Label(self, text="Length:", width=10, background="#aaa")
        llbl.grid(row=1, column=0, sticky=W+S)
        ltext = Text(self, width=10, height=1)
        ltext.insert(END, "Length")
        ltext.grid(row=2, column=0)
        wbl = Label(self, text="Width:", width=10, background="#aaa")
        wbl.grid(row=3, column=0, sticky=W+S)
        wtext = Text(self, width=10, height=1)
        wtext.insert(END, "Width")
        wtext.grid(row=4, column=0)
        hlbl = Label(self, text="Height:", width=10, background="#aaa")
        hlbl.grid(row=5, column=0, sticky=W+S)
        htext = Text(self, width=10, height=1)
        htext.insert(END, "Height")
        htext.grid(row=6, column=0)
        stylelbl = Label(self, text="Draft Type:", width=10, background="#aaa")
        stylelbl.grid(row=7, column=0, sticky=W + S)
        stylecboxvar = 0
        stylecbox = Combobox(self, width=10, textvariable=stylecboxvar, state="readonly")
        stylecbox['values'] = ('Updraft', 'Downdraft')
        stylecbox.grid(row=8, column=0)

        fakelbl = Label(self, text="    ", width=10, background="#aaa")
        fakelbl.grid(row=9, column=0, sticky=W + S)

def size_list():
    global wt, lt, ht, top, skirt, draft
    sizelist = wt, lt, ht, top, skirt, draft
    return sizelist

def main():
    root = Tk()
    Example(root)
    root.mainloop()
