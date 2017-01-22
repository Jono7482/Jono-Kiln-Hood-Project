

def get_measurement_cords(points):
    facia = break_down_list_float(points, 0, 1)
    # seem = break_down_list_float(points, 1, 2)
    top = break_down_list_float(points, 2, 3)
    bottom = break_down_list_float(points, 5, 0)
    heightindex = [bottom, top]
    height = break_down_list_float(heightindex, 0, 1)

    facia[0] += 20
    # seem[0] += 20
    top[1] += 10
    bottom[1] -= 10

    cords = [facia, top, bottom, height]
    return cords


def break_down_list_float(variable, index1, index2):
    aa = variable[index1][0]
    ab = variable[index1][1]
    ba = variable[index2][0]
    bb = variable[index2][1]
    x = (aa + ba) / 2
    y = (ab + bb) / 2
    xy = [x, y]
    return xy


def size_array(x, ht):
    facia = 4
    top = 16
    sizearray = [facia, top, x, ht]
    return sizearray
