function [delta] = getDeltaPhase(timeD,angleD)
    preSwitchStart = ceil(0.14*length(timeD));
    preSwitchEnd = ceil(0.55*length(timeD));

    postSwitchStart = ceil(0.64*length(timeD));
    postSwitchEnd = ceil(0.95*length(timeD));

    preSwitchTime = timeD(preSwitchStart:preSwitchEnd);
    preSwitchAngle = angleD(preSwitchStart:preSwitchEnd);

    postSwitchTime = timeD(postSwitchStart:postSwitchEnd);
    postSwitchAngle = angleD(postSwitchStart:postSwitchEnd);

    [preSwitchFit, preSwitchGOF] = createFit(preSwitchTime, preSwitchAngle);
    preSwitchGOF.rsquare
    [postSwitchFit, postSwitchGOF] = createFit(postSwitchTime, postSwitchAngle);

    preSwitchOffset = preSwitchFit.p2;
    postSwitchOffset = postSwitchFit.p2;

    deltaAngle = preSwitchOffset - postSwitchOffset;
    deltaCos = cos(deltaAngle);
    deltaSin = sin(deltaAngle);
    deltaComplex = deltaCos + 1i*deltaSin;
    delta = angle(deltaComplex);
end

