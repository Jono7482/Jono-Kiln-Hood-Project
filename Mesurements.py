import math
import Gui
import Iso_View


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
    return measurementarray


def line_length(pointa, pointb):
    # sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    x = (pointb[0] - pointa[0]) ** 2
    y = (pointb[1] - pointa[1]) ** 2
    z = (pointb[2] - pointa[2]) ** 2
    l = math.sqrt(x + y + z)
    return l


def loc_size_output(front, side, top, iso):
    # sizearray format skirt, fhyp, top, wt, shyp, lt, ht, fbend, sbend, ffseem, bfseem
    sizearray = home_measurements()

    # locations front
    # width, angle, side face, top, skirt
    frontwidth = get_middle(front, 0, 5)
    frontwidth.append(sizearray[3])
    frontwidth[1] -= 9
    frontangle = front[1]
    frontangle.append(sizearray[8])
    frontangle[0] += 12
    frontangle[1] += 3
    frontface = get_middle(front, 1, 2)
    frontface.append(sizearray[1])
    frontface[0] += 25
    fronttop = get_middle(front, 2, 3)
    fronttop.append(sizearray[2])
    fronttop[1] += 9
    frontskirt = get_middle(front, 4, 5)
    frontskirt.append(sizearray[0])
    frontskirt[0] -= 12

    # locations side
    # length, height, top, front face, angle
    sidelength = get_middle(side, 0, 5)
    sidelength.append(sizearray[5])
    sidelength[1] -= 9
    sideheight = get_middle(side, 0, 2)
    sideheight.append(sizearray[6])
    sideheight[0] += 25
    sidetop = get_middle(side, 2, 3)
    sidetop.append(sizearray[2])
    sidetop[1] += 9
    sideface = get_middle(side, 3, 4)
    sideface.append(sizearray[4])
    sideface[0] -= 35
    sideface[1] += 6
    sideangle = side[4]
    sideangle.append(sizearray[7])
    sideangle[0] -= 25
    sideangle[1] += 3

    # locations top
    # width, length, top
    topwidth = get_middle(top, 0, 3)
    topwidth.append(sizearray[3])
    topwidth[1] -= 9
    toplength = get_middle(top, 2, 3)
    toplength.append(sizearray[5])
    toplength[0] -= 25
    toplength[1] -= 20
    toptop = get_middle(top, 4, 7)
    toptop.append(sizearray[2])
    toptop[1] += 9

    # locations iso
    # iso face format bskf, lskf, bf, lf, rskf, rf, fskf, ff, tpts [([x, y],[x....
    # seem front, seem back
    isoff = iso[7]
    isobf = iso[2]
    isoseemf = get_middle(isoff, 0, 1)
    isoseemf.append(sizearray[9])
    isoseemf[0] += 22
    isoseemf[1] += 12
    isoseemb = get_middle(isobf, 0, 1)
    isoseemb.append(sizearray[10])
    isoseemb[0] -= 12
    isoseemb[1] += 20

    locnsize = frontwidth, frontangle, frontface, fronttop, frontskirt, \
        sidelength, sideheight, sidetop, sideface, sideangle, \
        topwidth, toplength, toptop, isoseemf, isoseemb

    return locnsize  # format out [x, y, size]
