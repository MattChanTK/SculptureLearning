% determine whether or not the attractor is in the fov of the SimSon
% fov is in radion, attInFOV is an numAud x numAtt matrix
function attInFOV = getAttInFOV( Att, SimSon, fov)

    [numAud temp] = size(SimSon);
    [numAtt temp] = size(Att);
    
    angles = zeros(numAud, numAtt);
    
    %get the angle of the attractor relative to SimSon
    for i = 1:numAtt
        angles(:,i) = atan2(Att(i, 2)-SimSon(:,2), Att(i,1)-SimSon(:,1));
    end

    
    attInFOV = zeros(numAud, numAtt);
    
    % special case when SimSon FOV is span through the X-axis
    wrapAround = (SimSon(:,3) + fov/2) > 2*pi;
        
    % check if the attractor is within the FOV for each SimSon
    for j = 1:numAtt
        
        angles(:,j) = angles(:,j) + wrapAround*2*pi;
        attInFOV(:,j) = (angles (:,j) < (SimSon(:,3) + fov/2) ...
                        & angles(:,j) > (SimSon(:,3) - fov/2));
    end
    

end

