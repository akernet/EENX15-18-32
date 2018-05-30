"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import scipy


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Takes a vector of data that has been Fourier transformed and calculates the amplitude and phase of the specified frequency"""

    def __init__(self, v_len=1024, samp_rate=32000, freq=2000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Single frequency amplitude/phase.',   # will show up in GRC
            in_sig=[(np.complex64, v_len)],
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.v_len = (v_len)
        self.samp_rate = int(samp_rate)
        self.freq = int(freq)

    def work(self, input_items, output_items):
        """Takes a vector of data that has been Fourier transformed and calculates the amplitude and phase of the specified frequency"""
        def getBin(v_len, samp_rate, freq):
            return int(np.round(
                (float(v_len)/2)+(float(v_len)/2)*(float(freq)/(float(samp_rate)/2))
            ))


        freq_bin = getBin(self.v_len, self.samp_rate, self.freq)
        
        for index, work_item in enumerate(input_items[0]):
            amp = np.absolute(work_item[freq_bin])
            phase = np.angle(work_item[freq_bin])
            output_items[0][index] = amp
            output_items[1][index] = phase
        return len(output_items[0])
