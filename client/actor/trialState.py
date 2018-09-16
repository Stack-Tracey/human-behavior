from client.actor import nodes

class TrialState:
    def __init__(self, obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg, obs_slowdown_fac,
                  obs_visibility, obs_geometric_type, tar_x, tar_y, tar_z, tar_z_size, tar_radius, ball_x, ball_y,
                  ball_z, ball_radius, nr_of_targets, nr_of_obstacles):

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
        self.nr_of_obstacles = nr_of_obstacles

        self.tar_x = tar_x
        self.tar_y = tar_y
        self.tar_z = tar_z
        self.tar_z_size = tar_z_size
        self.tar_radius = tar_radius
        self.targets_tup = []
        self.nr_of_targets = nr_of_targets

        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_z = ball_z
        self.ball_radius = ball_radius
        self.ball = (ball_x, ball_y)# ball_z, ball_radius

        #TODO handling of different behavior: adding param for 'perfectness' and include by seeing all obstacles
        #returns the positions of obstacles.
        #visible_fac_val = {1. visible for player one, 2. visible for player two, 3. visible for both}
        def get_obstacles(obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg, obs_slowdown_fac, visibility, geometric_type):
            obstacles = []
            i = 0

            while i < nr_of_obstacles:
                x_val = obs_x[i]
                y_val = obs_y[i]
                z_val = obs_z[i]
                x_size_val = obs_x_size[i]
                y_size_val = obs_y_size[i]
                z_size_val = obs_z_size[i]
                angle_deg_val = obs_z_angle_deg[i]
                slowdown_fac_val = obs_slowdown_fac[i]
                visible_fac = visibility[i]
                geometric_type_val = geometric_type[i]

                if visible_fac_val == 1 or visible_fac_val == 3:
                    obs = [x_val, y_val, z_val, x_size_val, y_size_val, z_size_val, angle_deg_val, slowdown_fac_val, visible_fac, geometric_type_val]
                    obstacles.append(obs)

                i = i + 1
            print("obstacles, should be less than 9 elements: ", obstacles)
            return obstacles

        #returns the positions of targets.
        def get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets):
            targets = []
            tar_buffer = []
            i = 0

            while i < nr_of_targets:
                x_val = tar_x[i]
                y_val = tar_y[i]
                z_val = tar_z[i]
                z_size_val = tar_z_size[i]
                radius_val = tar_radius
                nr_of_tar_val = nr_of_targets

                tar = [x_val, y_val, z_val, z_size_val, radius_val, nr_of_tar_val]
                tar_tup = (x_val, y_val)
                targets.append(tar)
                tar_buffer.append(tar_tup)

                i = i + 1

            self.targets_tup = sorted(tar_buffer)
            return targets

        self.obstacles = get_obstacles(self.obs_x, self.obs_y, self.obs_z, self.obs_x_size, self.obs_y_size,
                                       self.obs_z_size, self.obs_z_angle_deg, self.obs_slowdown_fac,
                                       self.obs_visibility, self.obs_geometric_type)
        self.targets = get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets)
        self.nodes = nodes.Nodes(self.obstacles, self.targets, self.ball)
        self.tar_nodes = self.nodes.tar_nodes
        self.field_filled = self.nodes.field_filled







