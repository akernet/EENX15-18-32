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
    """Make sure the phase is between -pi and pi"""
    
    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
                               self,
                               name='Phase between -pi and pi',   # will show up in GRC
                               in_sig=[np.float32],
                               out_sig=[np.float32]
                               )
                               # if an attribute with the same name as a parameter is found,
                               # a callback is registered (properties work, too).
        self.example_param = example_param
    
    def work(self, input_items, output_items):
        """Make sure the phase is between -pi and pi"""
        output_items[0][:] = (scipy.pi + input_items[0]) % (2 * scipy.pi) - scipy.pi #* self.example_param
        return len(output_items[0])

