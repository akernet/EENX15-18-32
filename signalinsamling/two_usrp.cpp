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
    double freq, tx_gain, tx_bw;

    //receive variables to be set by po
    std::string tx_serial, rx_serial;
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
        ("tx-serial", po::value<std::string>(&tx_serial), "tx card serial number (12345678)") 
        ("rx-serial", po::value<std::string>(&rx_serial), "rx card serial number (12345678)") 
    ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    //print the help message
    if (vm.count("help")){
        std::cout << boost::format("UHD TXRX Loopback to File %s") % desc << std::endl;
        return ~0;
    }

    if (not vm.count("tx-serial")) {
        std::cerr << "Please specify the tx serial" << std::endl;
        return ~0;
    }

    if (not vm.count("rx-serial")) {
        std::cerr << "Please specify the rx serial" << std::endl;
        return ~0;
    }

    // Create tx device
    uhd::device_addr_t tx_hint;
    tx_hint["serial"] = tx_serial;
    uhd::usrp::multi_usrp::sptr tx_usrp_device = uhd::usrp::multi_usrp::make(tx_hint);
    
    // Create rx device
    uhd::device_addr_t rx_hint;
    rx_hint["serial"] = rx_serial;
    uhd::usrp::multi_usrp::sptr rx_usrp_device = uhd::usrp::multi_usrp::make(rx_hint);

    //Lock mboard clocks
    tx_usrp_device->set_clock_source("external");
    rx_usrp_device->set_clock_source("external");

    tx_usrp_device->set_tx_antenna("TX/RX");
    // Switch intial antenna config to tx/rx.
    rx_usrp_device->set_rx_antenna("RX2");

    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << boost::format("Setting TX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    tx_usrp_device->set_tx_rate(samp_rate);
    std::cout << boost::format("Actual TX Rate: %f Msps...") % (tx_usrp_device->get_tx_rate()/1e6) << std::endl << std::endl;

    std::cout << boost::format("Setting RX Rate: %f Msps...") % (samp_rate/1e6) << std::endl;
    rx_usrp_device->set_rx_rate(samp_rate);
    std::cout << boost::format("Actual RX Rate: %f Msps...") % (rx_usrp_device->get_rx_rate()/1e6) << std::endl << std::endl;

    //set the transmit center frequency
    if (not vm.count("freq")){
        std::cerr << "Please specify the transmit center frequency with --freq" << std::endl;
        return ~0;
    }

    std::cout << boost::format("Setting TX Freq: %f MHz...") % (freq/1e6) << std::endl;
    uhd::tune_request_t tx_tune_request(freq);
    tx_usrp_device->set_tx_freq(tx_tune_request);
    std::cout << boost::format("Actual TX Freq: %f MHz...") % (tx_usrp_device->get_tx_freq()/1e6) << std::endl << std::endl;

    //set the rf gain
    if (vm.count("tx-gain")){
        std::cout << boost::format("Setting TX Gain: %f dB...") % tx_gain << std::endl;
        tx_usrp_device->set_tx_gain(tx_gain);
        std::cout << boost::format("Actual TX Gain: %f dB...") % tx_usrp_device->get_tx_gain() << std::endl << std::endl;
    }

    std::cout << boost::format("Setting RX Freq: %f MHz...") % (freq/1e6) << std::endl;
    uhd::tune_request_t rx_tune_request(freq);
    rx_usrp_device->set_rx_freq(rx_tune_request);
    std::cout << boost::format("Actual RX Freq: %f MHz...") % (rx_usrp_device->get_rx_freq()/1e6) << std::endl << std::endl;

    //set the receive rf gain
    if (vm.count("rx-gain")){
        std::cout << boost::format("Setting RX Gain: %f dB...") % rx_gain << std::endl;
        rx_usrp_device->set_rx_gain(rx_gain);
        std::cout << boost::format("Actual RX Gain: %f dB...") % rx_usrp_device->get_rx_gain() << std::endl << std::endl;
    }

    //Check Ref and LO Lock detect
    std::vector<std::string> sensor_names;
    // TODO: Add rx lock detection
    sensor_names = tx_usrp_device->get_tx_sensor_names(0);
    if (std::find(sensor_names.begin(), sensor_names.end(), "lo_locked") != sensor_names.end()) {
        uhd::sensor_value_t lo_locked = tx_usrp_device->get_tx_sensor("lo_locked", 0);
        std::cout << boost::format("Checking lock: %s ...") % lo_locked.to_pp_string() << std::endl;
        UHD_ASSERT_THROW(lo_locked.to_bool());
    }

    std::cout << "Clock rate is " << tx_usrp_device->get_master_clock_rate() << std::endl;

    std::cout << "Sleeping for 5 seconds" << std::endl << std::flush; 
    std::this_thread::sleep_for(std::chrono::seconds(5));

    //reset usrp time to prepare for transmit/receive
    // TODO: Add lag compensation.
    std::cout << boost::format("Setting device timestamp to 0...") << std::endl;
    tx_usrp_device->set_time_now(uhd::time_spec_t(0.0));
    rx_usrp_device->set_time_now(uhd::time_spec_t(0.0));

    std::cout << "Press Ctrl + C to stop streaming..." << std::endl;

    //start transmit worker thread
    boost::thread_group transmit_thread;
    std::string in_file_path = "infile.bin";
    std::string out_file_path = "outfile.bin";
    transmit_thread.create_thread(boost::bind(&send_from_file, tx_usrp_device, 4.0f, in_file_path));

    boost::thread_group switch_thread;
    switch_thread.create_thread(boost::bind(&switch_antenna, rx_usrp_device, 5.0f));

    //recv to file
    recv_to_file(rx_usrp_device, 3.0f, out_file_path);

    //clean up transmit worker
    stop_signal_called = true;
    transmit_thread.join_all();

    //finished
    std::cout << std::endl << "Done!" << std::endl << std::endl;
    return EXIT_SUCCESS;
}
