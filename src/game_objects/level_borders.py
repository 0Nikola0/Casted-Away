import pymunk as pm


class LevelBorders:
    def __init__(self, p0, p1, /, space, d):
        """

        p0 is top left level point (0 - d, 0 - d)?
        p1 is bottom right level point (width + d, height + d)?
        """
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(len(pts)):
            segment = pm.Segment(space.static_body, pts[i], pts[(i + 1) % 4], d)
            segment.elasticity = 0
            segment.friction = 1
            space.add(segment)
