import random
from tkinter import *
from tkinter.ttk import Combobox

import GetSize
import Mesurements
import Iso_View


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

    # input testing amounts
        def setdef():
            ltext.delete("1.0", END)
            ltext.insert("1.0", "60.5")
            wtext.delete("1.0", END)
            wtext.insert("1.0", "52")
            htext.delete("1.0", END)
            htext.insert("1.0", "24")
            stylecbox.set("Downdraft")

        # time_loop(False)
        def randsettings():
            ltext.delete("1.0", END)
            ltext.insert("1.0", random.randint(50, 100))
            wtext.delete("1.0", END)
            wtext.insert("1.0", random.randint(50, 100))
            htext.delete("1.0", END)
            htext.insert("1.0", random.randint(20, 60))
            randdraft = "Downdraft", "Updraft"
            stylecbox.set(randdraft[random.randint(0, 1)])
            create()

    # Create floats run getsize
        def create():
            canvasheight = canvas.winfo_height()
            canvaswidth = canvas.winfo_width()

            canvas.delete("all")
            isfloat = bool(1)
            lt = float
            wt = float
            ht = float
            draft = stylecbox.get()

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

            if isfloat:
                # Get points
                fpoints = GetSize.create_points(wt, ht, draft, "Front")
                spoints = GetSize.create_points(lt, ht, draft, "Side")
                tpoints = GetSize.create_points(wt, lt, draft, "Top")
                hpoints = GetSize.create_points(wt, lt, draft, "Hole")

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

                # get measurement locations
                frontcords = Mesurements.get_measurement_cords(frontshape)
                sidecords = Mesurements.get_measurement_cords(sideshape)

                # Get size arrays
                frontsizearray = Mesurements.size_array(wt, ht)
                sidesizearray = Mesurements.size_array(lt, ht)

                # Print shapes to canvas
                canvas.create_polygon(frontshape, fill="#ccc", outline="black", width=2)
                canvas.create_polygon(sideshape, fill="#ccc", outline="black", width=2)
                canvas.create_polygon(topshape[0:4], fill="#ccc", outline="black", width=2)
                canvas.create_polygon(topshape[4:8], fill="#ccc", outline="black", width=2)
                canvas.create_line(topshape[0], topshape[4], width=2)
                canvas.create_line(topshape[1], topshape[5], width=2)
                canvas.create_line(topshape[2], topshape[6], width=2)
                canvas.create_line(topshape[3], topshape[7], width=2)
                canvas.create_oval(holeshape, width=2, fill="#fff")

                # Testing iso view
                isoscale = scale * .85 # temporary fix for oversized iso view

                bskf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "bskf")
                bsk = Iso_View.rotate_face(bskf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, bsk, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                bf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "bf")
                b = Iso_View.rotate_face(bf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, b, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                lskf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "lskf")
                lsk = Iso_View.rotate_face(lskf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, lsk, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                lf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "lf")
                l = Iso_View.rotate_face(lf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, l, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                rskf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "rskf")
                rsk = Iso_View.rotate_face(rskf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, rsk, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                rf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "rf")
                r = Iso_View.rotate_face(rf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, r, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                fskf = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "fskf")
                fsk = Iso_View.rotate_face(fskf)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, fsk, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                ff = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "ff")
                ff = Iso_View.rotate_face(ff)
                ffshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, ff, "iso", offset, lengthdif)
                canvas.create_polygon(ffshape, fill="#ccc", outline="black", width=2)

                tpts = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "tpts")
                tf = Iso_View.rotate_face(tpts)
                tfshape = GetSize.locate_points_canvas(
                    canvaswidth, canvasheight, isoscale, tf, "iso", offset, lengthdif)
                canvas.create_polygon(tfshape, fill="#ccc", outline="black", width=2)

                # holef = Iso_View.iso_points(wt, lt, ht, 4, 16, draft, "holef")
                # print("hole before rotate", holef)
                # hole = Iso_View.rotate_face(holef)
                # print("hole before locate", hole)
                # holeshape = GetSize.locate_points_canvas(
                #     canvaswidth, canvasheight, isoscale, hole, "iso", offset, lengthdif)
                # canvas.create_oval(holeshape, fill="#fff", outline="black", width=2)


                # print measurements to canvas
                for n in range(0, 4):
                    canvas_id = canvas.create_text(frontcords[n])
                    canvas.itemconfig(canvas_id, text=frontsizearray[n])
                for n in range(0, 4):
                    canvas_id = canvas.create_text(sidecords[n])
                    canvas.itemconfig(canvas_id, text=sidesizearray[n])
                return

            else:
                return

    # Frame objects
        lbl = Label(self, text="Kiln Hoods Calculator", width=20)
        lbl.grid(row=0, column=1, columnspan=2)
        dbtn = Button(self, text="Defaults", width=10, command=setdef)
        dbtn.grid(row=11, column=3, sticky=E)
        hbtn = Button(self, text="Random", width=10, command=randsettings)
        hbtn.grid(row=11, column=0)
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

        cbtn = Button(self, text="Create", width=10, command=create)
        cbtn.grid(row=10, column=0, sticky=N)


def main():

    root = Tk()
    Example(root)
    root.mainloop()
