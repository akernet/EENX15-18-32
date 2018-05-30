#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Send And Receive Amplitude And Phase
# Generated: Wed Apr 11 16:21:36 2018
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
import sip
import sys
import time
from gnuradio import qtgui


class send_and_receive_amplitude_and_phase(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Send And Receive Amplitude And Phase")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Send And Receive Amplitude And Phase")
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

        self.settings = Qt.QSettings("GNU Radio", "send_and_receive_amplitude_and_phase")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6
        self.fft_width = fft_width = 1024
        self.f4 = f4 = 3.5e6
        self.f3 = f3 = 2.5e6
        self.f2 = f2 = 1.5e6
        self.f1 = f1 = 0.5e6
        self.fft_offset_4 = fft_offset_4 = int(round(f4*fft_width/samp_rate) + fft_width/2 +1)
        self.fft_offset_3 = fft_offset_3 = int(round(f3*fft_width/samp_rate) + fft_width/2 +1)
        self.fft_offset_2 = fft_offset_2 = int(round(f2*fft_width/samp_rate) + fft_width/2 +1)
        self.fft_offset_1 = fft_offset_1 = int(round(f1*fft_width/samp_rate) + fft_width/2 +1)
        self.center_freq = center_freq = 1e9

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'Magnitude')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Phase')
        self.top_layout.addWidget(self.tab)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_clock_source('internal', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(30, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.qtgui_number_sink_0_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_0_1.set_update_time(0.1)
        self.qtgui_number_sink_0_0_1.set_title('Magnitude of 4th frequency')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_0_1.set_min(i, -1)
            self.qtgui_number_sink_0_0_1.set_max(i, 1)
            self.qtgui_number_sink_0_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_1.enable_autoscale(False)
        self._qtgui_number_sink_0_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_0_1.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_number_sink_0_0_1_win)
        self.qtgui_number_sink_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_0_0.set_update_time(0.1)
        self.qtgui_number_sink_0_0_0.set_title('Magnitude of 3rd frequency')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_number_sink_0_0_0_win)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_0.set_update_time(0.1)
        self.qtgui_number_sink_0_0.set_title('Magnitude of 2nd frequency')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_number_sink_0_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('Magnitude of 1st requency')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	fft_width, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'Skickad signal', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(True)

        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

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
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	fft_width, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'Mottagen signal', #name
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
        self.fft_vxx_0 = fft.fft_vcc(fft_width, True, (window.blackmanharris(fft_width)), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_skiphead_0_0_1 = blocks.skiphead(gr.sizeof_gr_complex*1, fft_offset_4)
        self.blocks_skiphead_0_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, fft_offset_3)
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, fft_offset_2)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, fft_offset_1)
        self.blocks_keep_one_in_n_0_0_1 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, fft_width)
        self.blocks_file_sink_4 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f4fas.txt', False)
        self.blocks_file_sink_4.set_unbuffered(False)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f3fas.txt', False)
        self.blocks_file_sink_3.set_unbuffered(False)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f2fas.txt', False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_1_0_1 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f4amp.txt', False)
        self.blocks_file_sink_1_0_1.set_unbuffered(False)
        self.blocks_file_sink_1_0_0 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f3amp.txt', False)
        self.blocks_file_sink_1_0_0.set_unbuffered(False)
        self.blocks_file_sink_1_0 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f2amp.txt', False)
        self.blocks_file_sink_1_0.set_unbuffered(False)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f1amp.txt', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, '/Users/arvidbjurklint/Google Drive/Kandidatarbete-Software defined radio/GNUradio-projekt/send and receive amplitude GRC/data/f1fas.txt', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0_0_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_2 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_1 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.blocks_add_xx_0_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_1_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f4, 1, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f3, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f2, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f1, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.blocks_add_xx_0_1, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.blocks_complex_to_arg_1, 0), (self.blocks_file_sink_4, 0))
        self.connect((self.blocks_complex_to_arg_2, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_file_sink_1_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_0, 0), (self.blocks_file_sink_1_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_0, 0), (self.qtgui_number_sink_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_1, 0), (self.blocks_file_sink_1_0_1, 0))
        self.connect((self.blocks_complex_to_mag_0_0_1, 0), (self.qtgui_number_sink_0_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_arg_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_complex_to_arg_2, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_complex_to_mag_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_1, 0), (self.blocks_complex_to_arg_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_1, 0), (self.blocks_complex_to_mag_0_0_1, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_skiphead_0_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_0_1, 0), (self.blocks_keep_one_in_n_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "send_and_receive_amplitude_and_phase")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fft_offset_4(int(round(self.f4*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_3(int(round(self.f3*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_2(int(round(self.f2*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_1(int(round(self.f1*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.analog_sig_source_x_0_1_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_fft_width(self):
        return self.fft_width

    def set_fft_width(self, fft_width):
        self.fft_width = fft_width
        self.set_fft_offset_4(int(round(self.f4*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_3(int(round(self.f3*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_2(int(round(self.f2*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.set_fft_offset_1(int(round(self.f1*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.blocks_keep_one_in_n_0_0_1.set_n(self.fft_width)
        self.blocks_keep_one_in_n_0_0_0.set_n(self.fft_width)
        self.blocks_keep_one_in_n_0_0.set_n(self.fft_width)
        self.blocks_keep_one_in_n_0.set_n(self.fft_width)

    def get_f4(self):
        return self.f4

    def set_f4(self, f4):
        self.f4 = f4
        self.set_fft_offset_4(int(round(self.f4*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.analog_sig_source_x_0_1_0.set_frequency(self.f4)

    def get_f3(self):
        return self.f3

    def set_f3(self, f3):
        self.f3 = f3
        self.set_fft_offset_3(int(round(self.f3*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.analog_sig_source_x_0_1.set_frequency(self.f3)

    def get_f2(self):
        return self.f2

    def set_f2(self, f2):
        self.f2 = f2
        self.set_fft_offset_2(int(round(self.f2*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.analog_sig_source_x_0_0.set_frequency(self.f2)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.set_fft_offset_1(int(round(self.f1*self.fft_width/self.samp_rate) + self.fft_width/2 +1))
        self.analog_sig_source_x_0.set_frequency(self.f1)

    def get_fft_offset_4(self):
        return self.fft_offset_4

    def set_fft_offset_4(self, fft_offset_4):
        self.fft_offset_4 = fft_offset_4

    def get_fft_offset_3(self):
        return self.fft_offset_3

    def set_fft_offset_3(self, fft_offset_3):
        self.fft_offset_3 = fft_offset_3

    def get_fft_offset_2(self):
        return self.fft_offset_2

    def set_fft_offset_2(self, fft_offset_2):
        self.fft_offset_2 = fft_offset_2

    def get_fft_offset_1(self):
        return self.fft_offset_1

    def set_fft_offset_1(self, fft_offset_1):
        self.fft_offset_1 = fft_offset_1

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)


def main(top_block_cls=send_and_receive_amplitude_and_phase, options=None):

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
