//
// Copyright 2014 Ettus Research LLC
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#include <uhd/types/tune_request.hpp>
#include <uhd/utils/thread_priority.hpp>
#include <uhd/utils/safe_main.hpp>
#include <uhd/utils/static.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/exception.hpp>
#include <boost/thread/thread.hpp>
#include <boost/program_options.hpp>
#include <boost/math/special_functions/round.hpp>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp>
#include <algorithm>    // std::fill
#include <vector>       // std::vector
#include <boost/filesystem.hpp>
#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <csignal>

#include "util.hpp"
#include <hidapi.h>

#include <stdio.h>
#include <stdlib.h>

void switch_antenna(uhd::usrp::multi_usrp::sptr usrp_device, float time) {
    std::this_thread::sleep_for(std::chrono::microseconds((long) time*1000000));
    //usrp_device->set_command_time(uhd::time_spec_t(time));
    usrp_device->set_rx_antenna("TX/RX");
    //usrp_device->clear_command_time();
}

int res;
unsigned char buffer[64];
hid_device *handle;
#define MAX_STR 255
wchar_t wstr[MAX_STR];

void init_matrix() {
    handle = hid_open(0x20ce, 0x0022, NULL);

    // Read the Manufacturer String
	res = hid_get_manufacturer_string(handle, wstr, MAX_STR);
	wprintf(L"Manufacturer String: %s\n", wstr);

	// Read the Product String
	res = hid_get_product_string(handle, wstr, MAX_STR);
	wprintf(L"Product String: %s\n", wstr);

	// Read the Serial Number String
	res = hid_get_serial_number_string(handle, wstr, MAX_STR);
	wprintf(L"Serial Number String: (%d) %s\n", wstr[0], wstr);
}

void switch_matrix(int port1, int port2) {

}

void send_from_file(
    uhd::usrp::multi_usrp::sptr usrp_device,
    double start_time,
    const std::string &file
){
    // Samples per buffer.
    int spb = 5000;
    uhd::tx_metadata_t md;

    md.start_of_burst = true;
    md.end_of_burst = false;

    // Start stream at given time, compensate with zero padding duration.
    // spb (samples) / tx_rate (samples/second) = time compensation (seconds).
    md.has_time_spec = true;
    uhd::time_spec_t tspec(start_time - ((double) spb)/((double) usrp_device->get_tx_rate()));
    md.time_spec = tspec;
     
    // Zeropadding buffer. 
    std::vector<std::complex<float> > zeropadding(spb);
    for (int i = 0; i < spb; i++) {
        zeropadding.push_back(std::complex<float>(0.0, 0.0));
    }

    uhd::stream_args_t stream_args("fc32", "sc16");

    std::vector<size_t> channel_nums;
    channel_nums.push_back(0);

    stream_args.channels = channel_nums;
    uhd::tx_streamer::sptr tx_stream = usrp_device->get_tx_stream(stream_args);
    
    int num = 20;
    std::cout << "Sending initial zero padding at time " << (start_time - ((double) spb)/((double) usrp_device->get_tx_rate())) << "s." << std::endl;
    for (int i = 0; i < num; i++) {
        tx_stream->send(&zeropadding.front(), spb, md, 0.1);
        md.has_time_spec = false;
    }
    
    // TODO: Implement memory caching of input file.
    std::ifstream infile(file.c_str(), std::ifstream::binary);
    int num_iter = 10;
    for (int file_iter = 0; file_iter < num_iter; file_iter++) {

        std::vector<std::complex<float> > buff(spb);
        bool eof = false;

        while(not eof){

            infile.read((char*)&buff.front(), buff.size()*sizeof(std::complex<float>));
            size_t num_tx_samps = size_t(infile.gcount()/sizeof(std::complex<float>));
            md.end_of_burst = infile.eof() and file_iter == num_iter - 1;
            eof = infile.eof();
            tx_stream->send(&buff.front(), num_tx_samps, md, 30);

        }

        infile.clear();
        infile.seekg(0, std::ios::beg);
    }

    infile.close();
    stop_signal_called = true;
}

void recv_to_file(
    uhd::usrp::multi_usrp::sptr usrp_device,
    double start_time,
    const std::string &file
){
    unsigned long long num_total_samps = 0;
    int spb = 10000;
    //create a receive streamer
    uhd::stream_args_t stream_args("fc32", "sc16");

    std::vector<size_t> channel_nums;
    channel_nums.push_back(boost::lexical_cast<size_t>(0));
    stream_args.channels = channel_nums;
    uhd::rx_streamer::sptr rx_stream = usrp_device->get_rx_stream(stream_args);

    // Prepare buffers for received samples and metadata
    uhd::rx_metadata_t md;
    std::vector<std::complex<float> > buff(spb);
    std::ofstream outfile;
    outfile.open(file.c_str(), std::ofstream::binary);

    bool overflow_message = true;
    bool first_message = true;
    float timeout = start_time + 0.3f; //expected settling time + padding for first recv

    //setup streaming
    uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_START_CONTINUOUS);
    stream_cmd.num_samps = 0;
    stream_cmd.stream_now = false;
    stream_cmd.time_spec = uhd::time_spec_t(start_time);

    rx_stream->issue_stream_cmd(stream_cmd);
    std::cout << "Starting receiver at " << start_time << " s." << std::endl;

    while(not stop_signal_called){
        // blocking
        size_t num_rx_samps = rx_stream->recv(&buff.front(), buff.size(), md, timeout);
        timeout = 0.1f; //small timeout for subsequent recv

        if (md.error_code == uhd::rx_metadata_t::ERROR_CODE_TIMEOUT) {
            std::cout << boost::format("Timeout while streaming") << std::endl;
            break;
        }

        if (md.error_code == uhd::rx_metadata_t::ERROR_CODE_OVERFLOW){
            if (overflow_message){
                overflow_message = false;
                std::cerr << boost::format(
                    "Got an overflow indication. Please consider the following:\n"
                    "  Your write medium must sustain a rate of %fMB/s.\n"
                    "  Dropped samples will not be written to the file.\n"
                    "  Please modify this example for your purposes.\n"
                    "  This message will not appear again.\n"
                ) % (usrp_device->get_rx_rate()*sizeof(std::complex<float>)/1e6);
            }
            continue;
        }
        if (md.error_code != uhd::rx_metadata_t::ERROR_CODE_NONE){
            throw std::runtime_error(str(boost::format(
                "Receiver error %s"
            ) % md.strerror()));
        }

        num_total_samps += num_rx_samps;

        if (outfile.is_open()) {
            outfile.write((const char*) &buff.front(), num_rx_samps*sizeof(std::complex<float>));
        } else {
            std::cout << "outfile not open!";
        }

    }
    // Shut down receiver
    stream_cmd.stream_mode = uhd::stream_cmd_t::STREAM_MODE_STOP_CONTINUOUS;
    rx_stream->issue_stream_cmd(stream_cmd);

    std::cout << std::flush;

    // Close file
    outfile.close();
}
