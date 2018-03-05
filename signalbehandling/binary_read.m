clear;
clf;
samp_rate = 0.064000e6; % samp/second

in_file_handler = fopen('usrp_samples.dat');
in_signal = fread(in_file_handler, 'double');
fclose(in_file_handler);

in_i_signal = in_signal(1:2:length(in_signal));
in_q_signal = in_signal(2:2:length(in_signal));
in_complex_signal = in_i_signal+1i*in_q_signal;

reference_file_handler = fopen('../signalgenerering/output/comb.bin');
reference_signal = fread(reference_file_handler, 'double');

reference_i_signal = reference_signal(1:2:length(reference_signal));
reference_q_signal = reference_signal(2:2:length(reference_signal));
reference_complex_signal = reference_i_signal+1i*reference_q_signal;

number_of_fft_samples = 2;
fft_size = 2^12;
offset = 2^12;
sample_offsets = transpose(offset + fft_size*(0:number_of_fft_samples-1));
sample_points = repmat((1:fft_size), number_of_fft_samples, 1) + sample_offsets;

in_fft_samples = in_complex_signal(sample_points);

% fftshift to convert to gnuradio presentation.
in_Y = fftshift(fft(in_fft_samples, [], 2));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(in_Y));
subplot(3, 1, 1);
plot(frequencies, abs(in_Y));

% offset fft window start
reference_fft_samples = reference_complex_signal(sample_points);
% fftshift to convert to gnuradio presentation.
reference_Y = fftshift(fft(reference_fft_samples, [], 2));

frequencies = linspace(-samp_rate/2, samp_rate/2, length(reference_Y));
subplot(3, 1, 2);
plot(frequencies, abs(reference_Y));

subplot(3, 1, 3);

phase_differences = angle(reference_Y) - angle(in_Y);

reference_threshold = 100;
reference_under_amplitude = abs(reference_Y) < reference_threshold;
in_threshold = 5;
in_under_amplitude = abs(in_Y) < in_threshold;

combined_samples_under_amplitude = or(reference_under_amplitude, in_under_amplitude);

phase_differences(combined_samples_under_amplitude) = NaN;

X = cos(phase_differences);
Y = sin(phase_differences);
average_X = nanmean(X, 1);
average_Y = nanmean(Y, 1);
average_phase = angle(average_X + 1i*average_Y);

plot(frequencies, unwrap(average_phase), 'o');

