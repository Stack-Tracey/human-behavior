import graph

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
        self.tar_x = tar_x
        self.tar_y = tar_y
        self.tar_z = tar_z
        self.tar_z_size = tar_z_size
        self.tar_radius = tar_radius
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_z = ball_z
        self.ball_radius = ball_radius
        self.nr_of_targets = nr_of_targets
        self.nr_of_obstacles = nr_of_obstacles

        #returns the positions of obstacles. Each Element in output-list has the same order as method call
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
                angle_deg_val = obs_z_angle_deg
                slowdown_fac_val = obs_slowdown_fac[i]
                visible_fac = visibility
                geometric_type_val = geometric_type
                print("here comes single vaalues", x_val, y_val, z_val, x_size_val, y_size_val, z_size_val, angle_deg_val, slowdown_fac_val,visible_fac, geometric_type_val)

                obs = [x_val, y_val, z_val, x_size_val, y_size_val, z_size_val, angle_deg_val, slowdown_fac_val, visible_fac, geometric_type_val]
                obstacles.append(obs)

                i = i + 1
                print("here comes obstacles", obstacles)
            return obstacles

        #returns the positions of targets. Each Element in output-list has the same order as method call
        def get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets):
            targets = []
            i = 0

            while i < nr_of_targets:

                x_val = tar_x[i]
                y_val = tar_y[i]
                z_val = tar_z[i]
                z_size_val = tar_z_size[i]
                radius_val = tar_radius
                nr_of_tar_val = nr_of_targets

                tar = [x_val, y_val, z_val, z_size_val, radius_val, nr_of_tar_val]
                targets.append(tar)

                print(tar)
                print(targets)

                i = i + 1

            return targets

        #returns the start position of the ball and it's radius
        def get_start_ball(ball_x, ball_y, ball_z, ball_radius):
            ball_pos = [ball_x, ball_y, ball_z, ball_radius]

            return ball_pos

        self.obs_x = obs_x
        self.obs_y = obs_y
        self.obs_z = obs_z
        self.obs_x_size = obs_x_size
        self.obs_y_size = obs_y_size
        self.obs_z_size = obs_z_size
        self.obs_z_angle_deg = obs_z_angle_deg
        self.obs_slowdown_fac = obs_slowdown_fac
        self.obs_visibility = obs_visibility
        self.obstacles = get_obstacles(self.obs_x, self.obs_y, self.obs_z, self.obs_x_size, self.obs_y_size,
                                       self.obs_z_size, self.obs_z_angle_deg, self.obs_slowdown_fac,
                                       self.obs_visibility, self.obs_geometric_type)
        self.targets = get_targets(tar_x, tar_y, tar_z, tar_z_size, tar_radius, nr_of_targets)
        self.ball = get_start_ball(ball_x, ball_y, ball_z, ball_radius)
        print("overhanded obstacles", self.obstacles)
        self.graph = graph.Graph(self.obstacles, self.targets, self.ball)

    def pause(self, val):
        print(val)




