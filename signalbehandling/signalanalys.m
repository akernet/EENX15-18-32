% Stand in the same folder as the data files
clear;
clc;
clf;
addpath('../../signalbehandling/figures');
sampRate = 6e5; % samp/second
fftSize = 2^10; % FFT-bin size

% Read the first data file. Assign to complex is done later
% after the the reference file is read because of reasons
inFileHandler = fopen('outfile.bin');
out1 = fread(inFileHandler, 'float');
fclose(inFileHandler);

% Read the second data file and assign complex
inFileHandler = fopen('outfile2.bin');
out2 = fread(inFileHandler, 'float');
length(out2)/2
reOut2 = out2(1:2:end);
imOut2 = out2(2:2:end);
out2 = reOut2 + 1i * imOut2;
fclose(inFileHandler);

% Read the reference file and make it as long as the output data files
% Also assign out1 to complex
inFileHandler = fopen('infile.bin');
in = fread(inFileHandler, 'float');
length(in)/2
in = repmat(in, ceil(length(out1)/length(in)), 1);
in = in(1:length(out1));
reIn = in(1:2:end);
imIn = in(2:2:end);
in = reIn + 1i * imIn;
fclose(inFileHandler);
reOut1 = out1(1:2:end);
imOut1 = out1(2:2:end);
out1 = reOut1 + 1i * imOut1;

% Create matrix used to partition the data into fftSize:d bins
repetitions = floor(length(out1)/fftSize)-1;
binMatrix = repmat((1:fftSize) , repetitions, 1) + transpose(fftSize*(0:repetitions-1));

% Partition the data into bins
out1Bin = out1(binMatrix);
out2Bin = out2(binMatrix);
inBin = in(binMatrix);

% Get the frequency domain of the data with the desired number of
% samples/bin
out1BinFft = fft(out1Bin, [], 2);
out2BinFft = fft(out2Bin, [], 2);
inBinFft = fft(inBin, [], 2);

% Generate phase difference plot
figure('rend','painters','pos',[10 10 700 300])
plot((1:repetitions)*fftSize/sampRate, (angle(out2BinFft(:,81)./inBinFft(:,81))),'blue',...
    (1:repetitions)*fftSize/sampRate, (angle(out1BinFft(:,81)./inBinFft(:,81))),'black--','LineWidth',1)
set(gca, 'FontSize', 15)
xlabel('Tid (s)','FontSize',15)
ylabel('Fasskillnad (rad)','FontSize',15)
title('Fasmätningar','FontSize',30)
legend({'Mätning 1','Mätning 2'},'FontSize',15)
axis([0 repetitions*fftSize/sampRate -4 4])

% matlab2tikz dynamic LaTeX-figures
matlab2tikz('../../signalbehandling/figures/phase-difference.tex')

% Plot example signal
t = (1:length(reOut1));%/sampRate;
t = (length(t)/2:length(t)/2+100);

figure('rend','painters','pos',[10 10 700 300])
plot((t-t(1))*1e3/sampRate, reOut1(t),'black','LineWidth',1);
%set(gca,'YTickLabel',[],'FontSize',15)
ylabel('Spänning (godtycklig skala)')
xlabel('Tid (ms)')
axis([0 (t(end)-t(1))*1e3/sampRate -4e-4 4e-4])
matlab2tikz('../../signalbehandling/figures/example-signal.tex')

% Plot the reference signal
figure('rend','painters','pos',[10 10 700 300])
plot((t-t(1))*1e3/sampRate, reIn(t),'black','LineWidth',1);
set(gca,'YTickLabel',[],'FontSize',15)
ylabel('Spänning (godtycklig skala)')
axis([0 (t(end)-t(1))*1e3/sampRate -1 1])
matlab2tikz('../../signalbehandling/figures/reference-signal.tex')