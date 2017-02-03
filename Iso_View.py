import math
import Gui
import operator

movex, movey = 0, 0


def sub_half(var, wlh):
    for n in range(len(var)):
        for x in range(len(var[n])):
            var[n][x] -= wlh[x] / 2
    return var


# All face point variables
def iso_points():
    width, length, height, top, skirt, draft = Gui.size_list()
    wlh = [width, height, length]
    wt2 = (width - top) / 2
    lt2 = (length - top) / 2
    bpts = [0, 0, 0], [0, 0, length], [width, 0, length], [width, 0, 0]
    skpts = [0, skirt, 0], [0, skirt, length], [width, skirt, length], [width, skirt, 0]
    tptsud = [wt2, height, lt2], \
             [wt2, height, lt2 + top], \
             [wt2 + top, height, lt2 + top], \
             [wt2 + top, height, lt2]
    tptsdd = [wt2, height, length - top], \
             [wt2, height, length], \
             [wt2 + top, height, length], \
             [wt2 + top, height, length - top]
    bpts = sub_half(bpts, wlh)
    skpts = sub_half(skpts, wlh)
    tptsud = sub_half(tptsud, wlh)
    tptsdd = sub_half(tptsdd, wlh)
    if draft == "Downdraft":
        tpts = tptsdd
    elif draft == "Updraft":
        tpts = tptsud
    else:
        print("Draft must be Updraft or Downdraft >", draft, "<")
        return
    fskf = bpts[0], skpts[0], skpts[3], bpts[3]
    rskf = bpts[3], skpts[3], skpts[2], bpts[2]
    lskf = bpts[1], skpts[1], skpts[0], bpts[0]
    bskf = bpts[2], skpts[2], skpts[1], bpts[1]
    ff = skpts[0], tpts[0], tpts[3], skpts[3]
    rf = skpts[3], tpts[3], tpts[2], skpts[2]
    lf = skpts[1], tpts[1], tpts[0], skpts[0]
    bf = skpts[2], tpts[2], tpts[1], skpts[1]
    isopoints = bskf, lskf, bf, lf, rskf, rf, fskf, ff, tpts
    return isopoints


def draw_order(isopoints, zdepth):
    points, points1, points2, points3, points4 = [], [], [], [], []
    # Sort Z axis for each face, adding the largest to the smallest to use for draw order
    for x in range(len(zdepth)):
        zdepth[x].sort(reverse=True)
        zdepth[x][0] += zdepth[x][3]
    # Adding in z axis to x and y axis one long list z, x, y, z, x, y...
    for x in range(len(isopoints)):
        for xx in range(len(isopoints[x])):
            points.append(zdepth[x][xx])
            for xxx in range(len(isopoints[x][xx])):
                points.append(isopoints[x][xx][xxx])
    # group all sets of points [z, x, y]...
    x = 0
    while (x < len(points)):
        pointsx = points[x:x + 3]
        points1.append(pointsx)
        x += 3
    # group all points into faces [face[z, x, y], [face[z, x, y]....
    x = 0
    while (x < len(points1)):
        pointsx = points1[x:x + 4]
        points2.append(pointsx)
        x += 4
    # sort all faces by z axis
    points2.sort(key=operator.itemgetter(0), reverse=True)
    # go through all points and remove z axis
    x = 0
    while (x < 9):
        xx = 0
        while (xx < 4):
            pointsx = [points2[x][xx][1], points2[x][xx][2]]
            points3.append(pointsx)
            xx += 1
        x += 1
    # Format wasn't working changed from [[[]]] to [([])]
    x = 0
    while (x < 36):
        pointsx = points3[x], points3[x + 1], points3[x + 2], points3[x + 3]
        points4.append(pointsx)
        x += 4
    # and fucking finally it kinda works
    return points4



# code from http://codentronix.com/2011/04/20/simulation-of-3d-point-rotation-with-python-and-pygame/
class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)


def reset_movement():
    global movex, movey
    movex = 22
    movey = -22


def rotate_face(points, movement):
    global movex, movey
    movex += movement[0]
    movey += movement[1]
    angleX, angleY, angleZ = movey, movex, 0.00001
    face, zdepth = [], []
    for n in range(len(points)):
        i = Point3D(*points[n])
        r = i.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
        face.append(r.x), face.append(r.y)
        zdepth.append(r.z)
    faceout = face[0:2], face[2:4], face[4:6], face[6:8]
    faceout = faceout[0:len(points)]
    return faceout, zdepth