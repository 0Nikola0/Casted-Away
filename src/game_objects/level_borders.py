import pymunk as pm
import src.settings as s


class LevelBorders:
    def __init__(self, p0, p1, /, space, d):
        """

        p0 is top left level point (0 - d, 0 - d)?
        p1 is bottom right level point (width + d, height + d)?
        """
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0 - d, y0 + d), (x1 + d, y0 + d), (x1 + d, y1 - d), (x0 - d, y1 - d)]
        for i in range(len(pts)):
            segment = pm.Segment(space.static_body, pts[i], pts[(i + 1) % 4], d)
            segment.elasticity = 0
            segment.friction = 1

            segment.collision_type = s.LEVEL_BORDERS_COLLISION_TYPE

            space.add(segment)
