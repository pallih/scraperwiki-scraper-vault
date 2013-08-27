# point_in_polygon() uses the 'Ray Casting' method to determine whether
# a given point (as a longitude, latitude) lies within a given area
# (as a list of longitude, latitude tuples).

def point_in_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

# Test - will return True, True, False
# polygon = [(0,10),(10,10),(10,0),(0,0)]
# print point_in_polygon(5,5,polygon)
# print point_in_polygon(10,10,polygon)
# print point_in_polygon(15,5,polygon)# point_in_polygon() uses the 'Ray Casting' method to determine whether
# a given point (as a longitude, latitude) lies within a given area
# (as a list of longitude, latitude tuples).

def point_in_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

# Test - will return True, True, False
# polygon = [(0,10),(10,10),(10,0),(0,0)]
# print point_in_polygon(5,5,polygon)
# print point_in_polygon(10,10,polygon)
# print point_in_polygon(15,5,polygon)# point_in_polygon() uses the 'Ray Casting' method to determine whether
# a given point (as a longitude, latitude) lies within a given area
# (as a list of longitude, latitude tuples).

def point_in_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

# Test - will return True, True, False
# polygon = [(0,10),(10,10),(10,0),(0,0)]
# print point_in_polygon(5,5,polygon)
# print point_in_polygon(10,10,polygon)
# print point_in_polygon(15,5,polygon)