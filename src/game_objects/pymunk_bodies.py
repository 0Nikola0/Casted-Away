import pymunk as pm
import src.settings as s


class KinematicRigidBody:
    def __init__(self, pos, size, collision_type, space):
        self.body = pm.Body(mass=1, moment=pm.inf, body_type=pm.Body.DYNAMIC)
        self.control_body = pm.Body(body_type=pm.Body.KINEMATIC)

        pm_x, pm_y = s.flip_y(pos)
        pm_size_x, pm_size_y = size

        self.body.position = pm_x + pm_size_x // 2, pm_y - pm_size_y // 2  # body.position == rect.center
        self.control_body.position = self.body.position

        self.shape = pm.Poly.create_box(self.body, size)

        self.shape.collision_type = collision_type  # for collisions

        self.pivot = pm.PivotJoint(self.control_body, self.body, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction
        self.pivot.max_force = 1000  # Emulate linear friction

        space.add(self.control_body, self.body, self.shape, self.pivot)


class ActorRigidBody(KinematicRigidBody):
    def __init__(self, pos, size, collision_type, space):
        KinematicRigidBody.__init__(self, pos, size, collision_type, space)

    def change_direction(self, arbiter, space, data):
        """Change self directions and velocity to opposite ones

        Function what called by pymunk collision handler.
        Basically it's a static method but placed here for code
        grouping (actors collisions are built-in actors class).
        """
        assert data["actor"] is self, "Collision error. Collision data and self aren't match!"

        data["actor"].directionx = -data["actor"].directionx
        data["actor"].directiony = -data["actor"].directiony
        data["actor"].control_body.velocity = -data["actor"].control_body.velocity
        return True
