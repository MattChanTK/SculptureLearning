import numpy as np
import RLtoolkit.tiles as tiles


import SimSystem
import CuriousLearner

# ===== Settings ======
fea_num = 1
fea_name = ["state"]
cmd_num = 1
cmd_name = ["action"]

# ==== Global variables =====
fea_val = np.zeros(fea_num)
cmd_val = np.zeros(cmd_num)


# ==== Algorithm ======

# ---- initialize ----
sim_sys = SimSystem.SimSystem()
q_learner = CuriousLearner.CuriousLearner(fea_num, cmd_num)
cmd_val = np.ones_like(cmd_val)  # initial commands

# ---- read features ----
input_val = sim_sys.simulate(cmd_val)

float_array = [50, 50]
num_tiling = 512

memory_size = 512
tiles_array = tiles.tiles(num_tiling, memory_size, float_array)
sum = 0
weight = dict()
target = 100
alpha = 0.2/num_tiling

for j in range(50):
    result = 0

    for i in range(num_tiling):
        if tiles_array[i] in weight:
            result += weight[tiles_array[i]]

    for i in range(num_tiling):
        if tiles_array[i] in weight:
            weight[(tiles_array[i])] += alpha*(target-result)
        else:
            weight[(tiles_array[i])] = alpha*(target-result)
    print tiles_array
    print result
result = 0

tiles_array = tiles.tiles(num_tiling, memory_size, [50, 56])
for i in range(num_tiling):
    if tiles_array[i] in weight:
        result += weight[tiles_array[i]]
print tiles_array
print result
print weight

# LOOP START
while False:

    pass

    # ---- select action ----


    # ---- predict features ----

    # ---- generate actuator output commands ----

    # ---- write actuator outputs -----

    # ---- read sensor inputs ----

    # ---- extract features ----

    # ---- calculate prediction error ----

    # ---- add to training set -----

    # ---- calculate learning progress -----

    # ---- update learner ----

# LOOP END
