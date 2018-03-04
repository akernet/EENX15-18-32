clear;


samp_rate = 0.064000e6; % samp/second

in_file_handler = fopen('usrp_samples.dat');
in_signal = fread(in_file_handler, 'double');
fclose(in_file_handler);

in_i_signal = in_signal(1:2:length(in_signal));
in_q_signal = in_signal(2:2:length(in_signal));
in_complex_signal = in_i_signal+1i*in_q_signal;

reference_file_handler = fopen('../signalgenerering/output/mls.bin');
reference_signal = fread(reference_file_handler, 'double');

reference_i_signal = reference_signal(1:1:length(reference_signal));
reference_q_signal = 0;
reference_complex_signal = reference_i_signal+1i*reference_q_signal;

% offset fft window start

fft_size = 2^10;
offset = fft_size*8;
fft_sample = in_complex_signal((offset:(offset+fft_size-1)));

% fftshift to convert to gnuradio presentation.
in_Y = fftshift(fft(fft_sample));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(in_Y));
subplot(3, 1, 1);
plot(frequencies, abs(in_Y));


% offset fft window start
fft_sample = reference_complex_signal((offset:(offset+fft_size-1)));

% fftshift to convert to gnuradio presentation.
reference_Y = fftshift(fft(fft_sample));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(reference_Y));
subplot(3, 1, 2);
plot(frequencies, abs(reference_Y));

subplot(3, 1, 3);
hold on;
threshold = abs(in_Y) > 0.005;
threshold_frequencies = frequencies(threshold);
phase_diff = (angle(in_Y./reference_Y))
threshold_phase_diff = phase_diff(threshold);
plot(threshold_frequencies, unwrap(threshold_phase_diff));

