clf
samp_rate = 64e3;
vector_length = 2^17;

frequencies = linspace(-samp_rate/2, samp_rate/2, vector_length);
frequency_bins = zeros(vector_length, 1);

signal_frequencies = (0:5000:samp_rate/2);

[closeness, indices] = min ( abs(repmat(frequencies, length(signal_frequencies)) - transpose(signal_frequencies)), [], 2 );

frequency_bins(indices) = 1;

figure(1)
clf
plot(frequencies, frequency_bins);

Y = ifftshift(frequency_bins);

%plot((1:length(Y)), Y)

figure(2);
clf;
y = ifft(Y);
y = y/max(abs(y));
t = linspace(0, 1/samp_rate*length(y), length(y));
plot3(t, real(y), imag(y));
out = zeros(length(y)*2, 1);
out(1:2:length(out)) = real(y);
out(2:2:length(out)) = imag(y);
output_file = fopen('output/comb.bin', 'w')
fwrite(output_file, out, 'double')

