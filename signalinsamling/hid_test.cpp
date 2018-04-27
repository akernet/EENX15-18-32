#include <stdio.h>
#include <stdlib.h>
#include "hidapi.h"
#include <iostream>

int main(int argc, char* argv[])
{
  int res;

  std::cout << "test";

  // Initialize the hidapi library
  res = hid_init();

  std::cout << "test";
  // Enumerate and print all the HID devices on the system
  struct hid_device_info *devs, *cur_dev;

  std::cout << "test";
  devs = hid_enumerate(0x0, 0x0);
  std::cout << "test";
  cur_dev = devs;
  std::cout << cur_dev;
  while (cur_dev) {
    std::cout << "test";
    printf("Device Found\n  type: %04hx %04hx\n  path: %s\n  serial_number: %ls",
           cur_dev->vendor_id, cur_dev->product_id, cur_dev->path, cur_dev->serial_number);
    printf("\n");
    printf("  Manufacturer: %ls\n", cur_dev->manufacturer_string);
    printf("  Product:      %ls\n", cur_dev->product_string);
    printf("\n");
    cur_dev = cur_dev->next;
    std::cout << std::flush;
  }
  hid_free_enumeration(devs);

  return 0;
}
