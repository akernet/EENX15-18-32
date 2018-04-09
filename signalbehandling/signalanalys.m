% Stand in the same folder as the data files
clear;
clc;
clf;
samp_rate = 6e5; % samp/second
fft_size = 2^10; % FFT-bin size
windowSize = 4096;
b = (1/windowSize)*ones(1,windowSize);
a = 1;

% Read the first data file. Assign to complex is done later
% after the the reference file is read because of reasons
in_file_handler = fopen('outfile.bin');
out1 = fread(in_file_handler, 'float');
fclose(in_file_handler);

% Read the second data file and assign complex
in_file_handler = fopen('outfile2.bin');
out2 = fread(in_file_handler, 'float');
length(out2)/2
re_out2 = out2(1:2:end);
im_out2 = out2(2:2:end);
out2 = re_out2 + 1i * im_out2;
fclose(in_file_handler);

% Read the reference file and make it as long as the output data files
% Also assign out1 to complex
in_file_handler = fopen('infile.bin');
in = fread(in_file_handler, 'float');
length(in)/2
in = repmat(in, ceil(length(out1)/length(in)), 1);
in = in(1:length(out1));
re_in = in(1:2:end);
im_in = in(2:2:end);
in = re_in + 1i * im_in;
fclose(in_file_handler);
re_out1 = out1(1:2:end);
im_out1 = out1(2:2:end);
out1 = re_out1 + 1i * im_out1;

% Create matrix used to partition the data into fft_size:d bins
repetitions = floor(length(out1)/fft_size)-1;
bin_matrix = repmat((1:fft_size) , repetitions, 1) + transpose(fft_size*(1:repetitions));

% Partition the data into bins
out1_bin = out1(bin_matrix);
out2_bin = out2(bin_matrix);
in_bin = in(bin_matrix);

% Get the frequency domain of the data with the desired number of
% samples/bin
out1_bin_fft = fft(out1_bin, [], 2);
out2_bin_fft = fft(out2_bin, [], 2);
in_bin_fft = fft(in_bin, [], 2);

% Plot the argument difference between output data and reference data
subplot(1,2,1)
plot(1:repetitions, unwrap(angle(out1_bin_fft(:,81)) - angle(in_bin_fft(:,81))))

subplot(1,2,2)
plot(1:repetitions, unwrap(angle(out2_bin_fft(:,81)) - angle(in_bin_fft(:,81))))
%%
plot(1:repetitions, angle(in_bin_fft(:,81)))

%%
k = 0;
for i=1:length(out1_bin_fft)
    if max(abs(out1_bin_fft(i,:))) > 0.3
        k = i
        break;
    end
end
f = 1:fft_size;
subplot(1,3,1)
plot(f, abs(out1_bin_fft(k,:)))

subplot(1,3,2)
plot(f, abs(out2_bin_fft(k,:)))

subplot(1,3,3)
plot(f, abs(in_bin_fft(k,:)))


%%
t = (1:length(re_out1));%/samp_rate;

subplot(1,3,1)
plot(t, re_out1);

subplot(1,3,2)
plot(t, re_out2);


subplot(1,3,3)
plot(t, re_in);