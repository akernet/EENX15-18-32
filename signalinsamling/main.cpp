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

namespace po = boost::program_options;

/***********************************************************************
 * Signal handlers
 **********************************************************************/
static bool stop_signal_called = false;
void sig_int_handler(int){stop_signal_called = true;}

void send_from_file(
    uhd::usrp::multi_usrp::sptr usrp_device,
    const std::string &file
){
    // Samples per buffer.
    int spb = 5000;
    uhd::tx_metadata_t md;

    md.start_of_burst = true;
    md.end_of_burst = false;

    // Start stream at 3 s.
    md.has_time_spec = true;
    uhd::time_spec_t tspec(3.0);
    md.time_spec = tspec;
     
    // Zeropadding buffer. 
    std::vector<std::complex<float>> zeropadding(spb);
    for (int i = 0; i < spb; i++) {
        zeropadding.push_back(std::complex<float>(0.0, 0.0));
    }

    uhd::stream_args_t stream_args("fc32", "sc16");

    std::vector<size_t> channel_nums;
    channel_nums.push_back(0);

    stream_args.channels = channel_nums;
    uhd::tx_streamer::sptr tx_stream = usrp_device->get_tx_stream(stream_args);
    
    int num = 20;
    std::cout << "Sending initial zero padding at time 3 s." << std::endl;
    for (int i = 0; i < num; i++) {
        tx_stream->send(&zeropadding.front(), spb, md, 0.1);
        md.has_time_spec = false;
    }
    
    // TODO: Implement memory caching of input file.
    std::ifstream infile(file.c_str(), std::ifstream::binary);
    int num_iter = 3;
    for (int file_iter = 0; file_iter < num_iter; file_iter++) {

        std::vector<std::complex<float>> buff(spb);
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
    std::vector<std::complex<float>> buff(spb);
    std::ofstream outfile;
    outfile.open(file.c_str(), std::ofstream::binary);

    bool overflow_message = true;
    bool first_message = true;
    float timeout = 3.2f; //expected settling time + padding for first recv

    //setup streaming
    uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_START_CONTINUOUS);
    stream_cmd.num_samps = 0;
    stream_cmd.stream_now = false;
    stream_cmd.time_spec = uhd::time_spec_t(3.0);

    rx_stream->issue_stream_cmd(stream_cmd);
    std::cout << "Starting receiver at 3 s." << std::endl;
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


/***********************************************************************
 * Main function
 **********************************************************************/
int UHD_SAFE_MAIN(int argc, char *argv[]){
    uhd::set_thread_priority_safe();

    //transmit variables to be set by po
    double freq, tx_gain, tx_bw;

    //receive variables to be set by po
    std::string rx_args, file, type, rx_ant, rx_subdev, rx_channels;
    size_t total_num_samps, spb;
    double samp_rate, rx_freq, rx_gain, rx_bw;

    //setup the program options
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "help message")
        ("samp-rate", po::value<double>(&samp_rate), "rate of transmit outgoing samples")
        ("freq", po::value<double>(&freq), "receive RF center frequency in Hz")
        ("tx-gain", po::value<double>(&tx_gain), "gain for the transmit RF chain")
        ("rx-gain", po::value<double>(&rx_gain), "gain for the receive RF chain")
        ("tx-bw", po::value<double>(&tx_bw), "analog transmit filter bandwidth in Hz")
        ("rx-bw", po::value<double>(&rx_bw), "analog receive filter bandwidth in Hz")
    ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    //print the help message
    if (vm.count("help")){
        std::cout << boost::format("UHD TXRX Loopback to File %s") % desc << std::endl;
        return ~0;
    }

    //create a usrp device
    uhd::usrp::multi_usrp::sptr usrp_device = uhd::usrp::multi_usrp::make(uhd::device_addr_t());

    //Lock mboard clocks
    usrp_device->set_clock_source("internal");

    usrp_device->set_tx_antenna("TX/RX");
    usrp_device->set_rx_antenna("RX2");

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << boost::format("Setting TX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    usrp_device->set_tx_rate(samp_rate);
    std::cout << boost::format("Actual TX Rate: %f Msps...") % (usrp_device->get_tx_rate()/1e6) << std::endl << std::endl;

    std::cout << boost::format("Setting RX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    usrp_device->set_rx_rate(samp_rate);
    std::cout << boost::format("Actual RX Rate: %f Msps...") % (usrp_device->get_rx_rate()/1e6) << std::endl << std::endl;

    //set the transmit center frequency
    if (not vm.count("freq")){
        std::cerr << "Please specify the transmit center frequency with --freq" << std::endl;
        return ~0;
    }

    std::cout << boost::format("Setting TX Freq: %f MHz...") % (freq/1e6) << std::endl;
    uhd::tune_request_t tx_tune_request(freq);
    usrp_device->set_tx_freq(tx_tune_request);
    std::cout << boost::format("Actual TX Freq: %f MHz...") % (usrp_device->get_tx_freq()/1e6) << std::endl << std::endl;

    //set the rf gain
    if (vm.count("tx-gain")){
        std::cout << boost::format("Setting TX Gain: %f dB...") % tx_gain << std::endl;
        usrp_device->set_tx_gain(tx_gain);
        std::cout << boost::format("Actual TX Gain: %f dB...") % usrp_device->get_tx_gain() << std::endl << std::endl;
    }

    std::cout << boost::format("Setting RX Freq: %f MHz...") % (freq/1e6) << std::endl;
    uhd::tune_request_t rx_tune_request(freq);
    usrp_device->set_rx_freq(rx_tune_request);
    std::cout << boost::format("Actual RX Freq: %f MHz...") % (usrp_device->get_rx_freq()/1e6) << std::endl << std::endl;

    //set the receive rf gain
    if (vm.count("rx-gain")){
        std::cout << boost::format("Setting RX Gain: %f dB...") % rx_gain << std::endl;
        usrp_device->set_rx_gain(rx_gain);
        std::cout << boost::format("Actual RX Gain: %f dB...") % usrp_device->get_rx_gain() << std::endl << std::endl;
    }


    //Check Ref and LO Lock detect
    std::vector<std::string> sensor_names;
    sensor_names = usrp_device->get_tx_sensor_names(0);
    if (std::find(sensor_names.begin(), sensor_names.end(), "lo_locked") != sensor_names.end()) {
        uhd::sensor_value_t lo_locked = usrp_device->get_tx_sensor("lo_locked",0);
        std::cout << boost::format("Checking lock: %s ...") % lo_locked.to_pp_string() << std::endl;
        UHD_ASSERT_THROW(lo_locked.to_bool());
    }

    std::cout << "Clock rate is " << usrp_device->get_master_clock_rate() << std::endl;


    std::cout << "Sleeping for 5 seconds" << std::endl << std::flush; 
    std::this_thread::sleep_for(std::chrono::seconds(5));

    //reset usrp time to prepare for transmit/receive
    std::cout << boost::format("Setting device timestamp to 0...") << std::endl;
    usrp_device->set_time_now(uhd::time_spec_t(0.0));

    std::cout << "Press Ctrl + C to stop streaming..." << std::endl;

    //start transmit worker thread
    boost::thread_group transmit_thread;
    std::string in_file_path = "infile.bin";
    std::string out_file_path = "outfile.bin";
    transmit_thread.create_thread(boost::bind(&send_from_file, usrp_device, in_file_path));

    //recv to file
    recv_to_file(usrp_device, out_file_path);

    //clean up transmit worker
    stop_signal_called = true;
    transmit_thread.join_all();

    //finished
    std::cout << std::endl << "Done!" << std::endl << std::endl;
    return EXIT_SUCCESS;
}
