import math
import Gui
import operator
movex = 0
movey = 0


# All face point variables
# def iso_points():
def iso_points():
    width, length, height, top, skirt, draft = Gui.size_list()
    hwidth = width/2
    hlength = length/2
    hheight = height /2
    bpts = [0, 0, 0], [0, 0, length], [width, 0, length], [width, 0, 0]
    skpts = [0, skirt, 0], [0, skirt, length], [width, skirt, length], [width, skirt, 0]
    tptsud = [(width - top) / 2, height, (length - top) / 2], \
        [(width - top) / 2, height, ((length - top) / 2) + top], \
        [((width - top) / 2) + top, height, ((length - top) / 2) + top], \
        [((width - top) / 2) + top, height, (length - top) / 2]
    tptsdd = [(width - top) / 2, height, length - top], \
        [(width - top) / 2, height, length], \
        [((width - top) / 2) + top, height, length], \
        [((width - top) / 2) + top, height, length - top]

    for x in range(len(bpts)):
        bpts[x][0] -= hwidth
        bpts[x][1] -= hheight
        bpts[x][2] -= hlength
    for x in range(len(skpts)):
        skpts[x][0] -= hwidth
        skpts[x][1] -= hheight
        skpts[x][2] -= hlength
    for x in range(len(tptsud)):
        tptsud[x][0] -= hwidth
        tptsud[x][1] -= hheight
        tptsud[x][2] -= hlength
    for x in range(len(tptsdd)):
        tptsdd[x][0] -= hwidth
        tptsdd[x][1] -= hheight
        tptsdd[x][2] -= hlength

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
    points = []
    print("points = ", points)
    print("points length = ", len(points))
    print("zdepth = ", zdepth)
    print("zdepth length = ", len(zdepth))
    for x in range(len(isopoints)):
        print("iso [x] = ", isopoints[x])
        for xx in range(len(isopoints[x])):
            points.append(zdepth[x][xx])
            for xxx in range(len(isopoints[x][xx])):
                points.append(isopoints[x][xx][xxx])

    newnewpoints = []
    newnewpoints2 = []
    newnewpoints4 = []
    newnewpoints6 = []
    g = int()
    while (g < len(points)):
        newpoints = points[g:g + 3]
        newnewpoints.append(newpoints)
        g += 3
    j = int()
    while (j < len(newnewpoints)):
        newnewpoints1 = newnewpoints[j:j + 4]
        newnewpoints2.append(newnewpoints1)
        j += 4
    print("iso and zdepth = ", newnewpoints2)
    print("newnewpoints2 = ", newnewpoints2)
    newnewpoints2.sort(key=operator.itemgetter(0))


    print("newnewpoints2 = ", newnewpoints2)

    k = 0
    while (k < 9): # (len(newnewpoints2)):
        kk = 0
        # for kk in range(0, 4): # (len(newnewpoints2[k])):
        while (kk < 4):
            print("k = ", k)
            print("kk = ", kk)
            print("newnewpoints2[k][kk] = ", newnewpoints2[k][kk])
            newnewpoints3 = [newnewpoints2[k][kk][1], newnewpoints2[k][kk][2]]
            newnewpoints4.append(newnewpoints3)
            print("newnewpoints4 = ", newnewpoints4)
            kk += 1

        print("k = ", k)
        #print("newnewpoints4 = ", newnewpoints4)
        newnewpoints5 = newnewpoints4[k], newnewpoints4[k + 1], newnewpoints4[k + 2], newnewpoints4[k + 3]
        newnewpoints6.append(newnewpoints5)
        k += 1

    print("newnewpoints6 = ", newnewpoints6)
    print("isopoints =     ", isopoints)

    return newnewpoints6
    # return newnewpoints6


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

    # def project(self, win_width, win_height, fov, viewer_distance):
    #     """ Transforms this 3D point to 2D using a perspective projection. """
    #     factor = fov / (viewer_distance + self.z)
    #     x = self.x * factor + win_width / 2
    #     y = -self.y * factor + win_height / 2
    #     return Point3D(x, y, 1)
def reset_movement():
    global movex, movey
    movex = 22
    movey = -22

# def rotate_face(points, movement):
#     global movex, movey
#     movex += movement[0]
#     movey += movement[1]
#     angleX, angleY, angleZ = movey, movex, 0.00001
#     face = []
#     # depth = []
#     for n in range(len(points)):
#         i = Point3D(*points[n])
#         r = i.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
#         # p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
#         face.append(r.x), face.append(r.y)
#         # depth.append(r.z)
#     faceout = face[0:2], face[2:4], face[4:6], face[6:8]
#     faceout = faceout[0:len(points)]
#     #print(depth)
#     print("faceout = ", faceout)
#     return faceout, #depth

def rotate_face(points, movement):
    global movex, movey
    movex += movement[0]
    movey += movement[1]
    angleX, angleY, angleZ = movey, movex, 0.00001
    face = []
    zdepth = []
    for n in range(len(points)):
        i = Point3D(*points[n])
        r = i.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
        # p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
        face.append(r.x), face.append(r.y)
        zdepth.append(r.z)
    faceout = face[0:2], face[2:4], face[4:6], face[6:8]
    faceout = faceout[0:len(points)]
    return faceout, zdepth