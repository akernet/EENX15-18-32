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

#include <uhd/utils/thread_priority.hpp>
#include <uhd/utils/safe_main.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <boost/program_options.hpp>
#include <iostream>
#include <thread>

#include "util.hpp"

namespace po = boost::program_options;

/***********************************************************************
 * Main function
 **********************************************************************/
int UHD_SAFE_MAIN(int argc, char *argv[]){
    uhd::set_thread_priority_safe();

    //transmit variables to be set by po
    double start_freq, end_freq, tx_gain, tx_bw, step;

    //receive variables to be set by po
    std::string rx_args, file, type, rx_ant, rx_subdev, rx_channels;
    size_t total_num_samps, spb;
    double samp_rate, rx_freq, rx_gain, rx_bw;

    //setup the program options
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "help message")
        ("samp-rate", po::value<double>(&samp_rate), "rate of transmit outgoing samples")
        ("start-freq", po::value<double>(&start_freq), "starting center frequency in Hz")
        ("end-freq", po::value<double>(&start_freq), "ending center frequency in Hz")
        ("step", po::value<double>(&step), "frequency step for sweep in Hz")
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
    // Switch intial antenna config to tx/rx.
    usrp_device->set_rx_antenna("RX2");

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << boost::format("Setting TX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    usrp_device->set_tx_rate(samp_rate);
    std::cout << boost::format("Actual TX Rate: %f Msps...") % (usrp_device->get_tx_rate()/1e6) << std::endl << std::endl;

    std::cout << boost::format("Setting RX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    usrp_device->set_rx_rate(samp_rate);
    std::cout << boost::format("Actual RX Rate: %f Msps...") % (usrp_device->get_rx_rate()/1e6) << std::endl << std::endl;

    //set the transmit center frequency
    if (not vm.count("start-freq")){
        std::cerr << "Please specify the transmit starting center frequency with --start-freq" << std::endl;
        return ~0;
    }
    if (not vm.count("end-freq")){
        std::cerr << "Please specify the transmit ending center frequency with --end-freq" << std::endl;
        return ~0;
    }

    //set the receive rf gain
    if (vm.count("rx-gain")){
        std::cout << boost::format("Setting RX Gain: %f dB...") % rx_gain << std::endl;
        usrp_device->set_rx_gain(rx_gain);
        std::cout << boost::format("Actual RX Gain: %f dB...") % usrp_device->get_rx_gain() << std::endl << std::endl;
    }

    //set the rf gain
    if (vm.count("tx-gain")){
        std::cout << boost::format("Setting TX Gain: %f dB...") % tx_gain << std::endl;
        usrp_device->set_tx_gain(tx_gain);
        std::cout << boost::format("Actual TX Gain: %f dB...") % usrp_device->get_tx_gain() << std::endl << std::endl;
    }

    boost::thread_group transmit_thread;
    boost::thread_group switch_thread;
    std::string in_file_path;
    std::string out_file_path;
    
    int loopback_1 = 1;
    int loopback_2 = 2;
    
    int test_1 = 4;
    int test_2 = 5;

    //sweep through the frequencies
    for(double freq = start_freq; freq <= end_freq; freq += step){
        
        std::cout << "Resetting switch" << std::endl;
        switch_matrix(loopback_1, loopback_2, 0.0f);

        std::cout << boost::format("Setting TX Freq: %f MHz...") % (freq/1e6) << std::endl;
        uhd::tune_request_t tx_tune_request(freq);
        usrp_device->set_tx_freq(tx_tune_request);
        std::cout << boost::format("Actual TX Freq: %f MHz...") % (usrp_device->get_tx_freq()/1e6) << std::endl << std::endl;

        std::cout << boost::format("Setting RX Freq: %f MHz...") % (freq/1e6) << std::endl;
        uhd::tune_request_t rx_tune_request(freq);
        usrp_device->set_rx_freq(rx_tune_request);
        std::cout << boost::format("Actual RX Freq: %f MHz...") % (usrp_device->get_rx_freq()/1e6) << std::endl << std::endl;

        //Check Ref and LO Lock detect
        std::vector<std::string> sensor_names;
        sensor_names = usrp_device->get_tx_sensor_names(0);
        if (std::find(sensor_names.begin(), sensor_names.end(), "lo_locked") != sensor_names.end()) {
            uhd::sensor_value_t lo_locked = usrp_device->get_tx_sensor("lo_locked",0);
            std::cout << boost::format("Checking lock: %s ...") % lo_locked.to_pp_string() << std::endl;
            UHD_ASSERT_THROW(lo_locked.to_bool());
        }

        std::cout << "Clock rate is " << usrp_device->get_master_clock_rate() << std::endl;

        std::cout << "Sleeping for 1 seconds" << std::endl << std::flush; 
        std::this_thread::sleep_for(std::chrono::seconds(1));

        //reset usrp time to prepare for transmit/receive
        std::cout << boost::format("Setting device timestamp to 0...") << std::endl;
        usrp_device->set_time_now(uhd::time_spec_t(0.0));

        std::cout << "Press Ctrl + C to stop streaming..." << std::endl;

        //start transmit worker thread
        in_file_path = "infile.bin";
        out_file_path = boost::str(boost::format("sweep-measurements/outfile%.1f.bin")%freq);
        transmit_thread.create_thread(boost::bind(&send_from_file, usrp_device, 3.0f, in_file_path));
        
        switch_thread.create_thread(boost::bind(&switch_matrix, test_1, test_2, 4.0f));

        //recv to file
        recv_to_file(usrp_device, 2.9f, out_file_path);
    }

    //clean up transmit worker
    stop_signal_called = true;
    transmit_thread.join_all();

    //finished
    std::cout << std::endl << "Done!" << std::endl << std::endl << std::flush;
    return EXIT_SUCCESS;
}
