function [binFrequencies, deltaPhases] = getParameters(filePath, centerFrequency)
    data = getData(filePath);

    fftSize = 2*2*2*2*2*1024;

    sampRate = 6e5;

    fftPoints = (1:fftSize);
    spacingPoints = (0:fftSize/128:length(data)-fftSize-1);
    [pointsX, pointsY] = meshgrid(fftPoints, spacingPoints);
    dataPoints = pointsX + pointsY;
    fftWindows = (fft(data(dataPoints), [], 2));
    amplitude = abs(fftWindows);
    amplitude = amplitude/max(max(amplitude));
    phase = angle(fftWindows);
    phase = phase + 2*pi*(phase < 0);

    frequencies = (pointsX-1)*(sampRate/fftSize);
    startTimes = (pointsY)*(1/sampRate);

    frequencyPhaseWindowStart = mod(2*pi.*frequencies.*startTimes, 2*pi);

    relativePhase = phase - frequencyPhaseWindowStart;

    bins = [2732, 5462, 8193, 10923, 13654];
    binFrequencies = frequencies(1, bins)+centerFrequency;
    deltaPhases = zeros(1, length(bins));
    
    for binIndex = 1:length(bins)
        bin = bins(binIndex);
        timeD = (1/sampRate)*pointsY(:, bin);
        %pointsD = pointsY(:, bin);
        angleD = unwrap(relativePhase(:, bin));
        [delta] = getDeltaPhase(timeD, angleD);
        deltaPhases(binIndex) = delta;
    end
end
