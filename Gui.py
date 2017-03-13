import random
from tkinter import *
from tkinter.ttk import Combobox

import GetSize
import Mesurements
import Iso_View
wt, lt, ht, top, skirt = 0, 0, 0, 0, 0
draft = int
cview = "Default"
flatface = "Left"
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
        self.columnconfigure(3, weight=1)  # column 3 and 4 stretch for canvas
        self.columnconfigure(4, weight=1)
        self.columnconfigure(1, minsize=50)
        self.columnconfigure(2, minsize=50)
        # for x in range(0, 12): # pad all rows
        #     self.rowconfigure(x, pad=1)
        self.rowconfigure(11, weight=1)  # row 11 of canvas stretches
        self.rowconfigure(0, pad=8)


        # canvas
        canvas = Canvas(self, background="#fff")
        canvas.grid(row=1, column=1, columnspan=4, rowspan=17, padx=4, sticky=N+W+E+S)

    # free view mouse control
        start = []
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
            movement = (start[0] - xy[0]) / 15.0000, (start[1] - xy[1]) / 15.0000
            start = xy
            if cview is "Free":
                draw_iso_canvas(movement)
            else:
                return

        canvas.bind("<Button-1>", press)
        canvas.bind("<B1-Motion>", motion)

    # change global values for model custom update
        def setglobaldims(lv, wv, hv):
            global lt, wt, ht
            lt, wt, ht = lv, wv, hv

    # input testing amounts
        def setdef():
            ltext.delete("1.0", END)
            ltext.insert("1.0", "60.5")
            wtext.delete("1.0", END)
            wtext.insert("1.0", "52")
            htext.delete("1.0", END)
            htext.insert("1.0", "24")
            stylecbox.set("Downdraft")
            create()

    # Make random size hoods
        def randsettings():
            l = random.randint(50, 100)
            w = random.randint(50, 100)
            h = random.randint(20, 60)
            ltext.delete("1.0", END)
            ltext.insert("1.0", l)
            wtext.delete("1.0", END)
            wtext.insert("1.0", w)
            htext.delete("1.0", END)
            htext.insert("1.0", h)
            randdraft = "Downdraft", "Updraft"
            stylecbox.set(randdraft[random.randint(0, 1)])
            create()

    # store standard model dimensions for updraft and downdraft
        def modelsaves(index):
            ud4 = 45, 44, 24
            dd4 = 45, 52.5, 24
            ud9 = 52, 51, 24
            dd9 = 52, 60.5, 24
            ud12 = 54, 52, 24
            dd12 = 54, 61.5, 24
            ud18 = 57.5, 56, 24
            dd18 = 57.5, 66.5, 24
            ud24 = 62.5, 61.5, 24
            dd24 = 62.5, 72, 24
            ud40 = 67.5, 65, 24
            dd40 = 67.5, 75.5, 24
            saves = ud4, dd4, ud9, dd9, ud12, dd12, ud18, dd18, ud24, dd24, ud40, dd40
            return saves[index]

    # set model dimensions
        def setmodel():
            model = modelcbox.get()
            draft = stylecbox.get()

            if model == 'Custom' or model == '':
                return

            if draft == "Updraft" or draft == "":
                stylecbox.set("Updraft")
                if model == 'LE-200-4':
                    dims = modelsaves(0)
                elif model == 'LE-200-9':
                    dims = modelsaves(2)
                elif model == 'LE-200-12':
                    dims = modelsaves(4)
                elif model == 'LE-200-18':
                    dims = modelsaves(6)
                elif model == 'LE-200-24':
                    dims = modelsaves(8)
                elif model == 'LE-200-40':
                    dims = modelsaves(10)
                else:
                    print("Error not correct updraft model")
            elif draft == "Downdraft":
                if model == 'LE-200-4':
                    dims = modelsaves(1)
                elif model == 'LE-200-9':
                    dims = modelsaves(3)
                elif model == 'LE-200-12':
                    dims = modelsaves(5)
                elif model == 'LE-200-18':
                    dims = modelsaves(7)
                elif model == 'LE-200-24':
                    dims = modelsaves(9)
                elif model == 'LE-200-40':
                    dims = modelsaves(11)
                else:
                    print("Error not correct Downdraft model")
            else:
                print("Not Correct draft")

            ltext.delete("1.0", END)
            ltext.insert("1.0", dims[1])
            wtext.delete("1.0", END)
            wtext.insert("1.0", dims[0])
            htext.delete("1.0", END)
            htext.insert("1.0", dims[2])
            setglobaldims(dims[1], dims[0], dims[2])
            create()

    # create / recreate canvas
        def create():
            global cview
            if cview is "Default":
                cview = "Home"
            if cview is "Home" or cview is "Default":
                create_home()
            elif cview is "Free":
                create_free()
            elif cview is "Flat":
                create_flat()
            elif cview is "Stat":
                create_stat()
            else:
                print("error view not defined")
                return


    # Create floats from inputs
        def get_user_inputs():
            isfloat = bool(1)
            global wt, lt, ht
            global top
            global skirt
            top = 16
            skirt = 4
            try:
                ltt = float(ltext.get("1.0", 'end-1c'))
            except ValueError:
                print("Length must be a number! ")
                isfloat = False
            try:
                wtt = float(wtext.get("1.0", 'end-1c'))
            except ValueError:
                print("Width must be a number!")
                isfloat = False
            try:
                htt = float(htext.get("1.0", 'end-1c'))
            except ValueError:
                print("Height must be a number!")
                isfloat = False
            if isfloat == True:
                if (lt != ltt) or (wt != wtt) or (ht != htt):
                    modelcbox.set('Custom')

                wt, lt, ht = wtt, ltt, htt
            return wt, lt, ht, isfloat

    # Get points
        def get_points(view="home"):
            global wt
            global lt
            global ht
            global skirt
            global draft
            fpoints = GetSize.create_points(wt, ht, draft, "Front")
            spoints = GetSize.create_points(lt, ht, draft, "Side")
            if view == "home":
                tpoints = GetSize.create_points(wt, lt, draft, "Top")
                hpoints = GetSize.create_points(wt, lt, draft, "Hole")
                return fpoints, spoints, tpoints, hpoints
            elif view == "flat":
                locnsize = Mesurements.loc_size_output(fpoints, spoints)
                frontht = locnsize[8][2] + skirt
                if draft == "Updraft":
                    backht = locnsize[8][2]
                else:
                    backht = ht
                sideht = locnsize[2][2] + skirt
                frontpoints = GetSize.create_points(wt, frontht, draft, "Front")
                backpoints = GetSize.create_points(wt, backht, draft, "Front")
                leftpoints = GetSize.create_points(lt, sideht, draft, "Side")
                rightpoints = GetSize.create_points(lt, sideht, draft, "Side")
                return frontpoints, backpoints, leftpoints, rightpoints
            else:
                print("Error view not flat or home")

    # Display objects on canvas
        def create_home():
            global cview
            cview = "Home"
            Iso_View.reset_movement()
            canvas.delete("all")
            draw_home_canvas()


        def create_free():
            global cview
            cview = "Free"
            defmovement = 0, 0
            Iso_View.reset_movement()
            draw_iso_canvas(defmovement)

        def create_flat(face=None):
            global cview
            global flatface
            if face is None:
                face = flatface
            else:
                flatface = face
            cview = "Flat"
            Iso_View.reset_movement()
            canvas.delete("all")
            draw_flat_canvas(face)

        def create_stat():
            global cview
            cview = "Stat"
            canvas.delete("all")
            Iso_View.reset_movement()
            draw_stat_canvas()

        def draw_home_canvas():
            global draft
            global wt
            global lt
            global ht
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            draft = stylecbox.get()
            wt, lt, ht, isfloat = get_user_inputs()
            if not isfloat:
                return
            fpoints, spoints, tpoints, hpoints = get_points()

            # Scale points to canvas
            offset = 20
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
            isoscale = scale * .75  # temporary fix for oversized iso view
            isopoints = Iso_View.iso_points()
            scaledisopoints = []

            movement = 0, 0
            for n in range(len(isopoints)):
                r, zdepth = Iso_View.rotate_face(isopoints[n], movement)
                shape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, r, "iso", offset, lengthdif)
                scaledisopoints.append(shape)
                canvas.create_polygon(shape, fill="#ccc", outline="black", width=2)

            if var1.get():
                locnsize = Mesurements.loc_size_output(fpoints, spoints, tpoints, scaledisopoints)
                for each in locnsize:
                    if isinstance(each[2], str):
                        each[2] += "°"
                    else:
                        each[2] = round(each[2], 3)
                    canvas_id = canvas.create_text(each[0:2])
                    canvas.itemconfig(canvas_id, text=each[2], fill="#111", font=("Courier", 9))

            return

        def draw_flat_canvas(face):
            global draft
            global wt
            global lt
            global ht
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            draft = stylecbox.get()
            wt, lt, ht, isfloat = get_user_inputs()
            if not isfloat:
                return
            frontpoints, backpoints, leftpoints, rightpoints = get_points("flat")
            points = []
            if face == "Front":
                points = frontpoints
            elif face == "Back":
                points = backpoints
            elif face == "Left":
                points = leftpoints
            elif face == "Right":
                points = rightpoints

            else:
                print("Error not front back left or right")
            offset = 10
            windowratiox = canvasheight/canvaswidth
            windowratioy = canvaswidth/canvasheight
            xmax = points[5][0] - points[0][0]
            ymax = points[2][1] - points[0][1]
            xmax *= windowratiox
            ymax *= windowratioy

            if xmax >= ymax:
                scale = canvaswidth * .90 / (xmax + offset)
            else:
                scale = (canvasheight * .95) / (ymax + offset)

            if face == "Right":
                for n in range(len(points)):
                    points[n][0] = (points[n][0] - lt) * -1

            shape = GetSize.locate_points_canvas(
                canvaswidth, canvasheight, scale, points, "Flat", offset)
            canvas.create_polygon(shape, fill="#ccc", outline="black", width=2)

            if (draft != 'Downdraft') or (face != "Back"):
                canvas.create_line(points[1], points[4], width=1, dash=(10,10))

            canvas_id = canvas.create_text(canvaswidth/2, canvasheight)
            canvas.itemconfig(canvas_id, text=face, fill="#111", anchor=S, font=("Courier", 16))

            if var1.get():
                locnsize = Mesurements.loc_size_output_flat(points, face)
                for each in locnsize:
                    if isinstance(each[2], str):
                        if (draft != 'Downdraft') or (face != "Back"):
                            each[2] = "Bend " + each[2] + "° Down"
                        else: each[2] = ""
                    else:
                        each[2] = round(each[2], 3)
                    canvas_id = canvas.create_text(each[0:2])
                    canvas.itemconfig(canvas_id, text=each[2], fill="#111", font=("Courier", 9))


            buttonLeft = Button(self, text="Left", command=lambda: create_flat("Left"))
            buttonLeft.configure(width=8, pady=0)
            canvas.create_window(10, 10, anchor=NW, window=buttonLeft)
            buttonFront = Button(self, text="Front", command=lambda: create_flat("Front"))
            buttonFront.configure(width=8)
            canvas.create_window(110, 10, anchor=NW, window=buttonFront)
            buttonRight = Button(self, text="Right", command=lambda: create_flat("Right"))
            buttonRight.configure(width=8)
            canvas.create_window(210, 10, anchor=NW, window=buttonRight)
            buttonBack = Button(self, text="Back", command=lambda: create_flat("Back"))
            buttonBack.configure(width=8)
            canvas.create_window(310, 10, anchor=NW, window=buttonBack)

        def draw_iso_canvas(movement):
            canvas.delete("all")
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            global draft
            global wt
            global lt
            global ht
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
                runonce = False
                canvas_id = canvas.create_text(canvaswidth / 2, canvasheight / 8)
                canvas.itemconfig(canvas_id, font=("Courier", 20), text="Click and drag to rotate!")


        def draw_stat_canvas():
            global draft
            global wt
            global lt
            global ht
            draft = stylecbox.get()
            model = modelcbox.get()
            if modelcbox.get() == '':
                model = "Custom"
            wt, lt, ht, isfloat = get_user_inputs()
            if not isfloat:
                return

            def stat_text(varlabel, column, row, text):
                rowspace = 20
                row = row * rowspace + 30
                if column == 1:
                    loc = E
                    text += " "
                    column += 130
                else:
                    loc = W
                    column += 130

                varlabel = canvas.create_text(column, row)
                canvas.itemconfig(varlabel, text=text, width=130, anchor=loc, font=("Courier", 9))

            material = matcbox.get()
            gauge = gaugecbox.get()
            areasquare = Mesurements.get_area()
            gaugethick = 0 #in inches
            weightper = 0 # lb/ft²

        # gauge and weight from http://www.custompartnet.com/sheet-metal-gauge
            if material == "Stainless":
                if gauge == "16":
                    gaugethick = 0.0625
                    weightper = 2.601
                elif gauge == "14":
                    gaugethick = 0.0781
                    weightper = 3.250
                else:
                    print("Wrong Stainless gauge")
            elif material == "Galvanized":
                if gauge == "16":
                    gaugethick = 0.0635
                    weightper = 2.590
                elif gauge == "14":
                    gaugethick = 0.0785
                    weightper = 3.202
                else:
                    print("Wrong Galvanized gauge")
            else:
                print("Wrong Material")
            thickness = gaugethick

            squareft = areasquare * 0.00694444
            weight = weightper * squareft

            ppsqin = pricetext.get("1.0", 'end-1c')
            if ppsqin[0] != "$":
                ppsqin = "$" + ppsqin
                pricetext.delete("1.0", END)
                pricetext.insert("1.0", ppsqin)
            ppsqinint = float(ppsqin.lstrip("$"))
            price = "$" + str(round(areasquare * ppsqinint))

            stat_text("lbmod", 1, 1, "Model:")
            stat_text("lbmod1", 2, 1, model)
            stat_text("lblt", 1, 2, "Length:")
            stat_text("lblt1", 2, 2, lt)
            stat_text("lbwt", 1, 3, "Width:")
            stat_text("lbwt1", 2, 3, wt)
            stat_text("lbht", 1, 4, "Height:")
            stat_text("lbht1", 2, 4, ht)
            stat_text("lbdraft", 1, 5, "Draft:")
            stat_text("lbdraft1", 2, 5, draft)
            stat_text("lbmat", 1, 6, "Material:")
            stat_text("lbmat1", 2, 6, material)
            stat_text("lbgua", 1, 7, "Gauge:")
            stat_text("lbgua1", 2, 7, gauge)
            stat_text("lbthick", 1, 8, "Thickness:")
            stat_text("lbgua1", 2, 8, thickness)
            stat_text("lbarea", 1, 9, "Area:")
            areastr = str(areasquare)
            areastr2 = areastr[0:7] + " in²"
            stat_text("lbarea1", 2, 9, areastr2)
            stat_text("lbweight", 1, 10, "Weight:")
            weightstr = str(int(weight))
            weightstr2 = weightstr + " lbs."
            stat_text("lbweight", 2, 10, weightstr2)
            stat_text("lbpplb", 1, 11, "$ per in²:")
            stat_text("lbpplb1", 2, 11, ppsqin)
            stat_text("lbcost", 1, 12, "Price:")
            stat_text("lbcost1", 2, 12, price)

            # iso View
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()
            fpoints, spoints, tpoints, hpoints = get_points()

            # Scale points to canvas
            offset = 1
            scale, lengthdif = GetSize.find_scale(canvaswidth, canvasheight, tpoints, ht, offset)
            isoscale = scale * 1 # temporary fix for oversized iso view
            isopoints = Iso_View.iso_points()
            scaledisopoints = []
            lengthdif = -30, 70
            movement = 0, 0
            for n in range(len(isopoints)):
                r, zdepth = Iso_View.rotate_face(isopoints[n], movement)
                shape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, r, "iso", offset, lengthdif)
                scaledisopoints.append(shape)
                canvas.create_polygon(shape, fill="#ccc", outline="black", width=2)




    # Frame objects
        lbl = Label(self, text="Kiln Hoods Calculator", width=20)
        lbl.grid(row=0, column=1, columnspan=4)

        var1 = IntVar()
        var1.set(1)
        checkbut = Checkbutton(self, text="Measurements", variable=var1, command=lambda: create(), onvalue=1, offvalue=0)
        checkbut.grid(row=17, column=0, sticky=N)

        dbtn = Button(self, text="Defaults", width=10, command=setdef)
        dbtn.grid(row=11, column=0, sticky=S)
        hbtn = Button(self, text="Random", width=10, command=randsettings)
        hbtn.grid(row=12, column=0)
        quit_button = Button(self, text="Quit", width=10, command=self.quit)
        quit_button.grid(row=18, column=5)


        mlbl = Label(self, text="Model:", width=10, background="#aaa")
        mlbl.grid(row=1, column=0, sticky=S)
        modelcboxvar = 'cb1'
        modelcbox = Combobox(self, width=10, textvariable=modelcboxvar, state="readonly")
        modelcbox['values'] = ('Custom', 'LE-200-4', 'LE-200-9', 'LE-200-12', 'LE-200-18', 'LE-200-24', 'LE-200-40')
        modelcbox.grid(row=2, column=0, sticky=N)
        modelcbox.bind("<<ComboboxSelected>>", lambda _: setmodel())

        llbl = Label(self, text="Length:", width=10, background="#aaa")
        llbl.grid(row=3, column=0, sticky=S)
        ltext = Text(self, width=10, height=1)
        ltext.insert(END, "Length")
        ltext.grid(row=4, column=0)
        wbl = Label(self, text="Width:", width=10, background="#aaa")
        wbl.grid(row=5, column=0, sticky=S)
        wtext = Text(self, width=10, height=1)
        wtext.insert(END, "Width")
        wtext.grid(row=6, column=0)
        hlbl = Label(self, text="Height:", width=10, background="#aaa")
        hlbl.grid(row=7, column=0, sticky=S)
        htext = Text(self, width=10, height=1)
        htext.insert(END, "Height")
        htext.grid(row=8, column=0)
        stylelbl = Label(self, text="Draft Type:", width=10, background="#aaa")
        stylelbl.grid(row=9, column=0, sticky=S)

        matlbl = Label(self, text="Material:", width=13, background="#aaa")
        matlbl.grid(row=1, column=5, sticky=S)
        matcboxvar = 'cb3'
        matcbox = Combobox(self, width=10, textvariable=matcboxvar, state="readonly")
        matcbox['values'] = ('Stainless', 'Galvanized')
        matcbox.grid(row=2, column=5, sticky=S)
        matcbox.bind("<<ComboboxSelected>>", lambda _: create())
        gaugelbl = Label(self, text="Gauge:", width=10, background="#aaa")
        gaugelbl.grid(row=3, column=5, sticky=S)
        gaugecboxvar = 'cb4'
        gaugecbox = Combobox(self, width=10, textvariable=gaugecboxvar, state="readonly")
        gaugecbox['values'] = ('14', '16')
        gaugecbox.grid(row=4, column=5, sticky=S)
        gaugecbox.bind("<<ComboboxSelected>>", lambda _: create())
        pricelbl = Label(self, text="$ Per in²:", width=10, background="#aaa")
        pricelbl.grid(row=5, column=5, sticky=S)
        pricetext = Text(self, width=8, height=1)
        pricetext.insert(END, "$0.42")
        pricetext.grid(row=6, column=5)

        stylecboxvar = 'cb2'
        stylecbox = Combobox(self, width=10, textvariable=stylecboxvar, state="readonly")
        stylecbox['values'] = ('Updraft', 'Downdraft')
        stylecbox.grid(row=10, column=0, sticky=N)
        stylecbox.bind("<<ComboboxSelected>>", lambda _: setmodel())

        vlbl = Label(self, text="View:", width=10, background="#aaa")
        vlbl.grid(row=11, column=5, sticky=S)
        cbtn = Button(self, text="Home", width=10, command=create_home)
        cbtn.grid(row=12, column=5, sticky=N)
        flbtn = Button(self, text="Flat", width=10, command=create_flat)
        flbtn.grid(row=13, column=5, sticky=N)
        fbtn = Button(self, text="Free 3D", width=10, command=create_free)
        fbtn.grid(row=14, column=5, sticky=N)
        statbtn = Button(self, text="Stats", width=10, command=create_stat)
        statbtn.grid(row=15, column=5, sticky=N)

        fakelbl = Label(self, text="", width=0, background="#aaa")
        fakelbl.grid(row=15, column=0, sticky=N)


def size_list():
    global wt, lt, ht, top, skirt, draft
    sizelist = wt, lt, ht, top, skirt, draft
    return sizelist


def main():
    root = Tk()
    Example(root)
    root.mainloop()

