import math
import Gui
import Iso_View
import GetSize


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


def loc_size_output(front, side, top=None, iso=None):
    # sizearray format skirt, fhyp, top, wt, shyp, lt, ht, fbend, sbend, ffseem, bfseem
    sizearray = home_measurements()

    # locations front
    # width, angle, side face, top, skirt
    frontwidth = get_middle(front, 0, 5)
    frontwidth.append(sizearray[3])
    frontwidth[1] -= 9
    frontangle = front[1]
    frontangle.append(str(sizearray[8]))
    frontangle[0] += 16
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
    sideangle.append(str(sizearray[7]))
    sideangle[0] -= 25
    sideangle[1] += 3

    # locations top
    # width, length, top
    if top != None:
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
    else:
        topwidth, toplength, toptop = None, None, None

    # locations iso
    # iso face format bskf, lskf, bf, lf, rskf, rf, fskf, ff, tpts [([x, y],[x....
    # seem front, seem back
    if iso != None:
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
    else:
        isoseemf, isoseemb = None, None

    locnsize = frontwidth, frontangle, frontface, fronttop, frontskirt, \
        sidelength, sideheight, sidetop, sideface, sideangle, \
        topwidth, toplength, toptop, isoseemf, isoseemb

    return locnsize  # format out [x, y, size]

def loc_size_output_flat(points, face):
    # sizearray format skirt, fhyp, top, wt, shyp, lt, ht, fbend, sbend, ffseem, bfseem
    sizearray = home_measurements()

    if face is "Front":
        # locations front
        # width, hyp, top, skirt
        frontwidth = get_middle(points, 0, 5)
        frontwidth.append(sizearray[3])
        frontwidth[1] -= 9
        fronthyp = get_middle(points, 1, 2)
        fronthyp.append(sizearray[9])
        fronthyp[0] += 29
        fronttop = get_middle(points, 2, 3)
        fronttop.append(sizearray[2])
        fronttop[1] += 9
        frontskirt = get_middle(points, 4, 5)
        frontskirt.append(sizearray[0])
        frontskirt[0] -= 12
        frontheighttemp = get_middle(points, 2, 3), get_middle(points, 0, 5)
        frontheight = get_middle(frontheighttemp, 0, 1)
        frontheight.append(sizearray[4] + sizearray[0])
        frontheight[0] += 1
        frontbend = get_middle(points, 1, 4)
        frontbend.append(str(sizearray[7]))
        frontbend[1] -= 9

        locnsize = frontwidth, fronthyp, fronttop, frontskirt, frontheight, frontbend

    if face is "Back":
        # locations front
        # width, hyp, top, skirt
        backwidth = get_middle(points, 0, 5)
        backwidth.append(sizearray[3])
        backwidth[1] -= 9
        backhyp = get_middle(points, 1, 2)
        backhyp.append(sizearray[10])
        backhyp[0] += 29
        backtop = get_middle(points, 2, 3)
        backtop.append(sizearray[2])
        backtop[1] += 9
        backskirt = get_middle(points, 4, 5)
        backskirt.append(sizearray[0])
        backskirt[0] -= 12
        backheighttemp = get_middle(points, 2, 3), get_middle(points, 0, 5)
        backheight = get_middle(backheighttemp, 0, 1)
        backheight.append(sizearray[1] + sizearray[0])
        backheight[0] += 1
        backbend = get_middle(points, 1, 4)
        backbend.append(str(sizearray[7]))
        backbend[1] -= 9

        locnsize = backwidth, backhyp, backtop, backskirt, backheight, backbend

    if face is "Left":
        # locations side
        # length, height, top, front face, skirt
        leftlength = get_middle(points, 0, 5)
        leftlength.append(sizearray[5])
        leftlength[1] -= 9
        leftheight = get_middle(points, 0, 2)
        leftheight.append(sizearray[10] + sizearray[0])
        leftheight[0] += 29
        lefttop = get_middle(points, 2, 3)
        lefttop.append(sizearray[2])
        lefttop[1] += 9
        leftface = get_middle(points, 3, 4)
        leftface.append(sizearray[9])
        leftface[0] -= 35
        leftface[1] += 6
        leftskirt = get_middle(points, 4, 5)
        leftskirt.append(sizearray[0])
        leftskirt[0] -= 12
        leftbend = get_middle(points, 1, 4)
        leftbend.append(str(sizearray[8]))
        leftbend[1] -= 9

        locnsize = leftlength, leftheight, lefttop, leftface, leftskirt, leftbend

    if face is "Right":
        # locations side
        # length, height, top, front face, skirt
        rightlength = get_middle(points, 0, 5)
        rightlength.append(sizearray[5])
        rightlength[1] -= 9
        rightheight = get_middle(points, 0, 2)
        rightheight.append(sizearray[10] + sizearray[0])
        rightheight[0] -= 28
        righttop = get_middle(points, 2, 3)
        righttop.append(sizearray[2])
        righttop[1] += 9
        rightface = get_middle(points, 3, 4)
        rightface.append(sizearray[9])
        rightface[0] += 29
        rightface[1] += 6
        rightskirt = get_middle(points, 4, 5)
        rightskirt.append(sizearray[0])
        rightskirt[0] -= 12
        rightbend = get_middle(points, 1, 4)
        rightbend.append(str(sizearray[8]))
        rightbend[1] -= 9

        locnsize = rightlength, rightheight, righttop, rightface, rightskirt, rightbend

    return locnsize

def get_area():
    # wt, lt, ht, top, skirt, draft
    wt, lt, ht, top, skirt, draft = Gui.size_list()

    fpoints = GetSize.create_points(wt, ht, draft, "Front")
    spoints = GetSize.create_points(lt, ht, draft, "Side")

    locnsize = loc_size_output(fpoints, spoints)
    frontht = locnsize[8][2] + skirt
    if draft == "Updraft":
        backht = locnsize[8][2]
    else:
        backht = ht
    sideht = locnsize[2][2] + skirt

    frontarea = (wt * frontht) - ((frontht - skirt) * ((wt - top)/2))
    backarea = (wt * backht) - ((backht - skirt) * ((wt - top)/2))
    if draft == "Updraft":
        sidearea = (lt * sideht) - ((sideht - skirt) * ((lt - top)/2))
    else:
        sidearea = (lt * sideht) - ((sideht - skirt) * ((lt - top)/2))
    toparea = top * top
    area = frontarea + backarea + (sidearea * 2) + toparea

    return area


