import os
# PyvJoy only works on Windows
if os.name == "nt":
    import pyvjoy

from controller_mappings import XBOX_TO_PYVJOY


class XboxController:
    def __init__(self, data_key_labels, button_threshold=0.5):
        self.controller = pyvjoy.VJoyDevice(1)
        self.data_key_labels = data_key_labels
        self.button_threshold = button_threshold

    def scale_axis(self, value):
        max_vjoy = 32767.0
        # [-1, 1] to [0, 32767]
        return int(((float(value) + 1.0) / 2.0) * max_vjoy)

    def threshold_button(self, value):
        if value >= self.button_threshold:
            return 1
        return 0

    def emit_keys(self, output_values):
        for idx, value in enumerate(output_values):
            key_label = self.data_key_labels[idx]
            if key_label in XBOX_TO_PYVJOY["AXES"].keys():
                scaled = self.scale_axis(value)
                self.controller.set_axis(
                    XBOX_TO_PYVJOY["AXES"][key_label], scaled)
            elif key_label in XBOX_TO_PYVJOY["BUTTONS"].keys():
                thresholded = self.threshold_button(value)
                self.controller.set_button(
                    XBOX_TO_PYVJOY["BUTTONS"][key_label], thresholded)
            else:
                raise Exception(f"{key_label = } is not in controller mappings")

    def reset_controller(self):
        a = XBOX_TO_PYVJOY["AXES"]
        self.controller.set_axis(a["RS_X"], 16384)
        self.controller.set_axis(a["RS_Y"], 16384)
        self.controller.set_axis(a["LS_X"], 16384)
        self.controller.set_axis(a["LS_Y"], 16384)
        self.controller.set_axis(a["LT"], 0)
        self.controller.set_axis(a["RT"], 0)
