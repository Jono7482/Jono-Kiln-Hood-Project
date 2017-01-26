# 7 visible sides + hole and back and left skirt
# all have 4 points except hole 2 points
import math

width = 52
length = 60.5
height = 24
skirt = 4
top = 16
draft = "Downdraft"


# # Create faces in 3D
# front_skirt = [0, 0, 0], [0, skirt, 0], [width, skirt, 0], [width, 0, 0]
# right_skirt = [width, 0, 0], [width, skirt, 0], [width, skirt, length], [width, 0, length]
# left_skirt = [0, 0, length], [0, skirt, length], [0, skirt, 0], [0, 0, 0]
# front = [0, skirt, 0], [(width-top)/2, height, (length-top)/2], [((width-top)/2)+top,
#             height, (length-top)/2], [width, skirt, 0]
# right = [width, skirt, 0], [((width-top)/2)+top, height, (length-top)/2],\
#             [((width-top)/2)+top, height, ((length-top)/2)+top], [width, skirt, length]
# left = [0, skirt, length], [(width-top)/2, height, ((length-top)/2)+top], [(width-top)/2,
#             height, (length-top)/2], [0, skirt, 0]
# back = [width, skirt, length], [((width-top)/2)+top, height, ((length-top)/2)+top],\
#             [(width-top)/2, height, ((length-top)/2)+top], [0, skirt, length]
# topf = [(width-top)/2, height, (length-top)/2], [(width-top)/2, height, ((length-top)/2)+top],\
#             [((width-top)/2)+top, height, ((length-top)/2)+top], [((width-top)/2)+top, height,
#             (length-top)/2]


# All face point variables
bpts = [0, 0, 0], [0, 0, length], [width, 0, length], [width, 0, 0]
skpts = (0, skirt, 0), [0, skirt, length], [width, skirt, length], [width, skirt, 0]
tptsud = [(width - top) / 2, height, (length - top) / 2], \
       [(width - top)/2, height, ((length - top)/2) + top], \
       [((width - top)/2) + top, height, ((length - top)/2) + top], \
       [((width - top)/2) + top, height, (length - top)/2]
tptsdd = [(width - top) / 2, height, length - top], \
       [(width - top)/2, height, length], \
       [((width - top)/2) + top, height, length], \
       [((width - top)/2) + top, height, length - top]
tpts = tptsud
if draft == "Downdraft":
    tpts = tptsdd
else:
    print("Draft must be Updraft or Downdraft >", draft, "<")
fskf = bpts[0], skpts[0], skpts[3], bpts[3]
rskf = bpts[3], skpts[3], skpts[2], bpts[2]
lskf = bpts[1], skpts[1], skpts[0], bpts[0]
bskf = bpts[2], skpts[2], skpts[1], bpts[1]
ff = skpts[0], tpts[0], tpts[3], skpts[3]
rf = skpts[3], tpts[3], tpts[2], skpts[2]
lf = skpts[1], tpts[1], tpts[0], skpts[0]
bf = skpts[2], tpts[2], tpts[1], skpts[1]


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
        return (self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return (x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return (x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)
print(ff[0])
print(ff[0][0])

test = Point3D(ff[0][0], ff[0][1], ff[0][2])
print(test)
test2 = test.rotateX(180)
print(test2)
test3 = test.rotateY(180)
print(test3)
test4 = test.rotateZ(180)
print(test4)
