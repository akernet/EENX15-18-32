samp_freq = 50e6; % samp/s
samp_period = 1/samp_freq; % s
signal_freq = 1e3; % Hz
signal_period = 1/signal_freq; % s
samp_per_signal_period = samp_freq * signal_period; % samp

t = 0:samp_period:signal_period;

signal = 0+cos(signal_freq*2*pi*t);
analytic_signal = hilbert(signal);

i_signal = real(analytic_signal);
q_signal = imag(analytic_signal);

figure(1)
clf
hold on;
plot(t, i_signal);
plot(t, q_signal);

figure(2)
clf
Y = fftshift(fft(analytic_signal));
frequency_bins = linspace(-samp_freq/2, samp_freq/2, length(Y));
plot(frequency_bins, abs(Y))
