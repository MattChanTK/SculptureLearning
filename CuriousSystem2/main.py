import numpy as np
import RLtoolkit.tiles as tiles


import SimSystem
import CuriousLearner2

# ===== Settings ======
fea_dim = 1
fea_name = ["state"]
fea_num = 10  # 0 to 9
cmd_dim = 1
cmd_name = ["action"]
cmd_num = 10  # 0 to 9

# ==== Global variables =====
fea_val = np.zeros(fea_dim)
cmd_val = np.zeros(cmd_dim)


# ==== Algorithm ======

# ---- initialize ----
sim_sys = SimSystem.SimSystem()
q_learner = CuriousLearner2.CuriousLearner2(fea_dim, cmd_dim, fea_num, cmd_num)
cmd_val = np.ones_like(cmd_val)  # initial commands

# ---- read features ----
input_val = sim_sys.simulate(cmd_val)

# LOOP START
while False:

    # ---- select action ----
    output_val = q_learner.select_action(input_val)

    # ---- predict features ----


    # ---- generate actuator output commands ----
    sim_sys.write_command(output_val)

    # ---- simulate one time step -----
    sim_sys.simulate()

    # ---- read features ----


    # ---- calculate prediction error ----

    # ---- add to training set -----

    # ---- calculate learning progress -----

    # ---- update learner ----

# LOOP END
