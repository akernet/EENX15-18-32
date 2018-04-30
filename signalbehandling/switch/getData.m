function complex_data = getData(path)
    fileHandler = fopen(path);
    data = fread(fileHandler, 'float');
    i_channel = data(1:2:end);
    q_channel = data(2:2:end);
    complex_data = i_channel + 1i*q_channel;
end

