import numpy as np
import RLtoolkit.tiles as tiles
import copy

import SimSystem
import CuriousLearner2
import Expert
import Expert2


# ===== Settings ======
fea_dim = 1
fea_name = ["state"]
fea_num = 10  # 0 to 9
cmd_dim = 1
cmd_name = ["action"]
cmd_num = 10  # 0 to 9

loop_num = 1000

# ==== Global variables =====
fea_val = np.zeros(fea_dim)
cmd_val = np.zeros(cmd_dim)

# ==== storage

# ==== Algorithm ======

# ---- initialize ----
sim_sys = SimSystem.SimSystem()
q_learner = CuriousLearner2.CuriousLearner2(fea_dim, cmd_dim, fea_num, cmd_num)
cmd_val = np.ones_like(cmd_val)  # initial commands
expert = Expert2.Expert2()

# ---- initial simulation ----
sim_sys.write_command(cmd_val)
sim_sys.simulate()
input_val = sim_sys.read_feature()
t = 0

# LOOP START
while t < loop_num:

    # ---- select action ----
    output_val = q_learner.select_action(input_val)

    # ---- predict features ----
    input_prediction = expert.predict(input_val, output_val)

    # ---- generate actuator output commands ----
    sim_sys.write_command(output_val)

    # ---- simulate one time step -----
    input_val_0 = copy.copy(input_val)  # remember previous input_val
    output_val_0 = copy.copy(output_val)  # remember previous output_val
    sim_sys.simulate()

    # ---- read features ----
    input_val = sim_sys.read_feature()

    # ---- calculate prediction error ----
    prediction_error = input_val - np.array(input_prediction)

    # ---- add to training set -----
    expert.add_to_training_set(input_val_0, output_val_0, input_val)

    # ---- calculate learning progress -----
    if 5 < sum(input_val) < 7:
        reward = sum(input_val)**2
    else:
        reward = 10

    # ---- update learner ----
    q_learner.update_q_table(input_val_0, output_val_0, input_val, reward)

    # ---- print to terminal ----

    print("State0: " + str(input_val_0))
    print("Action: " + str(output_val_0))
    print("State1: " + str(input_val))
    print("Prediction Error: " + str(prediction_error))
    print("Number of Partitions: " + str(expert.cluster_num))
    print("Reward: " + str(reward) + "\n")


    t += 1
    print("t = " + str(t))
# LOOP END


for i in range(expert.cluster_num):
    expert.plot_model(partition=i, show_plot=(i==expert.cluster_num-1))