import InteractiveCmd
from InteractiveCmd import command_object

from copy import copy

class HardcodedBehaviours(InteractiveCmd.InteractiveCmd):

    def run(self):

        teensy_ids = range(len(self.Teensy_thread_list))
        led_period = [0]*len(self.Teensy_thread_list)
        indicator_led_on = [0]*len(self.Teensy_thread_list)
        high_power_led_level = [0]*len(self.Teensy_thread_list)
        pwm_level = [0]*len(self.Teensy_thread_list)

        while True:
        #for i in range(5):

            analog_0_samples = []
            if len(self.Teensy_thread_list) == 0:
                return

            for teensy_id in teensy_ids:

                # check if the thread is still alive
                if not self.Teensy_thread_list[teensy_id].is_alive():

                    self.Teensy_thread_list.pop(teensy_id)
                    led_period.pop(teensy_id)
                    indicator_led_on.pop(teensy_id)
                    teensy_ids = range(len(self.Teensy_thread_list))

                else:
                    cmd_obj = command_object(teensy_id)

                    cmd_obj.add_param_change('indicator_led_on',  int(indicator_led_on[teensy_id]))
                    cmd_obj.add_param_change('indicator_led_period', int(led_period[teensy_id])*25)
                    cmd_obj.add_param_change('high_power_led_level', int(high_power_led_level[teensy_id]))
                    cmd_obj.add_param_change('sma_0_level', int(pwm_level[teensy_id]))
                    cmd_obj.add_param_change('sma_1_level', int((pwm_level[teensy_id])+50)%255)
                    cmd_obj.add_param_change('reflex_0_level', int((pwm_level[teensy_id])+100)%255)
                    cmd_obj.add_param_change('reflex_1_level', int((pwm_level[teensy_id])+150)%255)
                    self.enter_command(cmd_obj)

            self.send_commands()

            for teensy_id in teensy_ids:
                 # check if the thread is still alive
                if not self.Teensy_thread_list[teensy_id].is_alive():

                    self.Teensy_thread_list.pop(teensy_id)
                    led_period.pop(teensy_id)
                    indicator_led_on.pop(teensy_id)
                    teensy_ids = range(len(self.Teensy_thread_list))

                else:
                    sample, is_new_update = self.get_input_states(teensy_id, ('all', ))

                    if is_new_update:

                        if sample['analog_0_state'] > 850:
                            indicator_led_on[(teensy_id+1)%len(self.Teensy_thread_list)] = 1
                        else:
                            indicator_led_on[(teensy_id+1)%len(self.Teensy_thread_list)] = 1

                    # new blink period
                    led_period[teensy_id] += 0.002
                    led_period[teensy_id] %= 10
                    high_power_led_level[teensy_id] += 0.2
                    high_power_led_level[teensy_id] %= 100
                    pwm_level[teensy_id] += 0.1
                    pwm_level[teensy_id] %= 255
                    print(teensy_id, ": ", sample)

class HardcodedBehaviours_test(InteractiveCmd.InteractiveCmd):

    def run(self):

        teensy_ids = range(len(self.Teensy_thread_list))
        led_period = [0]*len(self.Teensy_thread_list)
        indicator_led_on = [0]*len(self.Teensy_thread_list)

        while True:
        #for i in range(5):

            analog_0_samples = []
            if len(self.Teensy_thread_list) == 0:
                return

            for teensy_id in teensy_ids:

                # check if the thread is still alive
                if not self.Teensy_thread_list[teensy_id].is_alive():

                    self.Teensy_thread_list.pop(teensy_id)
                    led_period.pop(teensy_id)
                    indicator_led_on.pop(teensy_id)
                    teensy_ids = range(len(self.Teensy_thread_list))

                else:
                    cmd_obj = command_object(teensy_id)

                    cmd_obj.add_param_change('indicator_led_on',  int(indicator_led_on[teensy_id]))
                    cmd_obj.add_param_change('indicator_led_period', int(led_period[teensy_id])*25)
                    self.enter_command(cmd_obj)

            self.send_commands()

            for teensy_id in teensy_ids:
                 # check if the thread is still alive
                if not self.Teensy_thread_list[teensy_id].is_alive():

                    self.Teensy_thread_list.pop(teensy_id)
                    led_period.pop(teensy_id)
                    indicator_led_on.pop(teensy_id)
                    teensy_ids = range(len(self.Teensy_thread_list))

                else:
                    sample, is_new_update = self.get_input_states(teensy_id, ('analog_0_state', ))
                    analog_0_samples.append(copy(sample['analog_0_state']))
                    if is_new_update:

                        if analog_0_samples[teensy_id] > 850:
                            indicator_led_on[(teensy_id+1)%len(self.Teensy_thread_list)] = 1
                        else:
                            indicator_led_on[(teensy_id+1)%len(self.Teensy_thread_list)] = 0

                    # new blink period
                    led_period[teensy_id] += 0.002
                    led_period[teensy_id] %= 10


            print("Analog 0 State: ", analog_0_samples)
