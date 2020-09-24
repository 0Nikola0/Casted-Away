import pymunk as pm
import src.settings as s


class LevelBorders:
    __LEVEL_BORDERS_IDS = set()

    def __init__(self, p0, p1, /, space, d):
        self.segments = []

        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0 - d, y0 + d), (x1 + d, y0 + d), (x1 + d, y1 - d), (x0 - d, y1 - d)]
        for i in range(len(pts)):
            segment = pm.Segment(space.static_body, pts[i], pts[(i + 1) % 4], d)
            segment.elasticity = 0
            segment.friction = 1

            segment.collision_type = s.get_id(LevelBorders.__LEVEL_BORDERS_IDS)

            space.add(segment)
            self.segments.append(segment)

    @property
    def get_segments(self):
        return self.segments
