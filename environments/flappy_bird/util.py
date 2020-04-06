def clamp(val, minimum, maximum):
    return val if minimum < val < maximum else minimum if val <= minimum else maximum

def collide(rect, circle):
    closest_x = clamp(circle[0], rect[0], rect[0] + rect[2])
    closest_y = clamp(circle[1], rect[1], rect[1] + rect[3])
    dist_x = circle[0] - closest_x
    dist_y = circle[1] - closest_y
    return dist_x ** 2 + dist_y ** 2 < circle[2] ** 2