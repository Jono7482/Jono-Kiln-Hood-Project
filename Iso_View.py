import math
import Gui


# width = 52
# length = 60.5
# height = 24
# skirt = 4
# top = 16
# draft = "Downdraft"

    # All face point variables
def iso_points():
    width, length, height, top, skirt, draft = Gui.size_list()
    bpts = [0, 0, 0], [0, 0, length], [width, 0, length], [width, 0, 0]
    skpts = [0, skirt, 0], [0, skirt, length], [width, skirt, length], [width, skirt, 0]
    tptsud = [(width - top) / 2, height, (length - top) / 2], \
           [(width - top)/2, height, ((length - top)/2) + top], \
           [((width - top)/2) + top, height, ((length - top)/2) + top], \
           [((width - top)/2) + top, height, (length - top)/2]
    tptsdd = [(width - top) / 2, height, length - top], \
           [(width - top)/2, height, length], \
           [((width - top)/2) + top, height, length], \
           [((width - top)/2) + top, height, length - top]

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

    # if face == "fskf":
    #     return fskf
    # elif face == "rskf":
    #     return rskf
    # elif face == "lskf":
    #     return lskf
    # elif face == "bskf":
    #     return bskf
    # elif face == "ff":
    #     return ff
    # elif face == "rf":
    #     return rf
    # elif face == "lf":
    #     return lf
    # elif face == "bf":
    #     return bf
    # elif face == "tpts":
    #     return tpts


    # elif face == "holef":
    #     hole = 12
    #     holeoffset = 0 #(top - hole) / 2
    #     h1 = [tpts[0][0] + holeoffset,tpts[3][1], tpts[0][2] - holeoffset]
    #     h2 = [tpts[2][0] - holeoffset,tpts[1][1], tpts[2][2] - holeoffset]
    #     holef = h2, h1
    #     print("holef", holef)
    #     return holef

    # else:
    #     print("Error face must match a variable name")


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


def rotate_face(points):
    angleX, angleY, angleZ = -22, 22, 0.00001
    face = []
    for n in range(len(points)):
        i = Point3D(*points[n])
        r = i.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
        # p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
        face.append(r.x), face.append(r.y)
    faceout = face[0:2], face[2:4], face[4:6], face[6:8]
    faceout = faceout[0:len(points)]
    return faceout


# *ff[n]