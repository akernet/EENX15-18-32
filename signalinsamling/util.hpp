static bool stop_signal_called = false;

void init_matrix();

void send_scpi(std::string command_string);

void switch_matrix(int port1, int port2, float delay);

void switch_antenna(uhd::usrp::multi_usrp::sptr usrp_device, float time);

void send_from_file(uhd::usrp::multi_usrp::sptr usrp_device, double start_time, const std::string &file);

void recv_to_file(uhd::usrp::multi_usrp::sptr usrp_device, double start_time, const std::string &file);
