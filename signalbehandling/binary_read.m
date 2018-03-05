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

number_of_fft_samples = 10;
fft_size = 2^10;
offset = 1;
sample_offsets = transpose(offset + fft_size*(0:number_of_fft_samples-1));
sample_points = repmat((1:fft_size), number_of_fft_samples, 1) + sample_offsets;

fft_samples = in_complex_signal(sample_points);

% fftshift to convert to gnuradio presentation.
in_Y = fftshift(fft(fft_samples, [], 2));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(in_Y));
subplot(3, 1, 1);
plot(frequencies, abs(in_Y));

% offset fft window start
fft_samples = reference_complex_signal(sample_points);
% fftshift to convert to gnuradio presentation.
reference_Y = fftshift(fft(fft_samples, [], 2));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(reference_Y));
subplot(3, 1, 2);
plot(frequencies, abs(reference_Y));

subplot(3, 1, 3);

phase_differences = angle(reference_Y) - angle(in_Y);
X = cos(phase_differences);
Y = sin(phase_differences);
average_X = mean(X, 1);
average_Y = mean(Y, 1);
average_phase = angle(average_X + 1i*average_Y);

plot(frequencies, unwrap(average_phase));

