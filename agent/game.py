
class Game:
    def __init__(self, frame):
        self.frame = frame


    def response(self, frame):
        return None


    def stop(self, frame):
        return None
        #exec.stop


    def experiment_def(self, frame):
        nr_of_trials = frame["Nr_of_Trials"]
        return nr_of_trials


    def trial_def(self, frame):
        level_data = frame['Level Data']
        print(level_data)
        target_data = level_data['Targets']
        print(target_data)
        ball_data = level_data['Ball']
        print(ball_data)
        obstacle_data = level_data['Obstacles']
        print("this works")
        ai_type = level_data['AI Type']
        show_bar = level_data['ShowBar']
        nr_of_frames_to_skip_at_start = level_data['Nr_of_Frames_to_Skip_at_Start_of_Trial']
        blink_wave_length_owg = level_data['Blink_Wavelength_OWG']
        blink_wave_length_screen = level_data['Blink_Wavelength_Screen']
        nr_of_targets = level_data['Nr of Targets']
        nr_of_obstacles = level_data['Nr of Obstacles']
        trial_duration_time = level_data['Trial Duration [ms]']

        aI_length_of_memory = level_data['AI 1 Length of Memory']
        screen_flicker_target_radius = level_data['Screen_Flicker_Target_Radius']
        questionaire_text = level_data['Questionair Text']
        show_fixiation_cross = level_data['Screen_Flicker_Target_Radius']
        trial_type = level_data['Trial Type']

        target_z = target_data['Z']
        target_y = target_data['Y']
        target_radius = target_data['Radius']
        target_x = target_data['X']
        target_z_size = target_data['Z_size']

        obs_x_size = obstacle_data['X_size']
        obs_y_size = obstacle_data['Y_size']
        obs_slowdown_fac = obstacle_data['slowdown factor']
        obs_visibility = obstacle_data['visibility']
        obs_z = obstacle_data['Z']
        obs_y = obstacle_data['Y']
        obs_z_size = obstacle_data['Z_size']
        obs_geometric_type = obstacle_data['geometric type']
        obs_z_angle_deg = obstacle_data['Z_angle_deg']

        ball_z = ball_data['Z']
        ball_y = ball_data['Y']
        ball_radius = ball_data['Radius']
        ball_x = ball_data['X']

        return None


    def play(self, frame):
        frame_data = frame["Frame Data"]
        trigger_state = frame_data['Trigger State']
        start_last_frame = frame_data['Last Frame Start [ms]']
        p1_norm_avg_x = frame_data["Player 1"]['norm_avg_x']
        p1_norm_avg_reshaped_y = frame_data["Player 1"]['norm avg_reshaped y']
        p1_x = frame_data["Player 1"]['X']
        p1_f_x = frame_data["Player 1"]['F_y']
        p1_y = frame_data["Player 1"]['Y']
        trial_start = frame_data['Trial Start [ms]']
        trial_elapsed = frame_data['Trial Elapsed [ms]']
        ode_processed_until = frame_data['ODE processed until [ms]']
        dt = frame_data['dt [ms]']
        p2_norm_avg_x = frame_data["Player 2"]['norm_avg_x']
        p2_norm_avg_reshaped_y = frame_data["Player 2"]['norm avg_reshaped y']
        p2_x = frame_data["Player 2"]['X']
        p2_f_x = frame_data["Player 2"]['F_y']
        p2_y = frame_data["Player 2"]['Y']
        #field.move(p1_f_x, p1_x, p1_y)

        return ode_processed_until


    def start(self, frame):
        return None



