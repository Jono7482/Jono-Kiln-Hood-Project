import math
import Gui
import Iso_View

def get_measurement_cords(points):
    facia = get_middle(points, 0, 1)
    # seem = break_down_list_float(points, 1, 2)
    top = get_middle(points, 2, 3)
    bottom = get_middle(points, 5, 0)
    heightindex = [bottom, top]
    height = get_middle(heightindex, 0, 1)

    facia[0] += 20
    # seem[0] += 20
    top[1] += 10
    bottom[1] -= 10

    cords = [facia, top, bottom, height]
    return cords


def size_array(x, ht):
    facia = 4
    top = 16
    sizearray = [facia, top, x, ht]
    return sizearray


def get_middle(variable, index1, index2):
    aa = variable[index1][0]
    ab = variable[index1][1]
    ba = variable[index2][0]
    bb = variable[index2][1]
    x = (aa + ba) / 2
    y = (ab + bb) / 2
    xy = [x, y]
    return xy


def bend_angles():
    # wt, lt, ht, top, skirt, draft
    sizelist = Gui.size_list()
    wt, lt, ht, top, skirt = sizelist[0:5]
    # Updraft
    if sizelist[5] == "Updraft":
        # Front Bend Angle UD
        frontbendtril = float((lt - top) / 2)
        frontbendangle = math.degrees(math.atan((ht-skirt) / frontbendtril))
        frontbend = round(90-frontbendangle)
        # Side Bend Angle UD
        sidebendtril = float((wt - top) / 2)
        sidebendangle = math.degrees(math.atan((ht-skirt) / sidebendtril))
        sidebend = round(90-sidebendangle)
        return frontbend, sidebend

    # DownDraft
    else:
        # Front Bend Angle DD
        ddfrontbendtril = float(lt - top)
        ddfrontbendangle = math.degrees(math.atan((ht-skirt) / ddfrontbendtril))
        frontbend = round(90-ddfrontbendangle)
        # Side Bend Angle DD
        ddsidebendtril = float((wt - top) / 2)
        ddsidebendangle = math.degrees(math.atan((ht-skirt) / ddsidebendtril))
        sidebend = round(90-ddsidebendangle)
        return frontbend, sidebend


def home_measurements():
    # wt, lt, ht, top, skirt, draft
    sizelist = Gui.size_list()
    wt, lt, ht, top, skirt = sizelist[0:5]
    # bskf, lskf, bf, lf, rskf, rf, fskf, ff, tpts
    isopoints = Iso_View.iso_points()
    # bend angles
    fbend, sbend = bend_angles()

    fhyp = math.hypot((wt - top) / 2, ht - skirt)  # length of side face as seen from front
    shypud = math.hypot((lt - top) / 2, ht - skirt)  # UD length of front face as seen from side
    shypdd = math.hypot(lt - top, ht - skirt)  # DD length of front face as seen from side
    if sizelist[5] == "Updraft":
        shyp = shypud
    else:
        shyp = shypdd
    ffseem = line_length(isopoints[7][0], isopoints[7][1])  # iso seem between front and side
    bfseem = line_length(isopoints[2][0], isopoints[2][1])  # iso seem between back and side
    measurementarray = [skirt, fhyp, top, wt, shyp, lt, ht, fbend, sbend, ffseem, bfseem]
    for x in range(len(measurementarray)):
        print(x, " = ", measurementarray[x])
    return measurementarray


# sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
def line_length(pointa, pointb):
    x = (pointb[0] - pointa[0]) ** 2
    y = (pointb[1] - pointa[1]) ** 2
    z = (pointb[2] - pointa[2]) ** 2
    l = math.sqrt(x + y + z)
    return l


def loc_size_output(front, side, top, iso):
    # format out [x, y, size]
    sizearray = home_measurements()

    # locations front
    # width, angle, side face, top, skirt
    frontwidth = get_middle(front, 0, 5)
    frontangle = front[1]
    frontface = get_middle(front, 1, 2)
    fronttop = get_middle(front, 2, 3)
    frontskirt = get_middle(front, 4, 5)

    # locations side
    # length, height, top, front face, angle
    sidelength = get_middle(side, 0, 5)
    sideheight = get_middle(side, 0, 2)
    sidetop = get_middle(side, 2, 3)
    sideface = get_middle(side, 3, 4)
    sideangle = side[4]

    # locations top
    # width, length, top
    topwidth = get_middle(top, 0, 3)
    toplength = get_middle(top, 2, 3)
    toptop = get_middle(top, 4, 7)

    # locations iso
    # seem front, seem back
    print(iso)

