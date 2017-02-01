
import math


def print_size(length, width, height, style):
    facia = 4
    top = 16
    # Updraft
    if style in 'Updraft':
        # Front Bend Angle UD
        frontbendtril = float((length - top) / 2)
        frontbendhyp = math.sqrt((frontbendtril ** 2) + ((height - facia) ** 2))
        frontbendangle = math.degrees(math.atan((height-facia) / frontbendtril))
        print("Front Bend: " + str(int(90-frontbendangle)))

        # Side Bend Angle UD
        sidebendtril = float((width - top) / 2)
        sidebendhyp = math.sqrt((sidebendtril ** 2) + ((height - facia) ** 2))
        sidebendangle = math.degrees(math.atan((height-facia) / sidebendtril))
        print("Side Bend: " + str(int(90-sidebendangle)))
        print("UP Draft")

        # Corner lengths
        print("Front Face Length: " + str(frontbendhyp))
        print("Sides Face Length: " + str(sidebendhyp))
    # DownDraft
    elif style in 'Downdraft':
        # Front Bend Angle DD
        ddfrontbendtril = float(length - top)
        # ddfrontbendhyp = math.sqrt((ddfrontbendtril ** 2) + ((height - facia) ** 2))
        ddfrontbendangle = math.degrees(math.atan((height-facia) / ddfrontbendtril))
        print("Front Bend: " + str(int(90-ddfrontbendangle)))

        # Side Bend Angle DD
        ddsidebendtril = float((width - top) / 2)
        # ddsidebendhyp = math.sqrt((ddsidebendtril ** 2) + ((height - facia) ** 2))
        ddsidebendangle = math.degrees(math.atan((height-facia) / ddsidebendtril))
        print("Side Bend: " + str(int(90-ddsidebendangle)))
        print("Down Draft")
    else:
        print("You typed ", style, ".")
        print("Must be UD or DD")


def create_points(x, y, draft, face):
    # number points starting 0 bottom left (0,0) going clockwise
    # Updraft & Downdraft
    facia = float(4)
    top = float(16)

    if (draft == "Updraft" or face == "Front") and (face != "Top" and face != "Hole"):
        p0 = [0, 0]
        p1 = [0, facia]
        p2 = [(x-top)/2, y]
        p3 = [(p2[0])+top, y]
        p4 = [x, facia]
        p5 = [x, 0]
        points = p0, p1, p2, p3, p4, p5
        return points
    elif draft == "Downdraft" and face == "Side":
        p0 = [0, 0]
        p1 = [0, facia]
        p2 = [0, y]
        p3 = [top, y]
        p4 = [x, facia]
        p5 = [x, 0]
        points = p0, p1, p2, p3, p4, p5
        return points
    elif face == "Top" or "Hole":
        p0 = [0, 0]
        p1 = [0, y]
        p2 = [x, y]
        p3 = [x, 0]

        if draft == "Updraft":
            p4 = [(x-top)/2, (y-top)/2]
            p5 = [p4[0], p4[1]+top]
            p6 = [p4[0]+top, p5[1]]
            p7 = [p6[0], p4[1]]
            points = p0, p1, p2, p3, p4, p5, p6, p7
        elif draft == "Downdraft":
            p4 = [(x-top)/2, y-top]
            p5 = [p4[0], y]
            p6 = [p4[0]+top, y]
            p7 = [p6[0], p4[1]]
            points = p0, p1, p2, p3, p4, p5, p6, p7
        else:
            print("Face is Top/Hole but invalid draft >", draft, "<")
            return

        if face == "Hole":
            hole = 12
            holeoffset = (top-hole)/2
            h1 = [p5[0]+holeoffset, p5[1]-holeoffset]
            h2 = [p7[0]-holeoffset, p7[1]+holeoffset]
            points = h1, h2
            return points
        else:
            return points

    else:
        print("Error in create_points style got >", draft, "< and >", face, "<")
        return


def find_scale(canvasx, canvasy, tpoints, height, offset):
    # get length of longest X and Y lines
    xlength = (tpoints[2][0] + tpoints[2][1]) + offset
    ylength = tpoints[2][1] + height + offset

    # Create scale on X or Y depending on what is larger
    # in relation to canvas size
    if canvasx / xlength <= canvasy / ylength:
        scale = float(canvasx) / xlength
    else:
        scale = float(canvasy) / ylength

    xlengthdif = (tpoints[2][0] - tpoints[2][1])
    ylengthdif = tpoints[2][1] - height
    lengthdif = xlengthdif, ylengthdif
    return scale, lengthdif

def find_iso_scale(canvasx, canvasy, isopoints, height, offset):
    # get length of longest X, Y, z lines
    xlength = (isopoints[6][3][0] - isopoints[6][0][0]) + offset
    ylength = height + offset
    zlength = (isopoints[1][0][2] - isopoints[1][3][2]) + offset
    if canvasx / xlength <= canvasy / ylength and canvasx / xlength <= canvasx / zlength:
        scale = float(canvasx) / xlength
    elif canvasy / ylength <= canvasx / xlength and canvasy / ylength <= canvasy / zlength:
        scale = float(canvasy) / ylength
    else:
        scale = float(canvasx) / zlength
    lengthdif = 0, 0
    return scale, lengthdif


def locate_points_canvas(canvasx, canvasy, scale, points, face, offset, lengthdif):

    # Scale points
    lengthdifx = lengthdif[0] * (scale / 2)
    lengthdify = lengthdif[1] * (scale / 2)
    for n in range(len(points)):
        points[n][0] = (points[n][0] * scale) + offset
        points[n][1] = (points[n][1] * scale) + offset

    # flip y axis put 0,0 in bottom left
    for index in range(len(points)):
        points[index][1] = canvasy - points[index][1]

    # Front return points Side Move to bottom right then return points

    if face is "front":
        return points
    elif face is "side":
        for x in range(len(points)):
            points[x][0] += (canvasx / 2) + lengthdifx
        return points
    elif face is "top" or face is "hole":
        for x in range(len(points)):
            points[x][1] -= (canvasy / 2) - lengthdify
        return points
    elif face == "iso":
        for x in range(len(points)):
            points[x][0] += canvasx - (canvasx / 4) + lengthdifx
            points[x][1] -= canvasy - (canvasy / 4) - lengthdify
        return points
    elif face is "free":
        for x in range(len(points)):
            points[x][0] += canvasx - (canvasx / 2)
            points[x][1] -= canvasy - (canvasy / 2)
        return points
    else:
        print("locate_points_canvas face != front or side")
        return
