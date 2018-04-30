centerFrequencies = 1e9:5e7:2e9;

dirName = 'tomas1';
pointsPerCenterFrequency = 5;
numResults = length(centerFrequencies)*pointsPerCenterFrequency;
resultFrequencies = zeros(1, numResults);
resultPhases = zeros(1, numResults);
index = 1;
for centerFrequency = centerFrequencies
    fileName = [dirName '/outfile' num2str(centerFrequency, '%d') '.0.bin'];
    [freq, phase] = getParameters(fileName, centerFrequency);
    resultFrequencies(index:index+pointsPerCenterFrequency-1) = freq;
    resultPhases(index:index+pointsPerCenterFrequency-1) = phase;
    index = index + pointsPerCenterFrequency;
end
hold on;

plot(resultFrequencies, (resultPhases), 'o');