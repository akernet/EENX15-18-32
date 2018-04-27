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
    std::cout << "Initilizing switch matrix" << std::endl << std::flush;
    init_matrix();
    std::string command_string = (std::string) argv[1];
    std::cout << "Sending scpi command: " << command_string << std::endl;
    send_scpi(command_string);
    std::cout << std::endl << "Done!" << std::endl << std::endl << std::flush;
    return EXIT_SUCCESS;
}
