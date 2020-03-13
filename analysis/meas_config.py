class Measurement_Configuration:

    def __init__(self, sample_name, ref_gain, sample_gain, pulse_dur, laser_volt, beam, temp):
        self.sample_name = sample_name # sample name
        self.ref_gain = ref_gain # reference gain setting on the pre-amplifier
        self.sample_gain = sample_gain # sample gain setting
        self.pulse_dur = pulse_dur # laser pulse duration
        self.laser_volt = laser_volt # laser peak voltage
        self.beam = beam # beam setting, e.g. BB for broad beam and NB for narrow beam
        self.temp = temp # temperature set during the measurement
