pn_signal = mls(17);
output_file = fopen('output/mls.bin', 'w')
fwrite(output_file, pn_signal, 'double')
