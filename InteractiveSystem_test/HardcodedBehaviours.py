import InteractiveCmd
from InteractiveCmd import command_object

class HardcodedBehaviours(InteractiveCmd.InteractiveCmd):

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
                    sample, is_new_update = self.get_input_states(0, ('analog_0_state', ))
                    analog_0_samples.append(sample['analog_0_state'])
                    if is_new_update:

                        if analog_0_samples[teensy_id] > 850:
                            indicator_led_on[teensy_id] = 1
                        else:
                            indicator_led_on[teensy_id] = 0

                    # new blink period
                    led_period[teensy_id] += 0.002
                    led_period[teensy_id] %= 10


            print(analog_0_samples)