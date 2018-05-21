

class Graph:
    def __init__(self, obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg, obs_slowdown_fac,
                  obs_visibility, obs_geometric_type,
                  target_x, target_y, target_z, target_z_size, target_radius, ball_x, ball_y, ball_z,
                  ball_radius, nr_of_targets, nr_of_obstacles):
        self.obs_x = obs_x
        self.obs_y = obs_y
        self.obs_z = obs_z
        self.obs_x_size = obs_x_size
        self.obs_y_size = obs_y_size
        self.obs_z_size = obs_z_size
        self.obs_z_angle_deg = obs_z_angle_deg
        self.obs_slowdown_fac = obs_slowdown_fac
        self.obs_visibility = obs_visibility
        self.obs_geometric_type = obs_geometric_type
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z
        self.target_z_size = target_z_size
        self.target_radius = target_radius
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_z = ball_z
        self.ball_radius = ball_radius
        self.nr_of_targets = nr_of_targets
        self.nr_of_obstacles = nr_of_obstacles

        def get_objects(obj_x, obj_y, obj_z, amount):

            objects = []
            i = 0

            while i < amount:
                x_val = obj_x[i]
                y_val = obj_y[i]
                z_val = obj_z[i]

                obj = []
                obj.append(x_val)
                obj.append(y_val)
                obj.append(z_val)
                objects.append(obj)
                print(obj)
                print(objects)
                i = i + 1

            return objects

        self.obstacles = get_objects(obs_x, obs_y, obs_z, nr_of_obstacles)
        self.targets = get_objects(target_x, target_y, target_z, nr_of_targets)

    def pause(self):
        return None


