#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fftfas 2 Cards
# Generated: Wed Apr 11 13:50:58 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import epy_block_0
import epy_block_0_0
import epy_block_0_0_1
import sip
import sys
import time
from gnuradio import qtgui


class fftfas_2_cards(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fftfas 2 Cards")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fftfas 2 Cards")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fftfas_2_cards")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 4e6
        self.rel_freq = rel_freq = 1e6
        self.fft_width = fft_width = 1024
        self.skip = skip = (fft_width/2+ 1  + int(round(rel_freq*fft_width/samp_rate)))
        self.center_freq = center_freq = 1e9

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('serial=30DBB29', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('serial=30DBB0D', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(1, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.qtgui_number_sink_1_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_1_1_0.set_update_time(0.10)
        self.qtgui_number_sink_1_1_0.set_title('Mottagen fas')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_1_1_0.set_min(i, -1)
            self.qtgui_number_sink_1_1_0.set_max(i, 1)
            self.qtgui_number_sink_1_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_1_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_1_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_1_1_0.enable_autoscale(True)
        self._qtgui_number_sink_1_1_0_win = sip.wrapinstance(self.qtgui_number_sink_1_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_1_0_win)
        self.qtgui_number_sink_1_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_1_1.set_update_time(0.10)
        self.qtgui_number_sink_1_1.set_title('Mottagen amplitud')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_1_1.set_min(i, -1)
            self.qtgui_number_sink_1_1.set_max(i, 1)
            self.qtgui_number_sink_1_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1_1.set_label(i, labels[i])
            self.qtgui_number_sink_1_1.set_unit(i, units[i])
            self.qtgui_number_sink_1_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1_1.enable_autoscale(True)
        self._qtgui_number_sink_1_1_win = sip.wrapinstance(self.qtgui_number_sink_1_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_1_win)
        self.qtgui_number_sink_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_1_0.set_update_time(0.10)
        self.qtgui_number_sink_1_0.set_title('Skickad fas')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_1_0.set_min(i, -1)
            self.qtgui_number_sink_1_0.set_max(i, 1)
            self.qtgui_number_sink_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_1_0.enable_autoscale(True)
        self._qtgui_number_sink_1_0_win = sip.wrapinstance(self.qtgui_number_sink_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_0_win)
        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_1.set_update_time(0.10)
        self.qtgui_number_sink_1.set_title('Skickad amplitud')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_1.set_min(i, -1)
            self.qtgui_number_sink_1.set_max(i, 1)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(True)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('Fasskillnad mellan skickad och mottagen signal')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -3.141)
            self.qtgui_number_sink_0.set_max(i, 3.141)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_width, True, (window.blackmanharris(1024)), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_width, True, (window.blackmanharris(1024)), True, 1)
        self.epy_block_0_0_1 = epy_block_0_0_1.blk(v_len=1024, samp_rate=samp_rate, freq=rel_freq)
        self.epy_block_0_0 = epy_block_0_0.blk(v_len=1024, samp_rate=samp_rate, freq=rel_freq)
        self.epy_block_0 = epy_block_0.blk(example_param=1.0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, rel_freq, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.epy_block_0_0, 1), (self.blocks_sub_xx_0, 1))
        self.connect((self.epy_block_0_0, 0), (self.qtgui_number_sink_1_1, 0))
        self.connect((self.epy_block_0_0, 1), (self.qtgui_number_sink_1_1_0, 0))
        self.connect((self.epy_block_0_0_1, 1), (self.blocks_sub_xx_0, 0))
        self.connect((self.epy_block_0_0_1, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.epy_block_0_0_1, 1), (self.qtgui_number_sink_1_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.epy_block_0_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fftfas_2_cards")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.set_skip((self.fft_width/2+ 1  + int(round(self.rel_freq*self.fft_width/self.samp_rate))))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.epy_block_0_0_1.samp_rate = self.samp_rate
        self.epy_block_0_0.samp_rate = self.samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_rel_freq(self):
        return self.rel_freq

    def set_rel_freq(self, rel_freq):
        self.rel_freq = rel_freq
        self.set_skip((self.fft_width/2+ 1  + int(round(self.rel_freq*self.fft_width/self.samp_rate))))
        self.epy_block_0_0_1.freq = self.rel_freq
        self.epy_block_0_0.freq = self.rel_freq
        self.analog_sig_source_x_0.set_frequency(self.rel_freq)

    def get_fft_width(self):
        return self.fft_width

    def set_fft_width(self, fft_width):
        self.fft_width = fft_width
        self.set_skip((self.fft_width/2+ 1  + int(round(self.rel_freq*self.fft_width/self.samp_rate))))

    def get_skip(self):
        return self.skip

    def set_skip(self, skip):
        self.skip = skip

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)


def main(top_block_cls=fftfas_2_cards, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
