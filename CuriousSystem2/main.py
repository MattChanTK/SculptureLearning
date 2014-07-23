import numpy as np
import RLtoolkit.tiles as tiles
import copy
import pylab as pl

import SimSystem
import CuriousLearner2
import Expert
import Expert2
import save_figure
import Partition


# ===== Settings ======
fea_dim = 1
fea_name = ["state"]
fea_num = 10  # 0 to 9
cmd_dim = 1
cmd_name = ["action"]
cmd_num = 3  # 0 to 9

loop_num = 3000

# ==== Global variables =====
fea_val = np.zeros(fea_dim)
cmd_val = np.zeros(cmd_dim)

# ==== storage ====
prediction_error_history = []
state0_history = []
action0_history = []
state1_history = []
optimal_state_action_history = []
q_history = []

# ==== Algorithm ======

# ---- initialize ----
sim_sys = SimSystem.SimSystem()
q_learner = CuriousLearner2.CuriousLearner2(fea_dim, cmd_dim, fea_num, cmd_num)
cmd_val = np.ones_like(cmd_val)*7  # initial commands
#partition = Partition.Partition(fea_num, cmd_num)
expert = Expert2.Expert2()

# ---- initial simulation ----
sim_sys.write_command(cmd_val)
sim_sys.simulate()
input_val = sim_sys.read_feature()
t = 0

# LOOP START
while t < loop_num:

    # ---- select action ----
    q_history.append(copy.copy(q_learner.get_q_column(input_val[0])))
    output_val = q_learner.select_action(input_val)
    optimal_state_action = q_learner.get_state_action_with_highest_q()


    # ---- predict features ----
    #expert = partition.get_expert(input_val[0], output_val[0])
    input_prediction = expert.predict(input_val, output_val)

    # ---- generate actuator output commands ----
    sim_sys.write_command(output_val)

    # ---- simulate one time step -----
    input_val_0 = copy.copy(input_val)  # remember previous input_val
    output_val_0 = copy.copy(output_val)  # remember previous output_val
    state0_history.append(input_val_0[0])
    action0_history.append(output_val_0[0])
    optimal_state_action_history.append(tuple(optimal_state_action))
    sim_sys.simulate()

    # ---- read features ----
    input_val = sim_sys.read_feature()

    # ---- calculate prediction error ----
    if input_prediction[0] == -1:
        prediction_error_history.append(0)
    else:
        prediction_error = np.array(input_prediction) - input_val
        prediction_error_history.append(prediction_error)
    state1_history.append(input_val[0])

    # ---- add to training set -----
    expert.add_to_training_set(input_val_0, output_val_0, input_val)

    # ---- calculate learning progress -----

    if input_prediction[0] is not -1 and len(prediction_error_history) > 1:
        reward = prediction_error_history[-2]**2 - prediction_error_history[-1]**2
    else:
        reward = 0

    # ---- update learner ----
    q_learner.update_q_table(input_val_0, output_val_0, input_val, reward)

    # ---- print to terminal ----
    print("State0: " + str(input_val_0))
    print("Optimal state action: " + str(optimal_state_action))
    print("Action: " + str(output_val_0))
    print("State1: " + str(input_val))
    print("Input Prediction: " + str(input_prediction))
    try:
        print("Prediction Error: " + str(prediction_error))
    except:
         print("Prediction Error: N/A")
    print("Number of Partitions: " + str(expert.cluster_num))
    print("Reward: " + str(reward) + "\n")

    t += 1
    print("t = " + str(t))
# LOOP END


# ==== Visualization ====
folder_name = 'outputs/random(0.1) gamma(0.5) learn(0.1) VelocityControl 3-Action 3'
for i in range(expert.cluster_num):
    expert.plot_model(partition=i, show_plot=False, save_fig_folder=folder_name) #(i==expert.cluster_num-1))

pl.figure(expert.cluster_num+1)
pl.plot(prediction_error_history)
pl.title("Prediction Error History")
pl.xlabel("time")
pl.ylabel("Prediction Error")
save_figure.save(folder_name+"/Prediction Error History")

pl.figure(expert.cluster_num+2)
pl.hist(state1_history)
pl.title("Resultant State Histogram")
pl.xlabel("State")
pl.ylabel("# of Occurrence")
pl.autoscale(True)
save_figure.save(folder_name+"/Resultant State Histogram")

pl.figure(expert.cluster_num+3)
pl.hist2d(state0_history, action0_history)
pl.title("Initial State vs Initial Action Histogram")
pl.xlabel("State")
pl.ylabel("Action")
pl.colorbar()
save_figure.save(folder_name+"/Initial State vs Initial Action Histogram")

#print("Most common Action")
def most_common(lst):
    return max(set(lst), key=lst.count)
bin_num = 100
bin_size = int(len(action0_history)/bin_num)
most_common_action = []
for i in range(bin_num):
    start = i*bin_size
    end = start + bin_size
    state = most_common(action0_history[start:end])
    most_common_action.append(state)
    #print("t = " + str(start) + ":" + str(end) + "\t\t"),
    #print(state)
pl.figure(expert.cluster_num+4)
pl.plot(most_common_action,'ro-')
pl.title("Most Common Resultant Action History")
pl.xlabel("Time")
pl.ylabel("Action")
save_figure.save(folder_name+"/Most Common Resultant Action History")

def percent_occur(lst, key, window=30):
    percent_key = np.zeros(len(lst)-window)

    for i in range(window, len(lst)):
        key_occur_count = lst[i-window:i].count(key)
        percent_key[i-window] = float(key_occur_count)/float(window)
    return percent_key

for i in range(cmd_num):
    percent_key = percent_occur(action0_history, i, window=30)
    pl.figure(expert.cluster_num+5)
    pl.plot(percent_key, label=('Action '+str(i)))
pl.title("Percent Occurrence for Resultant Action History")
pl.xlabel("Time")
pl.ylabel("Percent Action")
pl.legend()
save_figure.save(folder_name+"/Percent Occurrence for Resultant Action History")

pl.figure(expert.cluster_num+6)
matrix = np.flipud(np.transpose(np.matrix(q_learner.q_table)))
pl.imshow(matrix, interpolation='nearest', cmap=pl.cm.gray,
            extent=(-0.5,np.shape(matrix)[1]-0.5,-0.5,np.shape(matrix)[0]-0.5))
pl.colorbar()
pl.title("Q-Table")
pl.xlabel("Initial State")
pl.ylabel("Initial Action")
save_figure.save(folder_name+"/Q-Table")


pl.figure(expert.cluster_num+7)
matrix = np.flipud(np.transpose(np.matrix(q_history)))
pl.imshow(matrix, interpolation='none', aspect='auto', cmap=pl.cm.gray,
            extent=(-0.5,np.shape(matrix)[1]-0.5, -0.5,np.shape(matrix)[0] - 0.5))
pl.plot(action0_history, 'r.', label="Actual")
pl.colorbar()
pl.title("Q-Table History")
pl.xlabel("Time")
pl.ylabel("Action")

save_figure.save(folder_name+"/Q-Table History")


optimal_state_action_history = np.array(optimal_state_action_history)

pl.figure(expert.cluster_num+8)
pl.plot(optimal_state_action_history[:,0], 'b-', label="Optimal")
pl.plot(state1_history, 'r.', label="Actual")
pl.title("Optimal State and Actual State")
pl.xlabel("time")
pl.ylabel("State")
pl.ylim([-1, 11])
pl.legend()
save_figure.save(folder_name+"/Optimal State and Actual State")

pl.figure(expert.cluster_num+9)
pl.plot(optimal_state_action_history[:,1], 'b-', label="Optimal")
pl.plot(action0_history, 'r.', label="Actual")
pl.title("Optimal Action and Actual Action")
pl.xlabel("time")
pl.ylabel("Action")
pl.ylim([-1, 11])
pl.legend()
save_figure.save(folder_name+"/Optimal Action and Actual Action")


pl.show()
