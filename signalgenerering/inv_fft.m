clf
samp_rate = 10e5;
vector_length = 2^15;


frequencies = linspace(-samp_rate/2, samp_rate/2, vector_length);
frequency_bins = zeros(vector_length, 1);

signal_frequencies = (0:10000:samp_rate/2);

[closeness, indices] = min ( abs(repmat(frequencies, length(signal_frequencies)) - transpose(signal_frequencies)), [], 2 )

frequency_bins(indices) = 1;

figure(1)
clf
plot(frequencies, frequency_bins)

Y = ifftshift(frequency_bins)

%plot((1:length(Y)), Y)

figure(2)
clf
y = ifft(Y)
t = linspace(0, 1/samp_rate*length(y), length(y))
plot3(t, real(y), imag(y))
%%

hold on;

signal_frequencies = [(-1e3)];

[closeness, indices] = min ( abs(repmat(frequencies, length(signal_frequencies)) - transpose(signal_frequencies)), [], 2 )
frequency_bins = zeros(vector_length, 1);

frequency_bins(indices) = 1;

%plot(frequencies, frequency_bins)

Y = ifftshift(frequency_bins)

%plot((1:length(Y)), Y)


y = ifft(Y)
%t = linspace(0, 1/samp_rate*length(y), length(y))
plot3(t, real(y), imag(y))