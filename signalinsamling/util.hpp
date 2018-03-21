static bool stop_signal_called = false;

void send_from_file(uhd::usrp::multi_usrp::sptr usrp_device, const std::string &file);

void recv_to_file(uhd::usrp::multi_usrp::sptr usrp_device, const std::string &file);
